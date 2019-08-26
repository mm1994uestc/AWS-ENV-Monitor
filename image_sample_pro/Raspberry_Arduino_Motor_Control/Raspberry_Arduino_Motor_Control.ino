#include <GravityTDS.h>
#include <Wire.h>

#define ADDRESS_SI7021 0x40
#define MEASURE_RH_HOLD 0xE5
#define READ_T_FROM_PRE_RH_MEASUREMENT 0xE0

#define CMD_DATA_Len 2

const int PH_SensorPin = A14;
float Current_PH = 0;

const int EC_SensorPin = A15;
GravityTDS gravityTds;
float temperature = 25,Current_EC = 0;

#define x_mm_pp 0.0711
#define y_mm_pp 0.0625// 1:100=0.0625 1:50=0.125

int Update_Flag = 0;
char Buffers[CMD_DATA_Len] = {0};

#define CMD_len 8
int Current_CO=0;
unsigned char CMD_Array[8] = {0xFE,0x04,0x00,0x03,0x00,0x01,0xD5,0xC5};

const int Pin_AP = 2;
const int Pin_AN = 3;
const int Pin_BP = 4;
const int Pin_BN = 5;
const int Y_Trigger = 6;
const int Y_Speed_us = 1800; //1800 us Unit:us

const int dirPin = 8;
const int stepperPin = 7;
const int enPin = 9;
const int X_Trigger = 11;
const int X_Speed = 800;

unsigned int x_abs_position = 0;
unsigned int y_abs_position = 0;
int current_steps = 0;

#define Delay_Device 7
const int CO2_Control_Pin = 18,whiteLight_Pin = 19,GorwLight1_Pin = 24,GorwLight2_Pin = 25,DosingPump1_Pin = 22,DosingPump2_Pin = 23,DosingPump3_Pin = 26;
const int Delay_PinList[Delay_Device] = {CO2_Control_Pin,whiteLight_Pin,GorwLight1_Pin,GorwLight2_Pin,DosingPump1_Pin,DosingPump2_Pin,DosingPump3_Pin};
void DelayPin_initial(int *PinList,int len)
{
  int i=0;
  for(i=0;i<len;i++){
    pinMode(PinList[i],OUTPUT);
  }
}
void DelayPin_Control(int PinNum,int state)
{
  digitalWrite(PinNum,state);
}

void x_step(boolean dir,int steps)
{
  digitalWrite(enPin,0);
  digitalWrite(dirPin,dir);
  delay(10);
  for(int i=0;i<steps;i++){
    digitalWrite(stepperPin, HIGH);
    delayMicroseconds(X_Speed);
    digitalWrite(stepperPin, LOW);
    delayMicroseconds(X_Speed); 
  }  
  
  if(dir == 0) x_abs_position += steps;
  if(dir == 1) x_abs_position -= steps;
}
void y_step(boolean dir,int steps)
{
  if(dir==0)
  {
    for(int i=0;i<steps;i++){
      digitalWrite(Pin_AP,HIGH); digitalWrite(Pin_AN,LOW);
      digitalWrite(Pin_BP,LOW);  digitalWrite(Pin_BN,HIGH);
      delayMicroseconds(Y_Speed_us);
      digitalWrite(Pin_AP,HIGH); digitalWrite(Pin_AN,LOW);
      digitalWrite(Pin_BP,HIGH); digitalWrite(Pin_BN,LOW);
      delayMicroseconds(Y_Speed_us);
      digitalWrite(Pin_AP,LOW);  digitalWrite(Pin_AN,HIGH);
      digitalWrite(Pin_BP,HIGH); digitalWrite(Pin_BN,LOW);
      delayMicroseconds(Y_Speed_us);
      digitalWrite(Pin_AP,LOW); digitalWrite(Pin_AN,HIGH);
      digitalWrite(Pin_BP,LOW);  digitalWrite(Pin_BN,HIGH);
      delayMicroseconds(Y_Speed_us);
      y_abs_position -= 1;
    }
  }
  if(dir==1)
  {
    for(int i=0;i<steps;i++){
      digitalWrite(Pin_AP,LOW); digitalWrite(Pin_AN,HIGH);
      digitalWrite(Pin_BP,LOW);  digitalWrite(Pin_BN,HIGH);
      delayMicroseconds(Y_Speed_us);
      digitalWrite(Pin_AP,LOW);  digitalWrite(Pin_AN,HIGH);
      digitalWrite(Pin_BP,HIGH); digitalWrite(Pin_BN,LOW);
      delayMicroseconds(Y_Speed_us);
      digitalWrite(Pin_AP,HIGH); digitalWrite(Pin_AN,LOW);
      digitalWrite(Pin_BP,HIGH); digitalWrite(Pin_BN,LOW);
      delayMicroseconds(Y_Speed_us);
      digitalWrite(Pin_AP,HIGH); digitalWrite(Pin_AN,LOW);
      digitalWrite(Pin_BP,LOW);  digitalWrite(Pin_BN,HIGH);
      delayMicroseconds(Y_Speed_us);
      y_abs_position += 1;
    }
  }
  digitalWrite(Pin_AP,0); digitalWrite(Pin_AN,0); // Close the micro motor
  digitalWrite(Pin_BP,0); digitalWrite(Pin_BN,0);
}

