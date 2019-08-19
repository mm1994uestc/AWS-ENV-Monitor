# How to upload the Arduino's program to Hardware?
## The window env:
1. Download the Arduino IDE on your computer.
2. Find the avrdude in the installation folder.
`D:\Program Files (x86)\Arduino\hardware\tools\avr\bin`
3. Add the folder to the path variable so that you can use it directly!
4. Compile the Arduino's Script to the executiable HEX file.
   * In order to create the hex file,you need to change the Preference of the Arduino IDE like this:
   * Create a new folder to store the HEX file.
   * Find the preference.txt file and add the code above at the end of preference.txt.
`build.path=C:\HexOfArduino`
   * If you want print the infomation while Arduino IDE compile the script,you need to mpdify the preference.txt like this:
`upload.verbose=true`
5. Copy the avrdude.conf file to the HEX-file'folder(HEXOfArduino).
You can find the avrdude.conf file is this folder:
`D:\Program Files (x86)\Arduino\hardware\arduino\avr\bootloaders\gemma`
6. Download the hex file to the hardware.
Change the pwd into the HEX-file'folder(HEXOfArduino) firstly.  
`avrdude.exe -C avrdude.conf -v -v -v -v -p m328p -c arduino -P COM3 -b 57600 -D -U flash:w:Raspberry_Arduino_Motor_Control.ino.hex:i`
7. Finished upload.
## The Linux env:
1. Install the avrdude software to your Raspberry:
`sudo apt-get install avrdude`
2. Copy the avrdude.conf file to the upload-folder.
3. Copy the hex file to the upload-folder.
4. Use the command to upload the hex file to hardware.  
`avrdude -C avrdude.conf -v -v -v -v -p m328p -c arduino -P /dev/ttyUSB0 -b 57600 -D -U flash:w:Raspberry_Arduino_Motor_Control.ino.hex:i`
## Additions,How the use the minicom to communicate with USART protocal?
* Step1:Install the minicom software.
`sudo apt-get install minicom`
* Step2:Find the usb port we need to control.
`ls -al /dev/tty*`
* Step3:Connect the Raspberry to the USART Devices.
`sudo minicom -b 9600 -o -D /dev/ttyUSB0`
* Step4:Setting the minicom to show the data we send.
   * Firstly press the `Ctrl+A` and then press the `e`.
   * Now we are in the send data show mode.
# How to download the HEX update file from aws's3 server?
1. Create a new S3 bucket for your app and upload the hex file you want to update.
2. Install the boto3-python library for communicate with aws. `pip install boto3`
3. Install the aws-cli(AWS-Command line) so that you can connect to aws with boto3.
* Step1:Install awscli. `pip install awscli --upgrade --user`
* Step2:In order to add the aws cmd to the path we need to change the path'file. `sudo vim ~/.bashrc`
   * Insert the line at the end of path'file. `export PATH=~/.local/bin:$PATH`
   * Make the path'file work. `source ~/.bashrc`
* Step3:Test whether the awscli is installed successfully.
   * `aws --version`
   * It should show like this: `aws-cli/1.16.116 Python/3.6.8 Linux/4.14.77-81.59-amzn2.x86_64 botocore/1.12.106`
* Step4:Config the aws'configration.
   * Execute the cmd:`aws configure`
   * And then you need to insert your aws conut infomations:
   ```
   $ aws configure
   AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
   AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
   Default region name [None]: us-west-2
   Default output format [None]: json
   ```
4. Finished the aws-cli configration and then you can download hex file with boto3-python script.  
# Install The Opencv For Raspberry.  
1. If your just need to use the Opencv lib for Python,run the cmd below.  
  ```
  sudo apt-get install python-opencv
  pip install numpy
  ```  
  Test opencv have been already setup.  
  ```
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
  ```  
2. If your need to use C to development your app,you need to compile all the source code of Opencv and create the new opencv's lib for C.  
