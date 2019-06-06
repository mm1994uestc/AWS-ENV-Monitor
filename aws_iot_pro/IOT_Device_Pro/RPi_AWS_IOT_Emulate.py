import os
import sys
import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import random, time

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
  print('UPDATE: $aws/things/' + SHADOW_HANDLER + 
    '/shadow/update/#')
  print("payload = " + payload)
  print("responseStatus = " + responseStatus)
  print("token = " + token)

# Create, configure, and connect a shadow client.
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
myShadowClient.configureEndpoint(HOST_NAME, 8883)
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY,
  CERT_FILE)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()

# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(
  SHADOW_HANDLER, True)

def get_CPU_Temprature():
    res = os.popen('vcgencmd measure_temp').readline()
    return res.replace("temp=","").replace("'C\n","")

# Keep generating random test data until this script 
# stops running.
# To stop running this script, press Ctrl+C.
while True:
  # Generate random True or False test data to represent
  # okay or low moisture levels, respectively.
  Temp = get_CPU_Temprature()
  Temp_val = float(Temp)


  if Temp_val > 58.0:
    myDeviceShadow.shadowUpdate(
            '{"default":"Trigger Test","state":{"reported":{"Temprature":"High"}},"email":"Temprature is High!"}',
      myShadowUpdateCallback, 5)
    GPIO.output(fans_pin,False)
  elif Temp_val < 53.0:
    myDeviceShadow.shadowUpdate(
            '{"state":{"reported":{"Temprature":"low"}}}',
      myShadowUpdateCallback, 5)
    GPIO.output(fans_pin,True)


  # Wait for this test value to be added.
  time.sleep(20)


