import os
import sys
import json
import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import random, time

from Sensor_Protocol.Si7021 import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

fans_pin = 17
GPIO.setup(fans_pin,GPIO.OUT)


# A random programmatic shadow client ID.
SHADOW_CLIENT = "myShadowClient"

# The unique hostname that &IoT; generated for 
# this device.
HOST_NAME = "a25lgmpslpm915.ats.iot.cn-north-1.amazonaws.com.cn"

# The relative path to the correct root CA file for &IoT;, 
# which you have already saved onto this device.
ROOT_CA = "AmazonRootCA1.pem"

# The relative path to your private key file that 
# &IoT; generated for this device, which you 
# have already saved onto this device.
PRIVATE_KEY = "ccc6620484-private.pem.key"

# The relative path to your certificate file that 
# &IoT; generated for this device, which you 
# have already saved onto this device.
CERT_FILE = "ccc6620484-certificate.pem.crt.txt" # The file have no ".txt" subfix here.

# A programmatic shadow handler name prefix.
SHADOW_HANDLER = "nexgen-ai-Demo001"

# Automatically called whenever the shadow is updated.
def myShadowUpdateCallback(payload, responseStatus, token):
    print()
    print('UPDATE: $aws/things/' + SHADOW_HANDLER + '/shadow/update/#')
    print("payload = " + payload)
    print("responseStatus = " + responseStatus)
    print("token = " + token)

# Create, configure, and connect a shadow client.
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
myShadowClient.configureEndpoint(HOST_NAME, 8883)
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY,CERT_FILE)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()

# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(SHADOW_HANDLER, True)

def get_CPU_Temprature():
    res = os.popen('vcgencmd measure_temp').readline()
    return res.replace("temp=","").replace("'C\n","")

json_data = [{'default':'ENV-Status','state':{'reported':{'nexgen-time':None,'ENV-Temp':None,'ENV-RH':None,'ENV-Fans':'OFF','CPU-Temp':None,'CPU-Fans':'OFF'}},'notify':False,'email':None}]
# '{"default":"Trigger Test","state":{"reported":{"Temprature":"High"}},"email":"Temprature is High!"}'
# Keep generating random test data until this script 
# stops running.
# To stop running this script, press Ctrl+C.
week_env_temp = []
week_cpu_temp = []
week_env_rh = []

while True:
    # Generate random True or False test data to represent
    # okay or low moisture levels, respectively.
    date = time.localtime(time.time())
    date_str = str(date.tm_year) + ':' + str(date.tm_mon) + ':' + str(date.tm_mday) + ':' + str(date.tm_hour) + ':' + \
            str(date.tm_min) + ':' + str(date.tm_sec)
    print 'Current time:',date_str
    
    CPU_Temp = get_CPU_Temprature()
    CPU_Temp_val = float(CPU_Temp)

    ENV_Temp = Si7021_Get_Temprature()
    ENV_Temp_val = 175.72*((ENV_Temp[0] << 8) + ENV_Temp[1]) / 65536 - 46.85

    ENV_RH = Si7021_Get_Humidity()
    ENV_RH_val = 125*((ENV_RH[0] << 8) + ENV_RH[1]) / 65536 - 6

    print ENV_Temp_val,ENV_RH_val,CPU_Temp_val

    json_data[0]['state']['reported']['nexgen-time'] = date_str
    json_data[0]['state']['reported']['ENV-Temp'] = str(ENV_Temp_val)
    json_data[0]['state']['reported']['ENV-RH'] = str(ENV_RH_val)+"%"
    json_data[0]['state']['reported']['CPU-Temp'] = str(CPU_Temp_val)
    
    # mesg = json.dumps(json_data)
    print 'Send the mseg to AWS!'
    if CPU_Temp_val > 60 or ENV_RH_val > 90 or ENV_Temp_val > 30:
        print 'notify on.'
        json_data[0]['notify'] = True
        json_data[0]['email'] = 'Fans ON!'+'\nTemp:'+str(ENV_Temp_val)+'\nRH:'+str(ENV_RH_val)+'\nCPU_Temp:'+str(CPU_Temp_val)
    else:
        print 'notify off.'
        json_data[0]['notify'] = False
        json_data[0]['email'] = None

    mesg = json.dumps(json_data[0])
    myDeviceShadow.shadowUpdate(mesg ,myShadowUpdateCallback, 5)

    # Wait for this test value to be added.
    time.sleep(60)



