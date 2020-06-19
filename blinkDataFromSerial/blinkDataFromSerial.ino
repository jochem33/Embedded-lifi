const int ledPin =  13;
const int buttonPin = 2;

int buttonState = 0;
int ledState = LOW;

unsigned long previousMicros = 0;

const long dataRate = 50000;

//const int data[129] = {0,0,1,0,0,0,1,1,
//                      0,1,0,0,1,0,0,0,
//                      0,1,1,0,0,1,0,1,
//                      0,1,1,0,1,1,0,0,
//                      0,1,1,0,1,1,0,0,
//                      0,1,1,0,1,1,1,1,
//                      0,0,1,0,0,0,0,0,
//                      0,1,1,1,0,1,1,1,
//                      0,1,1,0,1,1,1,1,
//                      0,1,1,1,0,0,1,0,
//                      0,1,1,0,1,1,0,0,
//                      0,1,1,0,0,1,0,0,
//                      0,0,1,0,0,0,0,1,
//                      0,0,1,0,0,0,0,1,
//                      0,0,1,0,0,0,0,1,
//                      0,0,1,0,0,0,1,1,0};
//
//                      
//int dataIndex = 0;

void setup() {
  Serial.begin(115201);
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT);
}

void loop() {
  char inByte = Serial.read();
  if(inByte == '1') {
    ledState = HIGH;
//    delay(2.5);
//    ledState = LOW;
  } else if(inByte == '0'){
    ledState = LOW;
//    delay(2.5);
//    ledState = HIGH;
  }
//  unsigned long currentMicros = micros();
//
//    buttonState = digitalRead(buttonPin);
//    if(buttonState == HIGH) {
//      dataIndex = 0;
//    }
//
//  if (currentMicros - previousMicros >= dataRate) {
//    previousMicros = currentMicros;
//
//    if (data[dataIndex] == 1) {
//      ledState = HIGH;
//    } else {
//      ledState = LOW;
//    }
//
//    Serial.println(data[dataIndex]);
//    dataIndex += 1;
//    if (dataIndex >= 128) {
//      dataIndex = 0;
//    }
//
    digitalWrite(ledPin, ledState);
    delay(1);
//  }
}
