# How to autostart the image_sample.py Script?
==============================================
## You need to modify the crontab files to Start the Process when you boot the System.
## Modify the crontab files.
`sudo crontab -e`
## Insert the context in to the file.
`@reboot python /home/pi/nexgen_pro/image_sample_pro/image_sample.py`
## Reboot your System and in Satrting when system is up!
