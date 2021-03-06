![RPi](https://cl.ly/851753b3601b/Raspbian.jpg)  
## _Create new Raspberry-Image.(Opencv/QT5/wiringPi/PythonLib/ENV)_
## 1. How to Create a new image on SD-Card?   
Step1. Download the image.zip file from [Official Edition](https://www.raspberrypi.org/downloads/) && [Other Rpi-Sys Edition](http://downloads.raspberrypi.org/raspbian/images/).  
Step2. unzip the image file into a new .img file.  
`unzip 2019-04-08-raspbian-stretch-full.zip`  
Step3. Insert your TF-Card into your computer(window/Ubuntu) and begin to make new image.    
* If your are a Windows user, Please do like this:  
  1. Download the [SD Format](https://www.sdcard.org/chs/downloads/formatter/) Software to Format the SD-Card.  
  2. Dowload the [Win32DiskImager](https://sourceforge.net/projects/win32diskimager/) software to create a new image in SD-Card.  
  3. Insert your SD-Card and use the [SD Format] format your card.  
  5. Select the correct img file and the SD card you just formated,and create a new image.  
* If your are a Linux user, Please do like this:  
  1. Change directory to the image file's dir.  
  2. Checkout the device mounted just now.[eg:]  
  `mount -ls`  
  `/dev/sdb1 on /mnt/raspberry-rootfs type ext4 (rw,relatime,data=ordered) [rootfs]`  
  3. Unmount the device make it could not be changed by Other User so that we can create the image safely.  
  `umount /dev/sdb1`  
  4. Use the dd CMD to Create the image.  
  `sudo dd bs=4M if=~/raspberry/Reference/2019-04-08-raspbian-stretch-full.img of=/dev/sdb`  
* Here the bash script(mkimg.sh) for Linux User to directly create the image(Notice some change need to be done for your own env):  
```
read -p "Create a new image.Need to Create New Image and already Insert Disk?(yes/no):"  mknewimage
if [ "$mknewimage" = "yes" -o "$mknewimage" = "y" ]
then
    echo "Please Insert you SD-Card Reader into the Ubuntu Mashine to make a new Raspberry Image."
    echo "Mounting TF Card..."
    TFCardMounted=$(mount -ls | grep /dev/sdb)
    if [ "$TFCardMounted" = "" ]
    then
        echo "TFCard mounted failed!Try again."
        exit 1
    fi
    mountpos=${TFCardMounted%% *}
    echo "Mount position is:" $mountpos
    echo "Starting dd 2019-04-08-raspbian-stretch-full.img into tf-card."
    sudo umount $mountpos
    sudo dd bs=4M if=~/raspberry/Reference/2019-04-08-raspbian-stretch-full.img of=/dev/sdb # Need to be change for your own env.
    echo "New image Created Finished."
    echo "Umounting the " $MOUNTPOINT " devices,please waitting..."
    sudo umount $MOUNTPOINT # Checkout if the mount point have been changed after cmd dd operation.
    echo "Creating new image Finished."
fi
```  
After your Finished create the image:  
![Mount -ls](https://cl.ly/5d57f8d58fab/mount-ls.png)
* Reference && Notice:  
R: [Linux命令行烧录树莓派镜像至SD卡](http://shumeipai.nxez.com/2013/12/08/linux-command-line-burn-raspberry-pi-mirror-to-sd-card.html)  
N: If you are using 2019-04-08-raspbian-stretch-full.img to create the system,you need at least 5G Space.  
![Raspbian Size](https://cl.ly/8fa6775312cb/SD_Size.png)
## 2. How to make a new image file by SD-Card Content?  
* Make Image File.  
1. On Window Env.  
We can directly use the [Win32DiskImager](https://sourceforge.net/projects/win32diskimager/) software to Get a new image file from SD-Card.  
![Win32DiskImager](https://cl.ly/a9653065dedc/Win32DiskImager.png)  
The yellow arrow means to Read the image from SD-Card.  
The Black arrow means to Write a new image to the SD-Card.  
2. On Linux Env.  
We just need to Create a shell script(imgmk.sh) so that we could read the image out.  
```
read -p "Make a new image with the software installed!Already Insert Disk?(yes/no):"  mkqtimage
if [ "$mkqtimage" = "yes" -o "$mkqtimage" = "y" ]
then
    bootMountState=$(mount -ls | grep boot | grep /dev/)
    rootfsMountState=$(mount -ls | grep rootfs | grep /dev)
    if [ "$bootMountState" = "" -a "$rootfsMountState" = "" ]
    then
        echo "The RaspberryPi's Image mount failed!"
        echo "Please Manual Operation to mount the image."
        exit 1
    fi
    echo "Mounting is OK! Let's Read the Image from SD-Card.Please waitting..."
    sudo dd bs=4M if=/dev/sdb | gzip > raspbian.img.gz # The image has been compressed.  
    # sudo dd bs=4M if=/dev/sdb of=raspbian.img          # The whole image has been compressed(Big as the SD-Card).  
    echo "Finish Reading image."
fi
```  
The compressed image res:  
![Compressed](https://cl.ly/c57b10cc87f9/compress-image-size.png)  
* Recovery Image-System by Compressed-Img Or Whole-Img:  
1. Compressed-Img: `gunzip --stdout raspbian.img.gz | sudo dd bs=4M of=/dev/sdb`  
2. Whole-Img: `sudo dd bs=4M if=raspbian.img of=/dev/sdb`  
* Reference && Notice:  
R: [官方备份步骤](https://www.raspberrypi.org/documentation/linux/filesystem/backup.md)  
R: [Raspberry-系统备份](https://wuziqingwzq.github.io/raspberrypi/2017/08/15/raspberry-backup.html)  
R: [Linux制作Raspberry最小镜像](https://blog.csdn.net/u013451404/article/details/80552765)  