void x_initial(void)
{
  digitalWrite(enPin,0);
  digitalWrite(dirPin,1);
  x_step(1,x_abs_position); // We first control the motor back itself,and then we use the IR-Sensor to check it.
  while(digitalRead(X_Trigger) == 0){
    digitalWrite(stepperPin, HIGH);
    delayMicroseconds(X_Speed);
    digitalWrite(stepperPin, LOW);
    delayMicroseconds(X_Speed-20);
  }
  digitalWrite(enPin,1); // Close the 42Motor
  x_abs_position = 0;
}

void y_initial(void)
{
  y_step(0,y_abs_position); // We first control the motor back itself,and then we use the IR-Sensor to check it.
  /*
  while(digitalRead(Y_Trigger) == 1){ // Judge the condition cost the time.We define it about 20us.
      digitalWrite(Pin_AP,HIGH); digitalWrite(Pin_AN,LOW);
      digitalWrite(Pin_BP,LOW);  digitalWrite(Pin_BN,HIGH);
      delayMicroseconds(Y_Speed_us);
      digitalWrite(Pin_AP,HIGH); digitalWrite(Pin_AN,LOW);
      digitalWrite(Pin_BP,HIGH); digitalWrite(Pin_BN,LOW);
      delayMicroseconds(Y_Speed_us);
      digitalWrite(Pin_AP,LOW);  digitalWrite(Pin_AN,HIGH);
      digitalWrite(Pin_BP,HIGH); digitalWrite(Pin_BN,LOW);
      delayMicroseconds(Y_Speed_us);
      digitalWrite(Pin_AP,LOW); digitalWrite(Pin_AN,HIGH);
      digitalWrite(Pin_BP,LOW);  digitalWrite(Pin_BN,HIGH);
      delayMicroseconds(Y_Speed_us-20);
  }*/
  digitalWrite(Pin_AP,0); digitalWrite(Pin_AN,0); // Close the micro motor
  digitalWrite(Pin_BP,0); digitalWrite(Pin_BN,0);
  y_abs_position = 0;
}

void Stop_Motor(void)
{
  digitalWrite(Pin_AP,LOW); digitalWrite(Pin_AN,LOW); digitalWrite(Pin_BP,LOW); digitalWrite(Pin_BN,LOW); digitalWrite(enPin,1);
}

float Get_PH_Val(const int PH_SensorPin)
{
  unsigned long int avgValue;  //Store the average value of the sensor feedback
  float b;
  int buf[10],temp;
  for(int i=0;i<10;i++)       //Get 10 sample value from the sensor for smooth the value
  { 
    buf[i]=analogRead(PH_SensorPin);
    delay(5);
  }
  for(int i=0;i<9;i++)        //sort the analog from small to large
  {
    for(int j=i+1;j<10;j++)
    {
      if(buf[i]>buf[j])
      {
        temp=buf[i];
        buf[i]=buf[j];
        buf[j]=temp;
      }
    }
  }
  avgValue=0;
  for(int i=2;i<8;i++)                      //take the average value of 6 center sample
    avgValue+=buf[i];
  float phValue=(float)avgValue*5.0/1024/6; //convert the analog into millivolt
  phValue=3.5*phValue;                      //convert the millivolt into pH value  
  return phValue;
}

