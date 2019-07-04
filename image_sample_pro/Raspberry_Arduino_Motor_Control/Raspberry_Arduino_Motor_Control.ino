#define CMD_DATA_Len 2
#define x_mm_pp 0.0711
#define y_mm_pp 0.0625

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
  digitalWrite(enPin,1);
  if(dir == 0) x_abs_position -= steps;
  if(dir == 1) x_abs_position += steps;
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
  if(dir == 0) y_abs_position -= steps;
  if(dir == 1) y_abs_position += steps;
}

void x_initial(void)
{
  x_step(0,x_abs_position);
  /*
  while(digitalRead(X_Trigger)){
    x_step(0,15);  
  }*/
}

void y_initial(void)
{
  y_step(0,y_abs_position);
  /*
  while(digitalRead(Y_Trigger)){
    y_step(0,15);  
  }*/
}

void Stop_Motor(void)
{
  digitalWrite(Pin_AP,LOW); digitalWrite(Pin_AN,LOW); digitalWrite(Pin_BP,LOW); digitalWrite(Pin_BN,LOW); digitalWrite(enPin,1);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  // pinMode(LED_Pin,OUTPUT);
  
  pinMode(dirPin,OUTPUT);
  pinMode(stepperPin,OUTPUT);
  pinMode(enPin,OUTPUT);
  pinMode(X_Trigger,INPUT);

  pinMode(Pin_AP,OUTPUT);
  pinMode(Pin_AN,OUTPUT);
  pinMode(Pin_BP,OUTPUT);
  pinMode(Pin_BN,OUTPUT);
  pinMode(Y_Trigger,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available() != 0){
      Serial.readBytes(Buffers,CMD_DATA_Len);
      Update_Flag = 1;
  }
  
    if(Update_Flag == 1){
    if(Buffers[0] == 'A') {current_steps = int(Buffers[1]/x_mm_pp); x_step(1,current_steps);  Serial.println("OK");}
    if(Buffers[0] == 'B') {current_steps = int(Buffers[1]/x_mm_pp); x_step(0,current_steps);  Serial.println("OK");}
    if(Buffers[0] == 'C') {current_steps = int(Buffers[1]/y_mm_pp); y_step(1,current_steps);  Serial.println("OK");}
    if(Buffers[0] == 'D') {current_steps = int(Buffers[1]/y_mm_pp); y_step(0,current_steps);  Serial.println("OK");}
    if(Buffers[0] == 'E') {x_initial();  Serial.println("OK");}
    if(Buffers[0] == 'F') {y_initial();  Serial.println("OK");}
    if(Buffers[0] == 'S') {Stop_Motor(); Serial.println("OK");}
    Update_Flag = 0;
  }
}
