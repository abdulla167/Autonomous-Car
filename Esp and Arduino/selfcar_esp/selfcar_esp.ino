#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ArduinoWebsockets.h>

//#define D0 16
//#define D1 5
//#define D2 4
//#define D3 0
//#define D4 2
//#define D5 14
//#define D6 12
//#define D7 13
//#define D8 15


String readStringArduino(void);

//SoftwareSerial arduinoSerial(D3, D4);
String arduinoData = "";

const char* ssid = "drwesh-Latitude-E7450";
const char* password = "CSqgoXNi";

const char* websocketUri = "ws://10.42.0.1:8080/esp";
const char* websocketUriMobile = "ws://10.42.0.134:38301/";
unsigned long i = 0;

using namespace websockets;

WebsocketsClient client;

WebsocketsClient clientMobile;

void setup() {
  Serial.begin(115200);
  //  arduinoSerial.begin(115200);
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);


  while ((WiFi.status() != WL_CONNECTED) )
  {
    Serial.print(".");
    delay(200);
  }
  Serial.println("");
  Serial.print("Coneccted, IP: ");
  Serial.println(WiFi.localIP());

  Serial.println("Connecting to server...");

  bool connected = client.connect(websocketUri);
  if (connected) {
    Serial.println("Connecetd to server");
    client.send("Hello Server");
  } else {
    Serial.println("Not Connected to server!");
  }

  connected =  clientMobile.connect(websocketUriMobile);

  if (connected) {
    Serial.println("Connecetd to Mobile");
    clientMobile.send("esp");
  } else {
    Serial.println("Not Connected to Mobile");
  }

  

  client.onMessage([](WebsocketsMessage message) {
    String recieved_data = message.data();
    if(recieved_data == "auto"){
      clientMobile.send("auto");
      delay(2);
      return;
    }
    Serial.write(recieved_data.c_str());
    delay(5);
  });

  clientMobile.onMessage([](WebsocketsMessage message) {
    String recieved_data = message.data();
    client.send(recieved_data);
    Serial.write(recieved_data.c_str());
    delay(5);
  });
}

void loop() {
  arduinoData = readStringArduino();
  delay(3);
  if (arduinoData != "0"){
    client.send(arduinoData);
  }
  
  if (client.available()) {
    client.poll();
  }

  if (clientMobile.available()) {
    clientMobile.poll();
  }

  
}

String readStringArduino() {
  String dataRecieved = "";
  char chBuffer;
  while (Serial.available() > 0) {
    chBuffer =  (char) Serial.read();
        dataRecieved += chBuffer;
        if (chBuffer == '\0') {
          return dataRecieved;
        }
  }
  return "0";
} 
