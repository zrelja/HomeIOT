
#include <Arduino.h>
#include "wifiScan.h"
#define LED_BUILTIN 2

void setup()
{
  // initialize LED digital pin as an output.
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  wifiScan();
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
