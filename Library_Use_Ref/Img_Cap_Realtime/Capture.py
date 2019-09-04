# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os
# initialize the camera and grab a reference to the raw camera capture

Image_Height = 128 # Set the image size_Height
Image_Width = 128 # Set the image size_Width

camera = PiCamera()
camera.resolution = (Image_Height, Image_Width)
camera.framerate = 20 # Set the FPS
camera.hflip = True
camera.vflip = False
rawCapture = PiRGBArray(camera, size=(Image_Height, Image_Width))
# allow the camera to warmup
time.sleep(0.1)

Train_Num = 500 # Train DataSet number
Total_Num = 500 # Total DataSet number(Total_Num-Train_Num = Test_Num)

Capture_Count = 1
Current_PWD = os.getcwd()

os.system('mkdir Train_DataSet')
os.system('mkdir Test_DataSet')

Train_Folder = Current_PWD + '/Train_DataSet'
Test_Folder  = Current_PWD + '/Test_DataSet'

# Make the journalingFile.log to information the user!
os.system('echo Welcome to the journalingFile > journalingFile.log')
os.system('date >> journalingFile.log')
os.system('echo ------------------------------------------------------------------------- >> journalingFile.log')
os.system('echo Image_Size:' + 'H:' + str(Image_Height) + ' ' + 'W:' + str(Image_Width) + ' >> journalingFile.log')
os.system('echo Image Type is PNG!RGB Color Model! >> journalingFile.log')
os.system('echo Train_DataSet_Number:' + str(Train_Num) + ' >> journalingFile.log')
os.system('echo Test_DataSet_Number:' + str(Total_Num-Train_Num) + ' >> journalingFile.log')
os.system('echo ------------------------------------------------------------------------- >> journalingFile.log')


# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
	image = frame.array
    # show the frame
	cv2.imshow("Frame", image)
	if Capture_Count <= Train_Num:
		cv2.imwrite(Train_Folder + '/' + str(Capture_Count) + '.png', image, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
	elif Capture_Count <= Total_Num:
		cv2.imwrite(Test_Folder  + '/' + str(Capture_Count-Train_Num) + '.png', image, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
	else:
		break
	Capture_Count += 1
	time.sleep(0.05) # The Frame_Rate can be set as 20 FPS
	
	key = cv2.waitKey(1) & 0xFF
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

cv2.destroyAllWindows()
