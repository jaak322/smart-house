#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <HttpClient.h>
#include <ESP8266WebServer.h>
#include <Servo.h> // including servo library.
#include <LiquidCrystal.h>
#include<SoftwareSerial.h>
#define lightPin D0
#define buzzerPin D1
#define servoPin D2
#define lightWarningPin D3
#define tempPin A0
//const int RS = D6, EN =  D0, d4 = D2 , d5 = D4 , d6 = D8, d7 = D9;
//LiquidCrystal lcd(RS, EN, d4, d5, d6, d7);
/* Set these to your desired credentials. */
const char *ssid = "networkName"; //Enter your WIFI ssid
const char *password = "pass"; //Enter your WIFI password
HttpClient httpClient;
SoftwareSerial nodeMcu(D6,D5);
const uint16_t port = 1234;
const char * host = "host";
ESP8266WebServer server(80);   
WiFiClient client;
float sensorValue;
float voltageOut;
float temperatureC;
float temperatureF;
Servo servo_1; // Giving name to servo.

void handleRoot() {
 server.send(200, "text/html", "<form action=\"/LED_BUILTIN_on\" method=\"get\" id=\"form1\"></form><button type=\"submit\" form=\"form1\" value=\"On\">On</button><form action=\"/LED_BUILTIN_off\" method=\"get\" id=\"form2\"></form><button type=\"submit\" form=\"form2\" value=\"Off\">Off</button>");
}
void handleSave() {
 if (server.arg("pass") != "") {
   Serial.println(server.arg("pass"));
 }
}
void setup() {
 servo_1.attach(servoPin); // Attaching Servo to D3
   nodeMcu.begin(115200);
   Serial.begin(115200);
  pinMode(lightPin, OUTPUT);
  pinMode(lightWarningPin,OUTPUT);
  pinMode(tempPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
// Temporery ESP SERVER

// delay(3000);
// Serial.begin(115200);
// Serial.println();
// Serial.print("Configuring access point...");
// WiFi.begin(ssid, password);
// while (WiFi.status() != WL_CONNECTED) {
//   delay(500);
//   Serial.print(".");
// }
// Serial.println("");
// Serial.println("WiFi connected");
// Serial.println("IP address: ");
// Serial.println(WiFi.localIP());
// server.on ( "/", handleRoot );
// server.on ("/save", handleSave);
// server.begin();
// Serial.println ( "HTTP server started" );
// server.on("/LED_BUILTIN_off", []() {
//  digitalWrite(lightPin, 0);
//  Serial.println("off");
//  handleRoot();
//});
//
// server.on("/LED_BUILTIN_on", []() {
//  digitalWrite(lightPin, 1);
//   Serial.println("on");
//   handleRoot();
//   });

  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }

  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
}
void loop() {
// Read Senso value
    sensorValue = analogRead(tempPin);
    // calculate temperature in Degree Celsius 
    temperatureC = ((sensorValue * 5.0) / 1024)*100.0-100;
    // calculate temperature in Fahrenheit
    temperatureF = (temperatureC * 1.8) + 32;
    // Print temperature values on Serial Monitor Window
    Serial.println("Temperature(ºC): ");
    Serial.println(temperatureC);
    String dataToSend = String(temperatureC);
    nodeMcu.println ("C:"+dataToSend);
    nodeMcu.println();
    Serial.println("Temperature(ºF): ");
    Serial.println(temperatureF);
    String dataToSend1 = String(temperatureF);
    nodeMcu.println("F:"+dataToSend1);
  delay(1000);
 if (client.connect(host, port))
  {
    Serial.print("Connected to host: ");
    Serial.println(host);
    //i tell the server i'm ready for data
    client.println("Connected");
    client.println(temperatureC);
    client.println(temperatureF);
    Serial.print("Wating for data");
    int i = 0;
    while(true){
      if(client.available() == 0){
        Serial.print(".");
        i++;
        if(i >= 10){
          break;
        }
        delay(10);
      } else {
         Serial.print("\nData received: ");
         digitalWrite(lightPin,client.read());
         int doorRead= client.read();
         if (doorRead==1){
          openDoor();
          }
          else{
            closeDoor();
            }
            if(temperatureC>20)
            {
              digitalWrite(lightWarningPin,1);
              tone(buzzerPin,5000,3000);
              }else{
                digitalWrite(lightWarningPin,0);
                noTone(buzzerPin);
                }
         Serial.println(doorRead);
        client.stop();
         Serial.println("Client disconnected");
      }
// server.handleClient();

 }
  }
}
void Forward() 
 {
    digitalWrite(D5,HIGH);
    digitalWrite(D6,LOW);
    delay(200);
  }
   void Backward()
  {
    digitalWrite(D6, HIGH);
    digitalWrite(D5,LOW);
    delay(200); 
  }
  void openDoor(){
    servo_1.write (0); // Servo will move to degree angle.
    }
 void closeDoor(){
    servo_1.write (180); // Servo will move to degree angle.
    }
