import socket
import random
import json
import threading
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8000))
print('连接成功')
car_list = []


# socket 发送数据并接受返回现有车辆信息
def send_info():
    car_list = []
    while True:
        msg = yield car_list
        if msg:
            s.send(msg.encode('utf-8'))
        print('发送完成')

        message = s.recv(1024)
        message.decode('utf-8')
        car_list = json.loads(message)


g = send_info()
g.send(None)


# 随机汽车进入
def running():
    while True:
        time.sleep(random.randint(1, 10))
        colors = ['black', 'white', 'yellow', 'blue', 'red']
        styles = ['SUV', '宝马', '奔驰', '小型轿车', '越野', '大众', '奥迪', '跑车', '货车', '现代']
        letter = [chr(i) for i in range(65, 91)]
        car_value = [f'京{random.choice(letter)}{random.randint(1000, 9999)}', random.choice(colors), random.choice(styles)]
        car_key = ['车牌号', '颜色', '类型']
        d = dict(zip(car_key, car_value))
        info = json.dumps(d)
        global car_list
        car_list = g.send(info)
        # car_list.append(car_value[0])


# 随机汽车离开
def leaving():
    while True:
        if not car_list:
            continue
        time.sleep(random.randint(1, 10) * 2)
        car_num = random.choice(car_list)
        car_num = json.dumps(car_num)
        g.send(car_num)


t1 = threading.Thread(target=running)
t2 = threading.Thread(target=leaving)
t1.start()
t2.start()
