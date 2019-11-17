#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import threading
import tkinter as tk
import pymysql.cursors

window = tk.Tk()
window.title('Nexgen UI')
window.geometry('1024x600')

Lable_W = 13
val_W = 15
Units={'temp':' (unit:degrees)','humi':' (unit:percent)','co2':' (unit:ppm)','ph':' (unit:PH)','ec':' (unit:TDS)'}

label_val_div = tk.Canvas(window,bg='blue',height=200,width=6).place(x=140,y=10,anchor='nw')

tempval = tk.StringVar()
tempval.set('25'+Units['temp'])
Temp_label = tk.Label(window,text='Tempratue:',bg='green',font=('Arial',15),width=Lable_W,anchor=tk.W,height=2,padx=0,justify=tk.LEFT).place(x=10,y=10,anchor='nw')
Temp_val = tk.Label(window,textvariable=tempval,font=('Arial',15),width=val_W,height=2,padx=0,justify=tk.LEFT).place(x=170,y=10,anchor='nw')

humival = tk.StringVar()
humival.set('65'+Units['humi'])
Humi_label = tk.Label(window,text='Humidity:',bg='green',font=('Arial',15),width=Lable_W,anchor=tk.W,height=2,padx=0,justify=tk.LEFT).place(x=10,y=50,anchor='nw')
Humi_val = tk.Label(window,textvariable=humival,font=('Arial',15),width=val_W,height=2,padx=0,justify=tk.LEFT).place(x=170,y=50,anchor='nw')

co2val = tk.StringVar()
co2val.set('888'+Units['co2'])
CO2_label = tk.Label(window,text='CO2 Potency:',bg='green',font=('Arial',15),width=Lable_W,anchor=tk.W,height=2,padx=0,justify=tk.LEFT).place(x=10,y=90,anchor='nw')
CO2_val = tk.Label(window,textvariable=co2val,font=('Arial',15),width=val_W,height=2,padx=0,justify=tk.LEFT).place(x=170,y=90,anchor='nw')

phval = tk.StringVar()
phval.set('6'+Units['ph'])
PH_label = tk.Label(window,text='PH Value:',bg='green',font=('Arial',15),width=Lable_W,anchor=tk.W,height=2,padx=0,justify=tk.LEFT).place(x=10,y=130,anchor='nw')
PH_val = tk.Label(window,textvariable=phval,font=('Arial',15),width=val_W,height=2,padx=0,justify=tk.LEFT).place(x=170,y=130,anchor='nw')

ecval = tk.StringVar()
ecval.set('1000'+Units['ec'])
EC_label = tk.Label(window,text='EC Value:',bg='green',font=('Arial',15),width=Lable_W,anchor=tk.W,height=2,padx=0,justify=tk.LEFT).place(x=10,y=170,anchor='nw')
EC_val = tk.Label(window,textvariable=ecval,font=('Arial',15),width=val_W,anchor=tk.W,height=2,padx=0,justify=tk.LEFT).place(x=170,y=170,anchor='nw')

def Get_LocalDB_NewData():
    try:
        connection = pymysql.connect(host='localhost',user='root',password='',db='Test',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT MAX(id) FROM ENV_TABLE"
            cursor.execute(sql)
            id = cursor.fetchone()
            id_val = id['MAX(id)']
            print('Current MAX-ID:',id,type(id),id_val,type(id_val))
            sql = "SELECT * FROM ENV_TABLE WHERE id=" + str(id_val)
            print(sql)
            cursor.execute(sql)
            result = cursor.fetchone()
            print('Current Res:',result)
        connection.close()
        return result
    except Exception:
        print('The MYSQL database is using by other process,Try again...')
        pass

ENV_val = ''
def timer_base():
    global Units,co2val
    ENV_val = Get_LocalDB_NewData()
    print('ENV_val:',ENV_val,type(ENV_val))
    co2val.set(str(ENV_val['CO2'])+Units['co2'])
    timer = threading.Timer(1,timer_base)
    timer.start()

timer = threading.Timer(1,timer_base)
timer.start()

window.mainloop()
