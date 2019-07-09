import os
import sys
import glob
import time
import sys
import getpass

'''
System Requir:
1. AWS-CLI installed ans configure
2. Boto3 python library is installed
3. If in Linux,you'd better mkdir "/home/pi/nexgen_pro/image_sample_pro/Raspberry_Arduino_Motor_Control/image_data/" and A1...A8,...,D1...D8.
'''

mswindows = (sys.platform == "win32")
linux = (sys.platform == "linux2" or sys.platform == "linux")

Upload_tm = time.localtime(time.time())
Current_date = str(Upload_tm.tm_year) + '-' + str(Upload_tm.tm_mon) + '-' + str(Upload_tm.tm_mday) + '-' + str(Upload_tm.tm_hour) + '-' + str(Upload_tm.tm_min) + '-' + str(Upload_tm.tm_sec)

image_obj = []
folder_obj = ['A1','A2','A3','A4','A5','A6','A7','A8','B1','B2','B3','B4','B5','B6','B7','B8',\
        'C1','C2','C3','C4','C5','C6','C7','C8','D1','D2','D3','D4','D5','D6','D7','D8']

if mswindows:
    print('Platform:Windows.')
    print("Start uploading images:",Current_date)
    Journal = open('sample_Journal.log','a')
    Journal.write("Upload-Time:"+Current_date+'\n')
    for folder in folder_obj:
        aws_cli = 'aws s3 cp ./' + folder + '/ s3://image-data/ --recursive --exclude \"*\" --include \"*_' + folder + '_V_NU.jpg\"'
        print('Uploading the ' + folder + '\'s image...')
        os.system(aws_cli)
    Journal.close()
    print("Finish Uploading Images.")
        
if linux:
    print('Platform:Linux.')
    print("Start uploading images:",Current_date)
    import boto3
    abs_path = "/home/"+ getpass.getuser() +"/nexgen_pro/image_sample_pro/Raspberry_Arduino_Motor_Control/image_data/"
    name_start = len(abs_path) + 3
    s3 = boto3.resource('s3')
    Journal = open(abs_path + 'sample_Journal.log','a+')
    Journal.write("Upload-Time:"+Current_date+'\n')
    
    for folder_name in folder_obj:
        Find_image_path = abs_path + folder_name + '/*.jpg'
        image_dataset = glob.glob(Find_image_path)
        image_n = len(image_dataset)
        for i in range(image_n):
            image_name = image_dataset[i][name_start:]
            Journal.write(image_name+'\n')
            print("Uploading " + image_name + "...")
            with open(image_dataset[i],'rb') as data:
                s3.meta.client.upload_fileobj(data,'image-data',image_name)
            print("Deleting " + image_name + "...")
            os.system('rm -f ' + image_dataset[i])
    Journal.close()
    print("Finish Uploading Images.")
