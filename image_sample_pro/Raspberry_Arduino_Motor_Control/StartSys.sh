#!/bin/bash
#set -x
a="$(ps -aux | grep Raspberry | grep -v 'grep')"
b="$(ps -aux | grep lighttpd  | grep -v 'grep')"
c="$(ps -aux | grep MysqlSave | grep -v 'grep')"
d="$(ps -aux | grep main.py   | grep -v 'grep')"

if [ -z "$a" -o -z "$c" -o -z "$d" ] ; then
	echo 'Need to restart Python Serial...'
	# /etc/init.d/cgminer.sh restart
	sudo killall -9 python2
	sudo killall -9 python3.5
	
	cd /home/pi/nexgen_pro/image_sample_pro/Raspberry_Arduino_Motor_Control/
	echo 'Starting ImageSample Process...'
	nohup sudo python2 Raspberry_ttyAMA0_Arduino_Serial3_USBImageSample.py > ImageSample.err 2>&1 &
	
	sleep 32
	
	# echo 'Starting lighttp WebServer...'
	# sudo /usr/local/src/lighttpd/sbin/lighttpd -f /usr/local/src/lighttpd/config/lighttpd.conf &
	echo 'Starting MysqlSave Process...'
	nohup python2 Sys_Status_MysqlSave.py > Mysql.err 2>&1 &
	
	sleep 2
	
	echo 'Starting Tkinter Process...'
	# export DISPLAY=:0
	cd /home/pi/nexgen_pro/Tkinter_UI/
	nohup python3.5 main.py > Tkinter.err 2>&1 &
fi

if [ -z "$b" ] ; then
	echo 'Need to restart Lighttp...'
	sudo killall -9 lighttpd
	echo 'Starting lighttp WebServer...'
	sudo /usr/local/src/lighttpd/sbin/lighttpd -f /usr/local/src/lighttpd/config/lighttpd.conf &
fi

echo 'Finished.'

exit 0

# Comments
:<<!
cd /home/pi/nexgen_pro/image_sample_pro/Raspberry_Arduino_Motor_Control/
echo 'Starting ImageSample Process...'
nohup sudo python2 Raspberry_ttyAMA0_Arduino_Serial3_USBImageSample.py > ImageSample.err 2>&1 &
sleep 2
echo 'Starting lighttp WebServer...'
sudo /usr/local/src/lighttpd/sbin/lighttpd -f /usr/local/src/lighttpd/config/lighttpd.conf &
sleep 30
echo 'Starting MysqlSave Process...'
nohup python2 Sys_Status_MysqlSave.py > Mysql.err 2>&1 &
sleep 2
echo 'Starting Tkinter Process...'
# export DISPLAY=:0
cd /home/pi/nexgen_pro/Tkinter_UI/
nohup python3.5 main.py > Tkinter.err 2>&1 &
!
