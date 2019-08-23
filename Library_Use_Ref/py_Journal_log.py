import os
import sys

def Journal_log(log,path='?'):
    DefaultPath = "/home/pi/nexgen_pro/image_sample_pro/Raspberry_Arduino_Motor_Control/Test_Journal.log"
    if path == '?':
        path = DefaultPath
    Journal = open(path,'a')
    Journal.write(log)
    Journal.close()

Journal_log(log='hahahah')
Journal_log(log='dsada',path='/home/pi/Test_Journal.log')
