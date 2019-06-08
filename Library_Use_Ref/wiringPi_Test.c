#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
int main(int argc,char* argv[])
{
    if (argc < 2)
    {
        printf("Usage example: ./led 4 \n");
        return 1;
    }
    int pinNumber = atoi(argv[1]);//字符串转整形函数atoi()函数
    printf("PinNumber is:%d\n",pinNumber);
    if (-1 == wiringPiSetup())
    {
        printf("Setup wiringPi failed!");
        return 1;
    }
    printf("The Code will begain to Running!\n");
    pinMode(pinNumber, OUTPUT); // set mode to output 
    while(1) 
    {
        digitalWrite(pinNumber, 1); // output a high level 
        delay(2000);
	printf("The pin is up!\n");
        digitalWrite(pinNumber, 0); // output a low level 
        delay(2000);
	printf("The pin is down!\n");
    }
    return 0;
}
