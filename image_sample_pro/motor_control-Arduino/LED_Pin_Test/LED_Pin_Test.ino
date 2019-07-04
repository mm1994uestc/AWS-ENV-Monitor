const int LED_Pin = 13;
void setup() {
  // put your setup code here, to run once:
  pinMode(LED_Pin,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(LED_Pin,HIGH);
  delay(1000);
  digitalWrite(LED_Pin,LOW);
  delay(1000);
}
