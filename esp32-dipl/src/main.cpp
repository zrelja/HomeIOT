
#include <Arduino.h>
#include "wifi.h"
#define LED_BUILTIN 2
#include <WiFi.h>

const char* ssid     = "Vip WLAN_8BD492";
const char* password = "DBBDBBEBCE";

void setup()
{
  // initialize LED digital pin as an output.
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  wifiScan();
  Serial.print("Connecting to ");
  Serial.print(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.print(".");
  }

  Serial.println("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
}

void loop()
{

  // turn the LED on (HIGH is the voltage level)
  digitalWrite(LED_BUILTIN, HIGH);
  // wait for a second
  delay(1000);
  // turn the LED off by making the voltage LOW
  digitalWrite(LED_BUILTIN, LOW);
  Serial.println("Blink");

   // wait for a second
  delay(1000);
}
