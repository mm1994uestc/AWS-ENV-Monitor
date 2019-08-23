import os 
import sys
import cv2
import numpy as np

I = cv2.imread('Test.jpg',cv2.IMREAD_UNCHANGED)
I_w = np.size(I, 0)
I_h = np.size(I, 1)

print I[1,2,1],I_w,I_h

if os.path.exists('/dev/video0') == False:
    print "No Camera Devices."
    sys.exit(2)
cap = cv2.VideoCapture(0)
i = 0
while True:
    ret,frame = cap.read()
    cv2.imwrite('Sample.jpg',frame)
    i += 1
    print i
cap.release()
