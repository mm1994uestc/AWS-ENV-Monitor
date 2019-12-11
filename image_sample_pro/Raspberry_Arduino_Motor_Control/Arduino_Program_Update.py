import boto3
import time
import sys
import os

def Serial_Get():
    USB_dev = ''
    find_count = 0
    while USB_dev == '':
        dev_list = os.listdir('/dev/')
        for dev in dev_list:
            if 'USB' in dev:
                USB_dev = dev
                print 'USB device founded:',USB_dev
                find_count = 0
                break
        find_count += 1
        if find_count >= 30:
            print 'Restart the Arduino Power supply by raspberry\'s GPIO Directly OR Mannually Operate.'
            find_count = 0
        time.sleep(1)
    serial_dev = '/dev/' +  USB_dev
    return serial_dev

print 'Finding USB-Device...'
USB_Device = Serial_Get()
print 'USB Device:',USB_Device

print 'Downloading BIN-FILE...'
s3 = boto3.resource('s3')

with open('Raspberry_Arduino_Motor_Control.ino.hex','wb') as data:
    s3.meta.client.download_fileobj('arduino-program-update','Raspberry_Arduino_Motor_Control.ino.hex',data)

print 'BIN FileName:','Raspberry_Arduino_Motor_Control.ino.hex'

print 'Flashing Arduino...'
time.sleep(1)


if sys.argv[1] in 'atmega328p':
    print "The Device is: atmega328p."
    print     "avrdude -C avrdude.conf -v -v -v -v -p m328p -c arduino -P %s -b 115200 -D -U flash:w:Raspberry_Arduino_Motor_Control.ino.hex:i"%USB_Device
    os.system('avrdude -C avrdude.conf -v -v -v -v -p m328p -c arduino -P %s -b 115200 -D -U flash:w:Raspberry_Arduino_Motor_Control.ino.hex:i'%USB_Device)
if sys.argv[1] in 'atmega2560':
    print "The Device is: atmega2560."
    print     "avrdude -C avrdude.conf -v -v -v -v -patmega2560 -cwiring -P %s -b115200 -D -Uflash:w:Raspberry_Arduino_Motor_Control.ino.hex:i"%USB_Device
    os.system('avrdude -C avrdude.conf -v -v -v -v -patmega2560 -cwiring -P %s -b115200 -D -Uflash:w:Raspberry_Arduino_Motor_Control.ino.hex:i'%USB_Device)
print 'Download Finished!'
