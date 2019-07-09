# -*- coding: cp936 -*-
import os
import sys
import glob
import time
import sys

mswindows = (sys.platform == "win32")
linux = (sys.platform == "linux2" or sys.platform == "linux")

Upload_tm = time.localtime(time.time())
Current_date = str(Upload_tm.tm_year) + '-' + str(Upload_tm.tm_mon) + '-' + str(Upload_tm.tm_mday) + '-' + str(Upload_tm.tm_hour) + '-' + str(Upload_tm.tm_min) + '-' + str(Upload_tm.tm_sec)

folder_obj = ['A1','A2','A3','A4','A5','A6','A7','A8','B1','B2','B3','B4','B5','B6','B7','B8',\
        'C1','C2','C3','C4','C5','C6','C7','C8','D1','D2','D3','D4','D5','D6','D7','D8']

if mswindows:
    print('Platform:Windows.')
    print("Start deleting images:",Current_date)
    for folder_name in folder_obj:
        Find_image_path = '.\\'+folder_name+'\\' + '*.jpg'
        image_dataset = glob.glob(Find_image_path)
        image_n = len(image_dataset)
        for i in range(image_n):
            image_name = image_dataset[i][5:]
            print("Deleting " + image_name + "...")
            os.system('del ' + image_dataset[i])
    print("Finish Deleting Images.")

if linux:
    print('Platform:Linux.')
    print("Start deleting images:",Current_date)
    for folder_name in folder_obj:
        Find_image_path = './'+folder_name+'/*.jpg'
        image_dataset = glob.glob(Find_image_path)
        image_n = len(image_dataset)
        for i in range(image_n):
            image_name = image_dataset[i][5:]
            print("Deleting " + image_name + "...")
            os.system('rm -f ' + image_dataset[i])
    print("Finish Deleting Images.")
