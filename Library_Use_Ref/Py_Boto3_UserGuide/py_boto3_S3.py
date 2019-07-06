import boto3

s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print bucket.name

with open('Test_Download.hex','wb') as data:
    s3.meta.client.download_fileobj('arduino-program-update','Raspberry_Arduino_Motor_Control.ino.hex',data)
