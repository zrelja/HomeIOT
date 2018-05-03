#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"


WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, MQTT_SERVER, MQTT_SERVERPORT, MQTT_USERNAME, MQTT_KEY);
Adafruit_MQTT_Publish mqttcamera = Adafruit_MQTT_Publish(&mqtt, MQTT_CAMERA1_IP);
Adafruit_MQTT_Subscribe requestForCameraImage = Adafruit_MQTT_Subscribe(&mqtt, MQTT_CAMERA1);

bool MQTTConnect() {
  int8_t ret;

  if (mqtt.connected()) {
    return true;
  }
  Serial.print("Connecting to MQTT... ");

  uint8_t retries = 3;
  while ((ret = mqtt.connect()) != 0) { // connect will return 0 for connected
       Serial.println(mqtt.connectErrorString(ret));
       Serial.println("Retrying MQTT connection");
       mqtt.disconnect();
       delay(1000);  // wait 5 seconds
       retries--;
       if (retries == 0) {
         Serial.println("MQTT connection failed");
         return false;
       }
  }
  Serial.println("MQTT connected");
  return true;
}

void MQTTLoop()
{

  // Now we can publish stuff!
  //max 64kb
  /*if (!mqttcamera.publish(bmp, 66))
  {
    Serial.println(F("Failed"));
  } else {
    Serial.println(F("OK!"));
  }*/
}