float Get_EC_Val(void)
{
  gravityTds.setTemperature(temperature);  // set the temperature and execute temperature compensation
  gravityTds.update();  //sample and calculate 
  return gravityTds.getTdsValue();  // then get the value
}
float SI7021_Get_Temp(void)
{
  byte buffer[] = {0, 0};
  word outTemp = 0;
  float valueTemp = 0;

  Wire.beginTransmission(ADDRESS_SI7021);
  Wire.write(READ_T_FROM_PRE_RH_MEASUREMENT);
  Wire.endTransmission();

  Wire.requestFrom(ADDRESS_SI7021, 2);
  if(Wire.available() >= 2){
    buffer[0] = Wire.read(); //high byte
    buffer[1] = Wire.read(); //low byte; no crc  
  }
  outTemp = (buffer[0]<<8) | buffer[1];
  valueTemp = 175.72*outTemp/65536 - 46.85;
  return valueTemp;
}

float SI7021_Get_Humi(void)
{
  byte buffer[] = {0, 0, 0};
  word outHumi = 0;
  float valueHumi = 0;

  Wire.beginTransmission(ADDRESS_SI7021);  
  Wire.write(MEASURE_RH_HOLD);
  Wire.endTransmission();

  Wire.requestFrom(ADDRESS_SI7021, 3);
  if(Wire.available() >= 3){
    buffer[0] = Wire.read(); //high byte
    buffer[1] = Wire.read(); //low byte
    buffer[2] = Wire.read(); //crc
  }
  outHumi = (buffer[0]<<8) | buffer[1];
  valueHumi = 125.0*outHumi/65536 - 6;
  return valueHumi;
}

