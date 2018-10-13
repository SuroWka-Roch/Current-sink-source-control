//includes 
#include <Wire.h>

//constants
#define HANSHAKE_CONFIRM_REQUEST_CODE '4'
#define HANSHAKE_CONFIRMATION_CODE '2'
#define COMAND_VOLTAGE_CHANGE 'v'
#define VOLTAGE_CHANGE_DONE 'd'
#define TABLE_SIZE 41
#define DAC_ADRESS 72 //important to działa
#define DAC_CHANGE_VALUE_AND_UPDATE_4BITS 0x30
// Globals :(
char information[TABLE_SIZE];

// for debuging
void blink(int time) {
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(time);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(time);
}

void errorBlink(){ 
  for(int i=0; i<20 ;i++){
    blink(200);
  }
}
void clearTable(char* table){
    for(int i=0;i<TABLE_SIZE;i++){
      *(table+i)='\0';  
    }
}
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN,OUTPUT);
  clearTable(information);
  Wire.begin();
}

void loop() {
  
  if(Serial.available() > 0){
    int info = Serial.read();
    switch(info){
      case HANSHAKE_CONFIRM_REQUEST_CODE:
        Serial.write(HANSHAKE_CONFIRMATION_CODE);
        break;
      case COMAND_VOLTAGE_CHANGE:
        Serial.readBytesUntil('\0',information,41);
        // tytaj wysyłaj
        sendVoltageInformation();
        clearTable(information);
        Serial.write(VOLTAGE_CHANGE_DONE);
        Serial.flush();
      default:
        Serial.write(info);
    }
  }
  delay(300);
}
void sendVoltageInformation(){
  char *charP = information; 
  while(*charP!='\0'){
    if(*charP>='a' && *charP<='h'){
      int portNumber = int(*charP)-97;
      int voltValue = int((*(++charP) - 48 ))*1000;
      for(int i =100;i>=1;i=i/10){
        voltValue += int((*(++charP) - 48))*i;
      }
      j2lComunication(portNumber,voltValue);
      //Serial.write(voltValue);
      charP++;
    }  
  }  
}
void j2lComunication(int portNumber,int voltValue){
  //Serial.write(voltValue);
  Wire.beginTransmission(DAC_ADRESS); // transmit to device
  Wire.write(DAC_CHANGE_VALUE_AND_UPDATE_4BITS + portNumber);        // 
  Wire.write(voltValue/16);              // send pierwszy bit
  Wire.write((voltValue%16)*16);      //drugi bit 
  Wire.endTransmission();    // stop transmitting

  
  /*for(int i =0 ;i<8 ;i++){
  Wire.beginTransmission(DAC_ADRESS); // transmit to device
  Wire.write(0x30+i);        // 
  Wire.write(254/2);              // send pierwszy bit
  Wire.write(254/2);      //drugi bit 
  if(Wire.endTransmission()== 0)    // stop transmitting
  {
  Serial.write('a');
  }
  }8*/
}
