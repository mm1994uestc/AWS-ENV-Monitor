## How to remove/download/upload the JPG in the AWS's S3 quickly?
1. Remove:We can use the aws-cli to remove the image-data recursively like this:  
`aws s3 rm s3://image-data/ --recursive --exclude "*" --include "*_2014_*_V_NU.jpg"`  
The re-rule is set by this:`*_2014_*_V_NU.jpg`
2. Download:Use the aws-cli download the image from AWS's S3 directly:  
`aws s3 cp s3://image-data/ ./ --recursive --exclude "*" --include "*_A1_V_NU.jpg"`
3. Upload:Use the aws-cli download the image from AWS's S3 directly:  
`aws s3 cp ./ s3://image-data/ --recursive --exclude "*" --include "*_A1_V_NU.jpg"`
## How to Upload the Picture to the aws server timingly?
* Step1: `sudo vim /etc/crontab`
* Step2:  Insert the time-line at the end of file and save it: 
`25 * * * * pi python /home/pi/nexgen_pro/image_sample_pro/Raspberry_Arduino_Motor_Control/image_data/image_aws_upload.py`
![crontab](https://github.com/mm1994uestc/AWS-ENV-Monitor/blob/master/image_sample_pro/Raspberry_Arduino_Motor_Control/image_data/pi-crontab-upload-image.png)
## How to use the script in the folder?(Introduce)
1. **mkdir.sh**: Used to make directorise recursively.(A1 ... A8,...,D1...D8)
2. **win_mkdir.bat**: Used to mkdir under the MSWindows Operation System.
3. **pic_rm.py**: Used to remove all the Image file recursively under the folder.
4. **image_aws_upload.py**: Used to upload all the image file under the folder recursively.(Compatibale with Windows/Linux-Python2.7/Python3)
5. **image_aws_download.py**: Used to download all the image file from aws's S3://image-data bucket recursively.(Compatibale with Windows/Linux/macOS-Python2.7/Python3)
6. **pic_rm.sh**: Used to delete the image file under the current folder.
