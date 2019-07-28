import serial
import time
import os

dev = "/dev/ttyAMA0"
baud = 9600

def rpi2_usart_open(device,baudrate):
    return serial.Serial(device,baudrate)
def rpi2_usart_send(serial,data):
    # serial.flushOutput()
    serial.write(data)
    # serial.flushOutput()
def rpi2_usart_recv(serial,lenght):
    buffers = ''
    while True:
        FIFO_len = serial.inWaiting()
        # print "Waiting data:",FIFO_len
        if lenght <= FIFO_len:
            buffers = serial.read(FIFO_len)
            # serial.flushInput()
            break
    return buffers
ser = rpi2_usart_open(dev,baud)
send_data = chr(254)+chr(4)+chr(0)+chr(3)+chr(0)+chr(1)+chr(213)+chr(197)
buf = ''
while True:
    print "Sending data:",
    for i in range(8):
        print ord(send_data[i]),
    print ' '
    rpi2_usart_send(ser,send_data)
    print "Recieve data:",
    buf = rpi2_usart_recv(ser,7)
    for i in range(7):
        print ord(buf[i]),
    print ' '

    H_Bits = ord(buf[3])
    L_Bits = ord(buf[4])
    H_Bits_H = H_Bits>>4
    H_Bits_L = H_Bits&0x0F
    L_Bits_H = L_Bits>>4
    L_Bits_L = L_Bits&0x0F

    print H_Bits,',',H_Bits>>4,',',H_Bits&0x0F
    print L_Bits,',',L_Bits>>4,',',L_Bits&0x0F
    
    CO2_PPM = H_Bits_H*4096 + H_Bits_L*256 + L_Bits_H*16 + L_Bits_L
    print "CO2-Value:",CO2_PPM
    time.sleep(2)
