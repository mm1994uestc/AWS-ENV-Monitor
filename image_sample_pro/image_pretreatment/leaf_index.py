#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 16:28:25 2019

@author: annaning
"""

import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os
import glob
import boto3

#Step 1 : Define the input location 
path ='D:/AWS/nexgen/*/*.jpg'
filenames = glob.glob(path)

#Step 2: Import the all files 
list2=['1059','1459'] 
list1=[]
for f in filenames:
    if any(x in f for x in list2):
        newfile=f
        list1.append(f)

#Step 3: Calculate the index of leaf
leaf_index=[]
for i in list1:
    img =cv2.imread(i, 1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (36, 0, 0), (70, 255,255))
    imask = mask>0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]
    green = np.where(green > 0, 1, 0)
    lai = np.mean(green)
    leaf_index.append(lai)

#Step 4 ： Data cleaning
leaf_index1=pd.DataFrame(leaf_index)
file0=pd.DataFrame(list1)

file1=file0[0].str.split('_', expand=True)
file1=file1.filter([4,2,3])

data=pd.concat([file1, leaf_index1], axis=1, sort=False)
data.rename(columns={4:"bucketName",2:"dateofPhoto",3:"timeofPhoto",0:"leafAreaIndex"}, inplace=True)

data.to_csv('D:/AWS/nexgen/data.csv')    

#Step 5: upload to AWS
s3 = boto3.client('s3')
filename = 'D:/AWS/nexgen/data.csv'
bucket_name = 'leafindex'
s3.upload_file(filename, bucket_name, 'data.csv')
