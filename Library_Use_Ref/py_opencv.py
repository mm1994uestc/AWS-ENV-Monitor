import os 
import sys
import cv2
import numpy as np

I = cv2.imread('0\'15.jpg',cv2.IMREAD_UNCHANGED)
I_w = np.size(I, 0)
I_h = np.size(I, 1)

print I[1,2,1],I_w,I_h
