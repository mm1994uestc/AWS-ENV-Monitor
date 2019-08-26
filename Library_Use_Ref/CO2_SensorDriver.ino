#define CMD_len 8
int Current_CO=0;

unsigned char CMD_Array[8] = {0xFE,0x04,0x00,0x03,0x00,0x01,0xD5,0xC5};

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
  Serial.println(H_Bits_H,HEX);
  Serial.println(H_Bits_L,HEX);
  Serial.println(L_Bits_H,HEX);
  Serial.println(L_Bits_L,HEX);
  CO2_PPM = H_Bits_H*4096 + H_Bits_L*256 + L_Bits_H*16 + L_Bits_L;
  return CO2_PPM;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  CO2_USART_Initial(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  Current_CO = CO2_USART_GetValue();
  Serial.print(" CO2:");
  Serial.print(Current_CO,DEC);
  Serial.println("OK-KCO2");
  int i = 2000;
  Serial.println("Waiting...");
  while(i--){delayMicroseconds(5000);}
}
