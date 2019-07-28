#define DATA_Len 7
int Update_Flag = 0;
char Buffers[DATA_Len] = {0};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("CO2-CMD-Send:");
  Serial.println("FE0400030001D5C5");
  delayMicroseconds(5000); delayMicroseconds(5000); delayMicroseconds(5000); 
  delayMicroseconds(5000); delayMicroseconds(5000); delayMicroseconds(5000); 
  while(Serial.available() != 0){
      Serial.readBytes(Buffers,DATA_Len);
      Update_Flag = 1;
  }
  if(Update_Flag){
    Serial.print("CO2-Value:");
      Serial.println(Buffers);
    }
}
