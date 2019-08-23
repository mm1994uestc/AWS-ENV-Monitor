import os
import time
import sys

USB_dev = ''
dev_list = os.listdir('/dev/')
for dev in dev_list:
    if 'USB' in dev:
        USB_dev = dev
if USB_dev == '':
    print 'No USB device found!Restart the USB Device auto.'
serial_port = '/dev/' +  USB_dev
print serial_port
