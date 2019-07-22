#include <GravityTDS.h>

#define CMD_DATA_Len 2

const int PH_SensorPin = 14;
float Current_PH = 0;

const int EC_SensorPin = 3;
GravityTDS gravityTds;
float temperature = 25,Current_EC = 0;

const int CO2_Control_Pin = 5;

#define x_mm_pp 0.0711
#define y_mm_pp 0.0625// 1:100=0.0625 1:50=0.125

int Update_Flag = 0;
char Buffers[CMD_DATA_Len] = {0};

const int Pin_AP = 2;
const int Pin_AN = 4;
const int Pin_BP = 12;
const int Pin_BN = 13;
const int Y_Trigger = 10;
const int Y_Speed_us = 1800; //1800 us Unit:us

const int dirPin = 8;
const int stepperPin = 7;
const int enPin = 9;
const int X_Trigger = 11;
const int X_Speed = 800;

unsigned int x_abs_position = 0;
unsigned int y_abs_position = 0;
int current_steps = 0;

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
    }
  }
  digitalWrite(Pin_AP,0); digitalWrite(Pin_AN,0); // Close the micro motor
  digitalWrite(Pin_BP,0); digitalWrite(Pin_BN,0);
  if(dir == 0) y_abs_position -= steps;
  if(dir == 1) y_abs_position += steps;
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
  }
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
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  pinMode(dirPin,OUTPUT);
  pinMode(stepperPin,OUTPUT);
  pinMode(enPin,OUTPUT);
  pinMode(X_Trigger,INPUT);

  pinMode(Pin_AP,OUTPUT);
  pinMode(Pin_AN,OUTPUT);
  pinMode(Pin_BP,OUTPUT);
  pinMode(Pin_BN,OUTPUT);
  pinMode(Y_Trigger,INPUT);

  pinMode(CO2_Control_Pin,OUTPUT);

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
  
//  Current_PH = Get_PH_Val(PH_SensorPin); 
//  Current_EC = Get_EC_Val();
//  
//  Serial.print(" PH:");
//  Serial.print(Current_PH,2);
//  Serial.println(" ");
//
//  Serial.print(Current_EC,0);
//  Serial.println("ppm");
  
  if(Update_Flag == 1){
    if(Buffers[0] == 'A') {current_steps = int(float(Buffers[1])/x_mm_pp); x_step(1,current_steps);  Serial.println("OK-A");} // 向右后退
    if(Buffers[0] == 'B') {current_steps = int(float(Buffers[1])/x_mm_pp); x_step(0,current_steps);  Serial.println("OK-B");} // 向左前进
    if(Buffers[0] == 'C') {current_steps = int(float(Buffers[1])/y_mm_pp); y_step(1,current_steps);  Serial.println("OK-C");} // 向下前进
    if(Buffers[0] == 'D') {current_steps = int(float(Buffers[1])/y_mm_pp); y_step(0,current_steps);  Serial.println("OK-D");} // 向上后退
    if(Buffers[0] == 'E') {x_initial();  Serial.println("OK-E");}
    if(Buffers[0] == 'F') {y_initial();  Serial.println("OK-F");}
    if(Buffers[0] == 'S') {Stop_Motor(); Serial.println("OK-S");}
    if(Buffers[0] == 'G') {digitalWrite(CO2_Control_Pin,LOW); Serial.println("OK-GCO2 ON");}
    if(Buffers[0] == 'H') {digitalWrite(CO2_Control_Pin,HIGH); Serial.println("OK-HCO2 OFF");}
    if(Buffers[0] == 'I') {Current_PH = Get_PH_Val(PH_SensorPin); Serial.print(" PH:");Serial.print(Current_PH,2); Serial.println("OK-IPH");}
    if(Buffers[0] == 'J') {Current_EC = Get_EC_Val(); Serial.print(" EC:");Serial.print(Current_EC,2);Serial.println("OK-JTDS");}
    Update_Flag = 0;
  }
}