void CO2_USART_Initial(int CO2_baud)
{
  Serial2.begin(CO2_baud);
}
int CO2_USART_GetValue(void)
{
  unsigned char CO2_BUF[7] = "";
  unsigned int H_Bits=0,L_Bits=0,H_Bits_H=0,H_Bits_L=0,L_Bits_H=0,L_Bits_L=0;
  unsigned int CO2_PPM = 0;
  Serial2.write(CMD_Array,8);
  delayMicroseconds(5000);
  while(Serial2.available() < 7) {;}
  while(Serial2.available() != 0){Serial2.readBytes(CO2_BUF,7);}
  
  H_Bits = CO2_BUF[3];
  L_Bits = CO2_BUF[4];
  
  H_Bits_H = H_Bits>>4;
  H_Bits_L = H_Bits&0x0F;
  L_Bits_H = L_Bits>>4;
  L_Bits_L = L_Bits&0x0F;
  CO2_PPM = H_Bits_H*4096 + H_Bits_L*256 + L_Bits_H*16 + L_Bits_L;
  return CO2_PPM;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  CO2_USART_Initial(9600);
  DelayPin_initial(Delay_PinList,Delay_Device);
  Wire.begin();
  
  pinMode(dirPin,OUTPUT);
  pinMode(stepperPin,OUTPUT);
  pinMode(enPin,OUTPUT);
  pinMode(X_Trigger,INPUT);

  pinMode(Pin_AP,OUTPUT);
  pinMode(Pin_AN,OUTPUT);
  pinMode(Pin_BP,OUTPUT);
  pinMode(Pin_BN,OUTPUT);
  pinMode(Y_Trigger,INPUT);

  gravityTds.setPin(EC_SensorPin);
  gravityTds.setAref(5.0);  //reference voltage on ADC, default 5.0V on Arduino UNO
  gravityTds.setAdcRange(1024);  //1024 for 10bit ADC;4096 for 12bit ADC
  gravityTds.begin();  //initialization
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available() != 0){
      Serial.readBytes(Buffers,CMD_DATA_Len);
      Update_Flag = 1;
  }
  
  if(Update_Flag == 1){
    if(Buffers[0] == 'A') {current_steps = int(float(Buffers[1])/x_mm_pp); x_step(1,current_steps);  Serial.println("OK-A");} // 向右后退
    if(Buffers[0] == 'B') {current_steps = int(float(Buffers[1])/x_mm_pp); x_step(0,current_steps);  Serial.println("OK-B");} // 向左前进
    if(Buffers[0] == 'C') {current_steps = int(float(Buffers[1])/y_mm_pp); y_step(1,current_steps);  Serial.println("OK-C");} // 向下前进
    if(Buffers[0] == 'D') {current_steps = int(float(Buffers[1])/y_mm_pp); y_step(0,current_steps);  Serial.println("OK-D");} // 向上后退
    if(Buffers[0] == 'E') {x_initial();  delay(300); Serial.println("OK-E");}
    if(Buffers[0] == 'F') {y_initial();  delay(300); Serial.println("OK-F");}
    if(Buffers[0] == 'S') {Stop_Motor(); delay(300); Serial.println("OK-S");}
    if(Buffers[0] == 'G') {digitalWrite(CO2_Control_Pin,LOW); delay(1000); Serial.println("OK-GCO2 ON");}
    if(Buffers[0] == 'H') {digitalWrite(CO2_Control_Pin,HIGH); delay(1000); Serial.println("OK-HCO2 OFF");}
    if(Buffers[0] == 'I') {Current_PH = Get_PH_Val(PH_SensorPin); delay(1000); Serial.print(" PH:");Serial.print(Current_PH,2); Serial.println("OK-I");}
    if(Buffers[0] == 'J') {Current_EC = Get_EC_Val(); delay(1000); Serial.print(" EC:");Serial.print(Current_EC,2);Serial.println("OK-J");}
    if(Buffers[0] == 'K') {Current_CO = CO2_USART_GetValue(); delay(1000); Serial.print(" CO2:");Serial.print(Current_CO,DEC);Serial.println("OK-K");}
    
    // whiteLight_Pin,GorwLight1_Pin,GorwLight2_Pin,DosingPump1_Pin,DosingPump2_Pin,DosingPump3_Pin;
    if(Buffers[0] == 'L') {DelayPin_Control(whiteLight_Pin,1);delay(1500); Serial.println("OK-L");}
    if(Buffers[0] == 'M') {DelayPin_Control(whiteLight_Pin,0);delay(1500); Serial.println("OK-M");}
    if(Buffers[0] == 'N') {DelayPin_Control(GorwLight1_Pin,1);delay(1500); Serial.println("OK-N");}
    if(Buffers[0] == 'O') {DelayPin_Control(GorwLight1_Pin,0);delay(1500); Serial.println("OK-O");}
    if(Buffers[0] == 'P') {DelayPin_Control(GorwLight2_Pin,1);delay(1500); Serial.println("OK-P");}
    if(Buffers[0] == 'Q') {DelayPin_Control(GorwLight2_Pin,0);delay(1500); Serial.println("OK-Q");}
    
    if(Buffers[0] == 'R') {DelayPin_Control(DosingPump1_Pin,1);delay(1500); Serial.println("OK-R");}
    if(Buffers[0] == 'T') {DelayPin_Control(DosingPump1_Pin,0);delay(1500); Serial.println("OK-T");}
    if(Buffers[0] == 'U') {DelayPin_Control(DosingPump2_Pin,1);delay(1500); Serial.println("OK-U");}
    if(Buffers[0] == 'V') {DelayPin_Control(DosingPump2_Pin,0);delay(1500); Serial.println("OK-V");}
    if(Buffers[0] == 'W') {DelayPin_Control(DosingPump3_Pin,1);delay(1500); Serial.println("OK-W");}
    if(Buffers[0] == 'X') {DelayPin_Control(DosingPump3_Pin,0);delay(1500); Serial.println("OK-X");}
    Update_Flag = 0;
  }
}
