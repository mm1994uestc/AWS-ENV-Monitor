const int LED_Pin = 13;
int incomingByte;
int UpdateByte = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_Pin,OUTPUT);
}
void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
  }
  if(UpdateByte != incomingByte){
    Serial.println(incomingByte);
    UpdateByte = incomingByte;
  }
  
  if (incomingByte == 'H') {
    digitalWrite(LED_Pin, HIGH);
  }
  if (incomingByte == 'L') {
    digitalWrite(LED_Pin, LOW);
  }
}
