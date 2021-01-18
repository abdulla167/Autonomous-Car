#include <SoftwareSerial.h>
#include <SPI.h>
#include <MFRC522.h>


#define SS_PIN 10
#define RST_PIN 9

#define ENABLE_L 6
#define HIGH_L 18
#define LOW_L 19

#define ENABLE_R 5
#define HIGH_R 16
#define LOW_R 17

MFRC522 mfrc522(SS_PIN, RST_PIN);
SoftwareSerial espSerial(3, 4);
char espData = '0';

char readStringEsp();
void forward(void);
void backward(void);

void setup() {
  Serial.begin(115200);
  espSerial.begin(115200);
  pinMode(ENABLE_R, OUTPUT);
  pinMode(ENABLE_L, OUTPUT);
  pinMode(HIGH_R, OUTPUT);
  pinMode(LOW_R, OUTPUT);
  pinMode(HIGH_L, OUTPUT);
  pinMode(LOW_L, OUTPUT);

  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
}

void loop() {
  espData = readStringEsp();

  if (espData == 'F') {
    forward();
  }
  else  if (espData == 'B') {
    backward();
  }

  else  if (espData == 'R') {
    right();
  }
  else  if (espData == 'L') {
    left();
  }
  else  if (espData == 'G') {
    forwardRight();
  }
  else  if (espData == 'H') {
    backwardRight();
  }
  else  if (espData == 'I') {
    backwardLeft();
  }
  else  if (espData == 'J') {
    forwardLeft();
  }

  else {
    analogWrite(ENABLE_L, 0);
    analogWrite(ENABLE_R, 0);
  }

  // Look for new cards
  if (! mfrc522.PICC_IsNewCardPresent())
  {
    return;
  }
  // Select one of the cards
  if (! mfrc522.PICC_ReadCardSerial())
  {
    return;
  }
  //Show UID on serial monitor
  Serial.print("UID tag :");
  String content = "";

  //  for (byte i = 0; i < mfrc522.uid.size; i++)
  //  {
  //    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
  //    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  //  }

  Serial.print("Message :");
  content.toUpperCase();
  if (content.substring(1) == "96 1D 17 7E") { //change here the UID of the card/cards that you want to give access
    Serial.println("96 1D 17 7E");
    espSerial.write("96 1D 17 7E", 12);
    delay(10);
  }
}

void forward(void) {

  digitalWrite(HIGH_L, HIGH);
  digitalWrite(LOW_L, LOW);
  analogWrite(ENABLE_L, 100);

  digitalWrite(HIGH_R, LOW);
  digitalWrite(LOW_R, HIGH);
  analogWrite(ENABLE_R, 100);
}

void backward(void) {
  digitalWrite(HIGH_L, LOW);
  digitalWrite(LOW_L, HIGH);
  analogWrite(ENABLE_L, 80);

  digitalWrite(HIGH_R, HIGH);
  digitalWrite(LOW_R, LOW);
  analogWrite(ENABLE_R, 80);
}

void right(void) {
  digitalWrite(HIGH_L, LOW);
  digitalWrite(LOW_L, HIGH);
  analogWrite(ENABLE_L, 100);

  digitalWrite(HIGH_R, LOW);
  digitalWrite(LOW_R, HIGH);
  analogWrite(ENABLE_R, 100);
}

void left(void) {

  digitalWrite(HIGH_L, HIGH);
  digitalWrite(LOW_L, LOW);
  analogWrite(ENABLE_L, 100);

  digitalWrite(HIGH_R, HIGH);
  digitalWrite(LOW_R, LOW );
  analogWrite(ENABLE_R, 100);
}

void forwardRight(void) {
  digitalWrite(HIGH_L, HIGH);
  digitalWrite(LOW_L, LOW);
  analogWrite(ENABLE_L, 115);

  digitalWrite(HIGH_R, LOW);
  digitalWrite(LOW_R, HIGH);
  analogWrite(ENABLE_R, 0);
}


void forwardLeft(void) {
  digitalWrite(HIGH_L, HIGH);
  digitalWrite(LOW_L, LOW);
  analogWrite(ENABLE_L, 0);

  digitalWrite(HIGH_R, LOW);
  digitalWrite(LOW_R, HIGH);
  analogWrite(ENABLE_R, 115);
}


void backwardRight(void) {
  digitalWrite(HIGH_L, LOW);
  digitalWrite(LOW_L, HIGH);
  analogWrite(ENABLE_L, 75);

  digitalWrite(HIGH_R, HIGH);
  digitalWrite(LOW_R, LOW);
  analogWrite(ENABLE_R, 105);
}

void backwardLeft(void) {
  digitalWrite(HIGH_L, LOW);
  digitalWrite(LOW_L, HIGH);
  analogWrite(ENABLE_L, 105);

  digitalWrite(HIGH_R, HIGH);
  digitalWrite(LOW_R, LOW);
  analogWrite(ENABLE_R, 75);
}

void _stop() {
  analogWrite(ENABLE_L, 0);
  analogWrite(ENABLE_R, 0);
}

char readStringEsp() {
  //  String dataRecieved = "";
  //  char chBuffer;
  if (espSerial.available() > 0) {
    //    chBuffer =  (char) espSerial.read();
    //    dataRecieved += chBuffer;
    //    if (chBuffer == '\0') {
    //      return dataRecieved;
    //    }
    return (char) espSerial.read();
  }
  return '0';
}
