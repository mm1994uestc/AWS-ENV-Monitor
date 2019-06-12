import time
import smbus

Device_Address = 0x40
Device_Measure_Humidity = 0xE5
Device_Measure_Temprature = 0xE3
Device_Readcmd = 0xE7
Device_Register = 0xE0

Si7021_Bus = smbus.SMBus(1)

def Si7021_Get_Temprature():
    Si7021_Bus.open(1)
    Si7021_Bus.write_byte(Device_Address,Device_Measure_Temprature)
    time.sleep(0.5)
    Si7021_Bus.write_byte(Device_Address,Device_Readcmd)
    time.sleep(0.5)
    Data = Si7021_Bus.read_i2c_block_data(Device_Address,Device_Register,2)
    Si7021_Bus.close()
    return Data
def Si7021_Get_Humidity():
    Si7021_Bus.open(1)
    Si7021_Bus.write_byte(Device_Address,Device_Measure_Humidity)
    time.sleep(0.5)
    Si7021_Bus.write_byte(Device_Address,Device_Readcmd)
    time.sleep(0.5)
    Data = Si7021_Bus.read_i2c_block_data(Device_Address,Device_Register,2)
    Si7021_Bus.close()
    return Data

#print 'Temp:',Si7021_Get_Temprature()
#print 'Humi:',Si7021_Get_Humidity()