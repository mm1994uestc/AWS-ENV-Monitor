# -*- uft-8 -*-
import time
import socket
import pymysql.cursors

'''
CREATE TABLE `ENV_TABLE` (
       `id`           int(11) NOT NULL AUTO_INCREMENT,
       `timestamp`    int(11) NOT NULL,
       `Temp`         int(11) NOT NULL,
       `Humi`         int(11) NOT NULL,
       `CO2`          int(11) NOT NULL,
       `PH`           int(11) NOT NULL,
       `EC`           int(11) NOT NULL,
       `ControlState` int(11) NOT NULL,
       PRIMARY KEY (`id`)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
   AUTO_INCREMENT=1 ;
'''

abs_path = "/home/pi/nexgen_pro/image_sample_pro/Raspberry_Arduino_Motor_Control/Mysql_Journal.log" # ADD-line

def Journal_log(log,path='?'):
    DefaultPath = "/home/pi/nexgen_pro/image_sample_pro/Raspberry_Arduino_Motor_Control/Mysql_Journal.log"
    if path == '?':
        path = DefaultPath
    Journal = open(path,'a')
    Journal.write(log)
    Journal.close()

def Get_time_str(separator,struct=''):
    if struct == '':
        time_struct_val = time.localtime(time.time())
        return str(time_struct_val.tm_year) + separator + str(time_struct_val.tm_mon) + separator + str(time_struct_val.tm_mday)+ separator + str(time_struct_val.tm_hour) + separator + str(time_struct_val.tm_min) + separator + str(time_struct_val.tm_sec)
    return str(struct.tm_year) + separator + str(struct.tm_mon) + separator + str(struct.tm_mday)+ separator + str(struct.tm_hour) + separator + str(struct.tm_min) + separator + str(struct.tm_sec)

Journal_log(log='Mysql-Save thread Started.(' + Get_time_str(':') + ')\n')

def Insert_LocalDB(data):
# Connect to the database
    try:
        connection = pymysql.connect(host='localhost',user='root',password='',db='Test',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `ENV_TABLE` (`timestamp`, `Temp`, `Humi`, `CO2`, `PH`, `EC`, `ControlState`) VALUES (%d, %d, %d, %d, %d, %d, %d)"
            cursor.execute(sql % (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
        # print('Insert Successful.')
        connection.close()
    except Exception:
        print('The MYSQL database is using by other process,Try again...')
        Journal_log('The MYSQL database is using by other process,Try again...(' + Get_time_str('-') + ')')
        pass

def Get_LocalDB(id):
    try:
        connection = pymysql.connect(host='localhost',user='root',password='',db='Test',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `*` FROM `users` WHERE `id`=%s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            # print(result)
    finally:
        connection.close()

# Connect Socket
S = socket.socket()
host = '192.168.101.121'
port = 5000
S.connect((host, port))
while True:
    # cmd = raw_input('Please enter your cmd:')
    cmd = 'G'
    if cmd == '':
        continue
    # print 'Sending Command!'
    S.sendall(cmd)
    data = S.recv(1024)
    # print data
    if data == 'EXD':
        continue
    data_list = []
    data_str_list = data.split('|')
    for i in range(8):
        data_list.append((int(data_str_list[i])))
        # print data_list[i],' type:',type(data_list[i])
    # print data_list
    Insert_LocalDB(data_list)
    # print 'Insert Successful.'
    time.sleep(2)
'''
    time.sleep(1)
    T = time.localtime(time.time())
    while T.tm_sec != 1:
        T = time.localtime(time.time())
        time.sleep(0.8)
'''
S.close()