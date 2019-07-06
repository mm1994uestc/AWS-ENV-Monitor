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
