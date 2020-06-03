int sensorPin = A0;
int ledPin = 13;
int sensorValue = 0;

int minimum = 2400;
int maximum = 0;
int average = 500;

int ledStatus = LOW;

const long dataRate = 50000;



unsigned long previousMicros = 0;


void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);

  for(int index=0; index<4000; index++)
  {
    if(index > 200) {
      sensorValue = analogRead(sensorPin);
      if (sensorValue <= minimum) {
        minimum = sensorValue;
      } else if (sensorValue >= maximum) {
        maximum = sensorValue;
      }
      delay(2);
    }
  }
  average = (maximum + minimum) / 2;
}


void loop() {  
  unsigned long currentMicros = micros();

  if (currentMicros - previousMicros >= dataRate) {
    previousMicros = currentMicros;
    
    sensorValue = analogRead(sensorPin);
    if(sensorValue >= average){
      if(ledStatus != HIGH){
        ledStatus = HIGH;
      }
      Serial.println(1);
      
    } else {
      if(ledStatus != LOW){
        ledStatus = LOW;
      }
      Serial.println(0);
    }
  }

  digitalWrite(ledPin, ledStatus);
}
