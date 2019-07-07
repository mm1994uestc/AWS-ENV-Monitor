const int Pin_AP = 2;
const int Pin_AN = 4;
const int Pin_BP = 12;
const int Pin_BN = 13;

const int dirPin = 8;
const int stepperPin = 7;
const int enPin = 9;

void setup() {
  // put your setup code here, to run once:
  pinMode(dirPin,OUTPUT);
  pinMode(stepperPin,OUTPUT);
  pinMode(enPin,OUTPUT);

  pinMode(Pin_AP,OUTPUT);
  pinMode(Pin_AN,OUTPUT);
  pinMode(Pin_BP,OUTPUT);
  pinMode(Pin_BN,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(dirPin,HIGH);
  digitalWrite(stepperPin,HIGH);
  digitalWrite(enPin,HIGH);
  digitalWrite(Pin_AP,HIGH);
  digitalWrite(Pin_AN,HIGH);
  digitalWrite(Pin_BP,HIGH);
  digitalWrite(Pin_BN,HIGH);
  delay(1000);
  digitalWrite(dirPin,LOW);
  digitalWrite(stepperPin,LOW);
  digitalWrite(enPin,LOW);
  digitalWrite(Pin_AP,LOW);
  digitalWrite(Pin_AN,LOW);
  digitalWrite(Pin_BP,LOW);
  digitalWrite(Pin_BN,LOW);
  delay(1000);
}
