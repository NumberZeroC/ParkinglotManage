import datetime
import random
import time
import pymysql


class Car:
    def __init__(self, number, color, style):
        self.num = number
        self.color = color
        self.style = style
        self.time_in = None
        self.time_out = None

    def car_in(self):
        self.time_in = datetime.datetime.now()
        return self.time_in

    def car_out(self):
        self.time_out = datetime.datetime.now()
        return self.time_out

    def parking_free(self):
        time = self.time_out - self.time_in
        return time


class ParkingLotManage:

    def __init__(self, count):
        self.count = [i + 1 for i in range(count)]     # 车位列表
        self.car_num_list = []                         # 存放汽车车牌号list
        self.cars_infor = {}                           # 存放汽车信息dict   初始值为car实例，离开时为car信息
        self.connect = None

    def car_in(self, car):
        if not self.count:
            print('停车场已满')
            return
        if not isinstance(car, Car):
            raise '{} is not class Car'.format(car)
        if car.num not in self.car_num_list:
            self.car_num_list.append(car.num)
            car.time_in = datetime.datetime.now()
            car.time_out = None
            space_num = self.count.pop(random.randint(0, len(self.count)-1))
            setattr(car, 'space_num', space_num)

            self.cars_infor[car.num] = car
            print('车牌号：{}停入{}号车位, 时间：{}'.format(
                car.num, space_num, car.time_in))
            print('停车场还有{}个空车位'.format(len(self.count)))

        else:
            print('车已存在')

    def car_out(self, car):
        if isinstance(car, str):
            car = self.cars_infor[car]
        self.count.append(car.space_num)
        self.car_num_list.remove(car.num)
        print(f'汽车{car.num}离开停车场,时间{car.time_out}')
        print(f'停车场还有{len(self.count)}个空车位')
        fee = self.parking_fee(car)
        setattr(car, 'fee', fee)
        print(f'计费：{fee}')
        lists = [car.num, car.color, car.style, car.time_in, car.time_out, car.time, car.space_num, car.fee]
        self.cars_infor[car.num] = lists
        print(lists)

    def parking_fee(self, car):
        """ 停车费 """
        time_out = datetime.datetime.now()
        car.time_out = time_out
        time_in = car.time_in
        time = time_out - time_in
        print('汽车：{} 在停车场停留时间：{}'.format(car.num, time))
        seconds = time.seconds
        fee = int(seconds) * 0.01
        setattr(car, 'time', time)
        car.time_in = car.time_in.strftime('%Y-%m-%d %H:%M:%S')
        car.time_out = car.time_out.strftime('%Y-%m-%d %H:%M:%S')
        times = str(car.time)
        car.time = times.split('.')[0]
        return fee

    def query_car(self, car):
        """ 查询汽车进入停车场记录 """
        num = car.num
        if num not in self.car_num_list:
            print('汽车{} 现在不在号车位'.format(num))
            if self.cars_infor.get(num, None):
                print('汽车{}在停车场的时间段是{}-{}'.format(num, car.time_in, car.time_out))
            else:
                print('没有车牌号{}进入停车场的信息'.format(num))
        else:
            print('汽车{}于{}停在{}号车位'.format(num, car.time_in, car.space_num))

    def sql_connect(self):
        connect = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='password',
            db='parkinglot'
        )
        if connect:
            print('连接数据库成功')
            self.connect = connect
            return self.connect

    def create_table(self):
        if not self.connect:
            self.sql_connect()
        connect = self.connect
        cursor = connect.cursor()
        sql = '''CREATE TABLE car_info(
              number CHAR(20) NOT NULL PRIMARY KEY,
              color CHAR(10),
              style CHAR(10),
              date_in DATETIME,
              date_ut DATETIME
              );
              '''
        try:
            cursor.execute(sql)
            connect.commit()
        except Exception as ex:
            print(ex)

    def sql_insert(self):
        informations = self.cars_infor
        insert = {}
        for key in informations.keys():
            value = informations[key]
            if isinstance(value, list):
                insert[key] = value

        if not insert:
            print('暂无可写入数据')
            return

        print(f'有{len(insert)}条记录待写入数据库')
        if not self.connect:
            self.sql_connect()
        connect = self.connect
        cursor = connect.cursor()
        sql = """
            INSERT INTO car_info (number,color,style,date_in,date_ut,time,space,fee)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """
        flag = True
        try:
            for lis in insert.values():
                cursor.execute(sql, lis)
            connect.commit()
        except Exception as ex:
            print(ex)
            connect.rollback()
            flag = False
        if flag:
            print(f'{len(insert)}条数据写入数据库完成')
        else:
            print(f'写入数据库失败')

    def sql_select(self, car_num):
        if not self.connect:
            self.sql_connect()
        connect = self.connect
        cursor = connect.cursor()
        sql = f"select * from car_info where number='{car_num}';"
        cursor.execute(sql)
        data = cursor.fetchall()
        return data

    def test(self):
        connect = self.sql_connect()
        cursor = connect.cursor()
        list = ('F6688', 'black', 'SUV', '2019-12-06 10:47:32', '2019-12-06 10:47:37', '0:00:05', 100, 0.05)

        sql = "INSERT INTO car_info(number,color,style,date_in,date_ut,time,space,fee) " \
              "VALUES('%s','%s','%s','%s','%s','%s',%d,%.2f)"%(
        list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7]
        )
        # cursor.execute(sql)

        sql = "INSERT INTO car_info(number,color,style,date_in,date_ut,time,space,fee) " \
              "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, list)

        connect.commit()
        print('插入成功')

        connect.close()


if __name__ == '__main__':
    a = Car('888', 'black', 'SUV')
    print(isinstance(a, Car))
    parkinglot = ParkingLotManage(100)
    parkinglot.car_in(a)
    time.sleep(5)
    parkinglot.car_out('888')
    parkinglot.sql_insert()



