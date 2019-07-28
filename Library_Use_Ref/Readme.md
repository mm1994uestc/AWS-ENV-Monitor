# How to use the files under this folder?
## 1. rpi2_py_usart_co2.py
The file is used to control the CO2 Sensor with the raspiberry zero directly.  
When you need to Use this file,you should firstly set up the PL011 usart device.  
Now let's setting the PL011 usart and make it mapping to the GPIO pins(GPIO14-->TXD && GPIO15-->RXD).  
**Step1:** Use Command to show whether the usart device is prepared? `sudo ls -al /dev/tty*`  
![dev](https://share.getcloudapp.com/2Nu2KxRN)
The ttyAMA0 is PL001 UART and the ttyUSB0 is the usb-usart device.  
**Step2:** Modify the cmdline.txt with vim. `sudo vim /boot/cmdline.txt`  
The content of cmdline.txt before we midify it:
```
dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=PARTUUID=a05c3c8f-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```
After i modify it(Delet all the console relative content!):
```
dwc_otg.lpm_enable=0 root=PARTUUID=a05c3c8f-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```
