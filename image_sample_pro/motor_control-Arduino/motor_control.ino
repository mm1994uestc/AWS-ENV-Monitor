int dirPin = 8;
int stepperPin = 7;
void setup() {
  // put your setup code here, to run once:
  pinMode(dirPin,OUTPUT);
  pinMode(stepperPin,OUTPUT);
}

void step(boolean dir,int steps)
{
  digitalWrite(dirPin,dir);
  delay(50);
  for(int i=0;i<steps;i++){
    digitalWrite(stepperPin, HIGH);
    delayMicroseconds(800);
    digitalWrite(stepperPin, LOW);
    delayMicroseconds(800); 
  }  
}

void loop() {
  // put your main code here, to run repeatedly:
  step(true,500);
  delay(500);
  step(false,500);
  delay(500);
}
