# How to use the files under this folder?
## 1. rpi2_py_usart_co2.py
The file is used to control the CO2 Sensor with the raspiberry zero directly.  
When you need to Use this file,you should firstly set up the PL011 usart device.  
Now let's setting the PL011 usart and make it mapping to the GPIO pins(GPIO14-->TXD && GPIO15-->RXD).  
**Step1:** Use Command to show whether the usart device is prepared?  
`sudo ls -al /dev/tty*`  
![dev](https://cl.ly/f9c2cfcae3c3/dev-tty.PNG)  
The ttyAMA0 is PL001 UART and the ttyUSB0 is the usb-usart device.  
**Step2:** Modify the cmdline.txt with vim.  
`sudo vim /boot/cmdline.txt`  
The content of cmdline.txt before we midify it:  
```
dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=PARTUUID=a05c3c8f-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```  
After i modify it(Delet all the console relative content!):  
```
dwc_otg.lpm_enable=0 root=PARTUUID=a05c3c8f-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```  
**Step3:** Disable the bluetooth.  
`sudo systemctl disable hciuart`  
Modify the content of config.txt file:  
`sudo nano /boot/config.txt`  
Add the line1: `dtoverlay=pi3-disable-bt`  
Add the line2: `enable_uart=1`  
**Step4:** Reboot Raspberry Zero W.  
`sudo shutdown -r now`  
## 2. Si7021.py
The Si7021.py file use the SMBus to communicate with the Sensor to get temprature && humidity values.  
The SMBus is similar with IIC protocal,we can use SMBus instead of IIC. How to Using SMBus?  
**Step1:** Install SMBus. [Read The Document](https://pypi.org/project/smbus2/)  
`pip install smbus2`  OR  `pip install smbus`  
**Step2:** Run the py's script Code.  
`python Si7021.py`  
## 3. Fans_Control.py
The Fans_Control.py file maintainly used to monitor the temprature of CPU and Control the Fans's Power Supply.If temp is High,Fans is ON.  
**Step1:** Install the GPIO Control Python'lib.  
`sudo pip install rpi.gpio`  
**Step2:** Read the temp of CPU.  
`temp_tmp = os.popen('vcgencmd measure_temp').readline()`  
**Step3:** Run the py's file.  
`python Fans_Control.py`  
## 4. wiringPi_Test.c  
This C file is used to show How to programming raspberry by C Code.Acturely,we should programming using the c file,also the Makefile is used to compile the C file into execution file.Just need to insert the CMD in the CMDLine-Terminal,and get the execution file.And then execute the exe's file like this: $>./main  
**Step1:** Install the wiringPi C Library. [Reference](https://www.cnblogs.com/uestc-mm/p/6290521.html)  
**Step2:** Programming and Compiling the C Code.  
**Step3:** Run the execution file.
## 5. py_opencv.py && py_camera.py  
The two file is Used to test whether the opencv library is install successfully and whether the Camera resource is OK?  
If those two file can be successfully been executed,that means the Opencv and Camera is OK.  
**Step1:** Install the Opencv Library on Raspberry.  [Install Opencv](https://www.cnblogs.com/uestc-mm/p/7338244.html)  
**Step2:** Enable the Raspberry Camera.  [Enable Camera](https://www.cnblogs.com/uestc-mm/p/7587783.html)
