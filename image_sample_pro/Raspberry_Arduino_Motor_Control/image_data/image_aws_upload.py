import os
import sys
import glob
import time
import boto3

Upload_tm = time.localtime(time.time())
Current_date = str(Upload_tm.tm_year) + '-' + str(Upload_tm.tm_mon) + '-' + str(Upload_tm.tm_mday) + '-' + str(Upload_tm.tm_hour) + '-' + str(Upload_tm.tm_min) + '-' + str(Upload_tm.tm_sec)
print Current_date
print "Start uploading images:"

image_obj = []
s3 = boto3.resource('s3')

Journal = open('sample_Journal.log','a')
Journal.write("Upload-Time:"+Current_date+'\n')

for i in range(1,4):
    folder_name = 'A' + str(i)
    Find_image_path = './'+folder_name+'/*.jpg'
    image_dataset = glob.glob(Find_image_path)
    image_n = len(image_dataset)
    for i in range(image_n):
        image_name = image_dataset[i][5:]
        Journal.write(image_name+'\n')
        print "Uploading " + image_name + "..."
        with open(image_dataset[i],'rb') as data:
            s3.meta.client.upload_fileobj(data,'image-data',image_name)
        print "Deleting " + image_name + "..."
        os.system('rm -f ' + image_dataset[i])

Journal.close()
print "Finish Uploading Images."
