from parking import Car, ParkingLotManage
import random
import time
import threading


class Running:
    parking = ParkingLotManage(100)
    car_list = parking.car_num_list

    def running(self):
        # 车进入停车场
        colors = ['black', 'white', 'yellow', 'blue', 'red']
        styles = ['SUV', '宝马', '奔驰', '小型轿车', '越野', '大众', '奥迪', '跑车', '货车', '现代']
        letter = [chr(i) for i in range(65, 91)]
        while True:
            time.sleep(random.randint(1, 10) * 10)
            car = [f'京{random.choice(letter)}{random.randint(1000, 9999)}', random.choice(colors), random.choice(styles)]
            car = Car(car[0], car[1], car[2])
            self.parking.car_in(car)
            print('')

    def leaving(self):
        while True:
            if not self.car_list:
                continue
            time.sleep(random.randint(10, 20) * 10)
            car = random.choice(self.car_list)
            self.parking.car_out(car)
            print('')

    def insert_sql(self):
        while True:
            time.sleep(60 * 10)
            self.parking.sql_insert()
            print('')



def start():
    run = Running()
    # 线程一 进入停车场
    t1 = threading.Thread(target=run.running)

    # 线程二 离开停车场
    t2 = threading.Thread(target=run.leaving)

    # 线程三 定时写入数据库
    t3 = threading.Thread(target=run.insert_sql)

    t1.start()
    t2.start()
    t3.start()


start()



