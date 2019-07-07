import os
import sys
import glob
import time
import boto3

Upload_tm = time.localtime(time.time())
Current_date = str(Upload_tm.tm_year) + '-' + str(Upload_tm.tm_mon) + '-' + str(Upload_tm.tm_mday) + '-' + str(Upload_tm.tm_hour) + '-' + str(Upload_tm.tm_min) + '-' + str(Upload_tm.tm_sec)

image_obj = []
folder_obj = ['A1','A2','A3','A4','A5','A6','A7','A8','B1','B2','B3','B4','B5','B6','B7','B8',\
        'C1','C2','C3','C4','C5','C6','C7','C8','D1','D2','D3','D4','D5','D6','D7','D8']

s3 = boto3.resource('s3')
image_data_bucket = s3.Bucket('image-data')
print 's3.bucket.name:',image_data_bucket.name
print "Start downloading images:(" + Current_date + ')'

Journal = open('Download-Journal.log','a')
Journal.write("Download-Time:"+Current_date+'\n')

for img in image_data_bucket.objects.all():
    image_name = img.key
    print "Downloading " + image_name + "..."
    for folder_name in folder_obj:
        if folder_name in image_name:
            download_pos = './' + folder_name + '/' + image_name
            Journal.write(image_name+'\n')
            with open(download_pos,'a') as data:
                image_data_bucket.download_fileobj(image_name,data)
            break

Journal.close()
print "Finish Downloading Images."
