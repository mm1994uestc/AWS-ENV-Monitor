import boto3
import time
import sys
import os

s3 = boto3.resource('s3')

with open('Raspberry_Arduino_Motor_Control.ino.hex','wb') as data:
    s3.meta.client.download_fileobj('arduino-program-update','Raspberry_Arduino_Motor_Control.ino.hex',data)

time.sleep(1)
print 'Downloading...'
if sys.argv[1] in 'atmega328p':
    print "The Device is: atmega328p."
    os.system('avrdude -C avrdude.conf -v -v -v -v -p m328p -c arduino -P /dev/ttyUSB0 -b 115200 -D -U flash:w:Raspberry_Arduino_Motor_Control.ino.hex:i')
if sys.argv[1] in 'atmega2560':
    print "The Device is: atmega2560."
    os.system('avrdude -C avrdude.conf -v -v -v -v -patmega2560 -cwiring -P /dev/ttyUSB0 -b115200 -D -Uflash:w:Raspberry_Arduino_Motor_Control.ino.hex:i')
print 'Download Finished!'
