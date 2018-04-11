#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library

#include <WiFi.h>
#include <WiFiMulti.h>
#include <WiFiClient.h>
//#define USE_MQTT

int pirPin = 35;
int calibrationTime = 30;

// wifi creds
//ured
#define ssid1        "Tehnoloski_park_Zagreb"
#define password1    "TpZ232!Raza"
//#define ssid1        "blabla"
//#define password1    "hajduk1950"
/*
//mqtt credentials
#ifdef USE_MQTT
  #define MQTT_SERVER      "192.168.254.252"
  #define MQTT_SERVERPORT  1883
  #define MQTT_USERNAME    "zvonimir"
  #define MQTT_KEY         "zadvarje"
  #define MQTT_CAMERA1      "iot/camera/1"
  #define MQTT_CAMERA1_IP      "iot/camera/ip/1"
  #include "MQTTStuff.h"
#endif
*/

WiFiMulti wifiMulti;
WiFiServer server(80);


void setup()
{

  pinMode(pirPin, INPUT);
  digitalWrite(pirPin, LOW);

  Serial.print("calibrating sensor ");
    for(int i = 0; i < calibrationTime; i++){
      Serial.print(".");
      delay(1000);
      }
    Serial.println(" done");
    Serial.println("SENSOR ACTIVE");
    delay(50);


  Serial.begin(115200);
  wifiMulti.addAP(ssid1, password1);
  //wifiMulti.addAP(ssid2, password2);
  Serial.println("Connecting Wifi...");
  if(wifiMulti.run() == WL_CONNECTED) {
      Serial.println("");
      Serial.println("WiFi connected");
      Serial.println("IP address: ");
      Serial.println(WiFi.localIP());
  }

  int retry = 3;
  Serial.println(WiFi.localIP());
  // subscribe to "iot/camera/frontDoorCamera" if somebody sends message you will now
//  mqtt.subscribe(&requestForCameraImage);

  //MQTTConnect();

  server.begin();
  Serial.println("server begin");
}


void loop()
{
  delay(1400);
Serial.println(digitalRead(pirPin));
digitalWrite(pirPin, LOW);
delay(1400);
Serial.println(digitalRead(pirPin));

}
