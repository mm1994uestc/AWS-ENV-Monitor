const int Pin_AP = 2;
const int Pin_AN = 4;
const int Pin_BP = 12;
const int Pin_BN = 13;

const int Y_Speed_us = 1800; //1800 us Unit:us
unsigned int y_abs_position = 0;
int current_steps = 0;

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

void setup() {
  // put your setup code here, to run once:
  pinMode(Pin_AP,OUTPUT);
  pinMode(Pin_AN,OUTPUT);
  pinMode(Pin_BP,OUTPUT);
  pinMode(Pin_BN,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  y_step(1,100);
  delayMicroseconds(800);
  y_step(1,100);
  delayMicroseconds(800);
  y_step(0,100);
  delayMicroseconds(800);
  y_step(0,100);
  delayMicroseconds(800);
}
