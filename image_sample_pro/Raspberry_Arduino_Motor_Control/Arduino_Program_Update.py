import boto3
import time
import os
s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print bucket.name

with open('Raspberry_Arduino_Motor_Control.ino.hex','wb') as data:
    s3.meta.client.download_fileobj('arduino-program-update','Raspberry_Arduino_Motor_Control.ino.hex',data)

time.sleep(1)
print 'Downloading...'
os.system('avrdude -C avrdude.conf -v -v -v -v -p m328p -c arduino -P /dev/ttyUSB0 -b 57600 -D -U flash:w:Raspberry_Arduino_Motor_Control.ino.hex:i')
print 'Download Finished!'
