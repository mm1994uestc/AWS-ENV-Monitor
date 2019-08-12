# How to Create a new image file for Raspberry with some usefull Software and the Enviroment.  
## How to Create a new image on SD-Card?   
Step1. Download the image.zip file from [here](https://www.raspberrypi.org/downloads/).  
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
  ```
  mount -ls
  /dev/sdb1 on /mnt/raspberry-rootfs type ext4 (rw,relatime,data=ordered) [rootfs]
  ```  
  3. Unmount the device make it could not be changed by Other User so that we can create the image safely. `umount /dev/sdb1`  
  4. Use the dd CMD to Create the image.  
  `sudo dd bs=4M if=~/raspberry/Reference/2019-04-08-raspbian-stretch-full.img of=/dev/sdb`  
* Here the bash script(mkimg.sh) for Linux User to directly create the image(Notice some change need to be done for your own env):  
```
echo "############################################### Step-Make New Image For Disk ############################"
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
## How to make a new image file by SD-Card Content?  
1. On Window Env.  
We can directly use the [Win32DiskImager](https://sourceforge.net/projects/win32diskimager/) software to Get a new image file from SD-Card.  
The yellow arrow means to Read the image from SD-Card.  
The Black arrow means to Write a new image to the SD-Card.  
2. On Linux Env.
