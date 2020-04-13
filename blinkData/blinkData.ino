const int ledPin =  13;
const int buttonPin = 2;

int buttonState = 0;
int ledState = LOW;

unsigned long previousMicros = 0;

const long dataRate = 100000;

const int data[113] = {0,0,0,0,0,0,0,0,
                      0,1,0,0,1,0,0,0,
                      0,1,1,0,0,1,0,1,
                      0,1,1,0,1,1,0,0,
                      0,1,1,0,1,1,0,0,
                      0,1,1,0,1,1,1,1,
                      0,0,1,0,0,0,0,0,
                      0,1,0,1,0,1,1,1,
                      0,1,1,0,1,1,1,1,
                      0,1,1,1,0,0,1,0,
                      0,1,1,0,1,1,0,0,
                      0,1,1,0,0,1,0,0,
                      0,0,1,0,0,0,0,1,
                      0,0,0,0,0,0,0,0,0};
int dataIndex = 0;

void setup() {
  Serial.begin(19200);
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT);
}

void loop() {
  unsigned long currentMicros = micros();
  
  buttonState = digitalRead(buttonPin);
  if(buttonState == HIGH) {
    dataIndex = 0;
  }

  if (currentMicros - previousMicros >= dataRate) {
    previousMicros = currentMicros;

    Serial.println(data[dataIndex]);
    if (data[dataIndex] == 1) {
      ledState = HIGH;
    } else {
      ledState = LOW;
    }
    dataIndex+= 1;
    if(dataIndex >= 112) {
      dataIndex = 0;
    }

    digitalWrite(ledPin, ledState);
  }
}
