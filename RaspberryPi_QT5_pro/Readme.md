# Building Qt 5 on Raspberry Pi  
This is a HOW TO guide for building Qt 5 for the [Raspberry Pi](http://raspberrypi.org/), and building and deploying Qt 5 apps using Qt Creator. This guide will be using Raspbian “Wheezy”, a Debian based distro designed for the Raspberry Pi. This guide also assumes the use of Linux or UNIX on the workstation side.  
Note: Throughout this guide the symbol “$” denotes a command prompt on the host workstation, and “pi$” denotes a command prompt on the target Raspberry Pi.  
# Getting started  
## Downloads  
You will need the following downloads:  
* The latest Raspbian “Wheezy” version of Debian Linux [2013-02-09]  
[http://www.raspberrypi.org/downloads](http://www.raspberrypi.org/downloads).  
* A working toolchain for the Raspberry Pi  
[http://swap.tsmt.eu/gcc-4.7-linaro-rpi-gnueabihf.tbz](http://swap.tsmt.eu/gcc-4.7-linaro-rpi-gnueabihf.tbz).  
* The latest Qt 5 sources [5.0.2]  
[http://qt-project.org/downloads](http://qt-project.org/downloads).  
Please note the user and login for the Linux image. Currently this is user “pi” and password “raspberry”, but this could change in the future.  
## Install a Toolchain  
To build on the Raspberry Pi we need a cross-compile toolchain. The toolchain will contain compilers, linkers and other tools that run on the host workstation but create executables for the target Raspberry Pi.  

For embedded development, one normally uses a vendor-supplied toolchain, but in the case of the Raspberry Pi, there is no official vendor supplied toolchain. There are several generic ARM toolchains that will suffice, however, we have chosen to use the same one the bakeqtpi script uses. This is a Linaro based toolchain for the ARMv6 platform with hard floating-point support. Alternatively, we could have built our own toolchain.  

We will create a working directory to use named “raspberry”. Our first step is to get and install a cross compiling toolchain.  
```
$ mkdir ~/raspberry
$ cd ~/raspberry
$ wget <a href="http://swap.tsmt.eu/gcc-4.7-linaro-rpi-gnueabihf.tbz&#10">http://swap.tsmt.eu/gcc-4.7-linaro-rpi-gnueabihf.tbz&#10</a>;$ tar xfj gcc-4.7-linaro-rpi-gnueabihf.tbz
```  
Since this toolchain is built for 32-bit systems, you will need a set of 32-bit libraries installed if you are on a 64-bit system. On Ubuntu systems, this can be accomplished by installing the ia32-libs package. Unfortunately, this is a deprecated transitional package, with no replacement.  
`$ sudo apt-get install ia32-libs`  
## Development Script  
As a convenience, you can create a setdevenv.sh script in ~/raspberry that can be sourced to set up necessary environment variables.  
```
#!/bin/sh
WORKINGDIRECTORY=$HOME/raspberry
TOOLCHAIN=gcc-4.7-linaro-rpi-gnueabihf
MOUNTPOINT=/mnt/raspberry-rootfs
export PATH=$PATH:$WORKINGDIRECTORY/$TOOLCHAIN/bin
```  
# Prepare the Image  
## Burn and Boot  
Before we can do anything, we need to be able to boot up the Raspberry Pi to a working Raspbian “Wheezy” Linux. We do this by burning a Raspbian image to an SD Card.  
* Extract and rename the image previously downloaded. We rename it to keep track of the image we are working on.   
```
$ unzip 2013-02-09-wheezy-raspbian.zip
  ...
$ mv 2013-02-09-wheezy-raspbian.img raspberry-working-image.img
```  
* Determine what device the SD card reader is. There are various ways to do this, but I prefer looking at the last few lines of dmesg output after inserting the card. In the following case, the device is sdb. Make sure you know the correct device to use with the subsequent dd command, or you could lose all your data.  

Repeat: Make sure you know the correct device to use with the subsequent dd command, or you could *lose all your data*.  
```
$ dmesg
...
[ 2838.088974] sd 7:0:0:0: [<strong>sdb</strong>] No Caching mode page present
[ 2838.088981] sd 7:0:0:0: [<strong>sdb</strong>] Assuming drive cache: write through
[ 2838.088986] sd 7:0:0:0: [<strong>sdb</strong>] Attached SCSI removable disk
```  
* Burn the image. It is advisable to use a smaller card rather than a larger card for this purpose. The minimum size is 2Gig however. Correct for any path and device differences in the following command.  
```
$ sudo dd bs=4M if=raspberry-working-image.img of=/dev/sdb
462+1 records in
462+1 records out
1939865600 bytes (1.9 GB) copied, 404.52 s, 4.8 MB/s
```  
* Remove the SD card and insert it into the Raspberry Pi. Boot the Raspberry Pi. Verify that it boots correctly to the Raspi-config screen.  
* Turn on ssh while you are in this screen, as well as any other options you might desire (keyboard layout, timezone, etc).  
* Exit the Raspi-config screen to a command prompt. Run ifconfig to determine the Raspberry's network address.   
```
pi$ ifconfig
eth0 Link encap:Ethernet HWaddr xx:xx:xx:xx:xx:xx  
     inet addr:<strong>10.0.0.3</strong> Bcast:10.0.0.255  Mask:255.255.255.0
...
```  
* Back on your workstation, ssh into the Raspberry Pi.   
```
$ ssh pi@10.0.0.3
pi@10.0.0.3's password:raspberry
pi$
```  
## Install Packages  
Additional packages will be needed on the Raspberry Pi in order to build Qt 5 and run Qt 5 applications.  

The first step is to update and upgrade the existing packages.  
```
pi$ sudo apt-get update
pi$ sudo apt-get upgrade
```  
Here is a list of the basic packages needed for building and running Qt 5. These are Ubuntu package names, but there should be similar packages on all Linux distros.  
* libfontconfig1-dev  
* libdbus-1-dev  
* libfreetype6-dev  
* libudev-dev  

```
pi$ sudo apt-get install libfontconfig1-dev ...
Setting up libfontconfig1-dev (2.9.0-7.1) ...
...
```  
If you plan on building QWebKit, you'll need the following additional packages.  

* libicu-dev  
* libsqlite3-dev  
* libxslt1-dev  
* libssl-dev  
For multimedia you will need the following optional packages.  

*    libasound2-dev  
*    libavcodec-dev  
*    libavformat-dev  
*    libswscale-dev  
*    libgstreamer0.10-dev  
*    libgstreamer-plugins-base0.10-dev  
*    gstreamer-tools  
*    gstreamer0.10-plugins-good  
*    gstreamer0.10-plugins-bad  

Install the software fot Qt needs:
If you want to install all of them,Please use this command:
`sudo apt-get install libfontconfig1-dev libdbus-1-dev libfreetype6-dev libudev-dev libicu-dev libsqlite3-dev libxslt1-dev libssl-dev libasound2-dev libavcodec-dev libavformat-dev libswscale-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev gstreamer-tools gstreamer0.10-plugins-good gstreamer0.10-plugins-bad`

# Back to the Workstation  
Building software on the Raspberry Pi will be too slow, thus we will need to return to our workstation and use our cross-compile toolchain to perform the remainder of the work.  

A traditional method of cross-platform development is to create a chroot or jail environment to build against. However, since we have a working image of the Raspberry Pi, we can use that instead and it will be much easier. There are also minor fixes we need to make to the image.  
* First, cleanly shutdown the Raspberry Pi.   
`pi$ sudo shutdown -h now`  
* Insert the SD card in the host workstation and copy the card contents back to our working image file. Note that this will create an image the size of the SD card, so make sure you have enough room. Correct for any path and device differences in the following command.  
```
$ sudo dd if=/dev/sdb of=raspberry-working-image.img
7761920+0 records in
7761920+0 records out
3974103040 bytes (4.0 GB) copied, 253.641 s, 15.7 MB/s
```  
* You will need the offset for the Linux image to mount it. If it's not otherwise provided with the download, you can determine it using losetup. There are 512 bytes per sector, so in the example below the offset is 122880 * 512 = 62914560.([Using losetup](https://www.cnblogs.com/uestc-mm/p/11345359.html))   
```
$ sudo /sbin/losetup /dev/loop0 raspberry-working-image.img
$ sudo /sbin/fdisk -l /dev/loop0
...
      Device Boot      Start         End      Blocks   Id  System
/dev/loop0p1            8192      122879       57344    c  W95 FAT32
/dev/loop0p2         <strong>122880</strong>     3788799     1832960   83  Linux
...
$ sudo /sbin/losetup -d /dev/loop0
```  
* Now create a mount point and mount the image:   
```
$ sudo mkdir /mnt/raspberry-rootfs
$ sudo mount -o loop,offset=62914560 \
  raspberry-working-image.img /mnt/raspberry-rootfs
$ ls /mnt/raspberry-rootfs
bin   dev  home  lost+found  mnt  proc  run   selinux  sys  usr
boot  etc  lib   media       opt  root  sbin  srv      tmp  var
```  
*For convenience our setdevenv.sh script sets a mountpoint variable for us, so we can use $MOUNTPOINT instead of the full path.*  
* Clone the cross-compile-tools repo. This contains some useful scripts, including the important fixQualifiedLibraryPaths script.   
```
$ git clone git://gitorious.org/cross-compile-tools/cross-compile-tools.git
$ cd cross-compile-tools
```  
* Apply the fixQualifiedLibraryPaths script. This fixes the symlinks in the mounted image to be relative instead of absolute. The command is: fixQualifiedLibraryPaths target-rootfs path-to-target-toolchain-compiler  
```
$ sudo ./fixQualifiedLibraryPaths $MOUNTPOINT \
  ~/raspberry/gcc-4.7-linaro-rpi-gnueabihf/bin/arm-linux-gnueabihf-gcc
```  
* Finally we need to make some miscellaneous fixes.   
```
$ sudo ln -s \
  $MOUNTPOINT/opt/vc/include/interface/vmcs_host/linux/vchost_config.h \
  $MOUNTPOINT/opt/vc/include/interface/vmcs_host/vchost_config.h
```  
# Building Qt 5  
Building Qt 5 will now proceed normally in much the same way as building Qt 5 for the desktop. There are a few minor differences however, such as applying a few patches and providing the appropriate configure options.  
## Patching Qt 5  

