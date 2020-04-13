int sensorPin = A0;
int ledPin = 13;
int sensorValue = 0;

int minimum = 2400;
int maximum = 0;
int average = 500;
//int data[64] = {};
//int dataIndex = 0;
int lastbit = 0;

int ledStatus = LOW;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(19200);

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
  sensorValue = analogRead(sensorPin);
  if(sensorValue >= average){
    if(ledStatus != HIGH){
      ledStatus = HIGH;
      Serial.println(1);
//      data[dataIndex] = 1;
//      dataIndex += 1;
    }
  } else {
    if(ledStatus != LOW){
      ledStatus = LOW;
      Serial.println(0);
//      data[dataIndex] = 0;
//      dataIndex += 1;
    }
  }

  digitalWrite(ledPin, ledStatus);

//  Serial.print(*data);
//  Serial.print(sensorValue);
//  Serial.print("\t");
//  Serial.print(average);
//  Serial.println();
}
