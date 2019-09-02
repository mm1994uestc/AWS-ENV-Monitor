#!/bin/bash

Time=$(date "+%Y%m%d%H%M%S")
echo "####"$Time"####" >> "USB-DEVICE.txt"
USB_Dev_ID=0
while [ $USB_Dev_ID -ne "10" ];do
    USB_Dev="/dev/ttyUSB"$USB_Dev_ID
    echo $USB_Dev
    if [ -e $USB_Dev ];then
        USB_Dev_INFO=`ls -al /sys/class/tty/ttyUSB$USB_Dev_ID`
        USB_Dev_TEMP=${USB_Dev_INFO##*/1-1.}
        USB_Dev_SIMP=${USB_Dev_TEMP%/*}
        pos_start=`expr index "$USB_Dev_TEMP" ":"`
        let "pos_start-=2"
        echo ${USB_Dev_TEMP:$pos_start:13} >> "USB-DEVICE.txt"
        echo $USB_Dev_INFO
    fi
    let "USB_Dev_ID+=1"
done
