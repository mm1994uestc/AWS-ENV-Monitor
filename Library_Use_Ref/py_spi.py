import os
import sys
import time
import spidev

# open(Bus,Device)  ===>  /dev/spidev<Bus>.<Device>
spi_dev = spidev.SpiDev()
spi_dev.open(0,1)
to_send = [0x01,0x02,0x03]

spi_dev.mode = 0b01
spi_dev.no_cs = True
spi_dev.max_speed_hz = 5000
spi_dev.xfer(to_send)

Data_Recv = spi_dev.readbytes(3)
Data_Send = [1,2,3,4]
spi_dev.writebytes(Data_Send)

print Data_Recv