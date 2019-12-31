import socket
import json
from parking import Car, ParkingLotManage
import threading
import time

parking = ParkingLotManage(100)


def receive():
    ip_port = ('127.0.0.1', 8000)
    back_log = 5
    buffer_size = 1024
    ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ser.bind(ip_port)
    ser.listen(back_log)
    print('开始监听')
    while True:
        con, addr = ser.accept()
        print('服务器连接成功')
        while True:
            try:
                msg = con.recv(buffer_size)
                if msg.decode('utf-8') == '1':
                    con.close()
                dics = msg.decode('utf-8')
                dic = json.loads(dics)
                print('接受成功')
                print(dic)
                print('')
                t = threading.Thread(target=runing, args=(dic,))
                t.start()
                con.send(json.dumps(parking.car_num_list).encode('utf-8'))

            except Exception as e:
                print(e)
                break


def runing(car_dict):
    if isinstance(car_dict, dict):
        car = Car(car_dict['车牌号'], car_dict['颜色'], car_dict['类型'])
        parking.car_in(car)
        print('')
    elif isinstance(car_dict, str):
        parking.car_out(car_dict)
        print('')


def insert_sql():
    while True:
        time.sleep(60 * 5)
        parking.sql_insert()
        print('')


receive()
t1 = threading.Thread(target=insert_sql)
t1.start()
