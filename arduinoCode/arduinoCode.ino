//includes 
#include <Wire.h>

//constants
#define HANSHAKE_CONFIRM_REQUEST_CODE '4'
#define HANSHAKE_CONFIRMATION_CODE '2'
#define COMAND_VOLTAGE_CHANGE 'v'
#define VOLTAGE_CHANGE_DONE 'd'
#define TABLE_SIZE 41
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
  
}

void loop() {
  if(Serial.available() > 0){
    int info = Serial.read();
    switch(info){
      case HANSHAKE_CONFIRM_REQUEST_CODE:
        Serial.write(HANSHAKE_CONFIRMATION_CODE);
        break;
       case COMAND_VOLTAGE_CHANGE:
        //blink(1000);
        //errorBlink();
        if(Serial.readBytesUntil('\0',information,41)==40){
          errorBlink();
        }
        Serial.write(VOLTAGE_CHANGE_DONE);
        Serial.flush();
      default:
        Serial.write(info);
    }
  }
  delay(4);
}
