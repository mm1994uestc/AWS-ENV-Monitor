## How to autostart the image_sample.py Script?
You need to modify the crontab files to Start the Process when you boot the System.
1. Modify the crontab files.
`sudo crontab -e`
2. Insert the context in to the file.
`@reboot python /home/pi/nexgen_pro/image_sample_pro/image_sample.py`
3. Reboot your System and in Satrting when system is up!
## How to Keepping your putty connect the Raspberry Forever?
您可以配置*PuTTY*以定期自动发送“保持连接”数据以将会话保持活动状态。要避免由于会话处于不活动状态而与实例断开连接，这是非常有用的。在*Category*窗格中，选择*Connection*，然后在*Seconds between keepalives*字段中输入所需的间隔。
eg:如果您的会话在处于不活动状态10分钟后断开连接，请输入180以将*PuTTY*配置为每隔3分钟发送一次保持活动数据。
## The Motor Control protocal:
![Motor](https://github.com/mm1994uestc/AWS-ENV-Monitor/blob/master/image_sample_pro/motor_param/Y-%E7%94%B5%E6%9C%BA%E6%8E%A7%E5%88%B6%E6%97%B6%E5%BA%8F.jpg)
