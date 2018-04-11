#include "OV7670.h"

#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library

#include <WiFi.h>
#include <WiFiMulti.h>
#include <WiFiClient.h>
#include "BMP.h"
#define USE_MQTT

const int SIOD = 25; //SDA
const int SIOC = 23; //SCL

const int VSYNC = 22;
const int HREF = 26;

const int XCLK = 27;
const int PCLK = 21;

const int D0 = 35;
const int D1 = 17;
const int D2 = 34;
const int D3 = 5;
const int D4 = 39;
const int D5 = 18;
const int D6 = 36;
const int D7 = 19;


// wifi creds
//ured
#define ssid1        "Tehnoloski_park_Zagreb"
#define password1    "TpZ232!Raza"
//#define ssid1        "blabla"
//#define password1    "hajduk1950"

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

OV7670 *camera;

WiFiMulti wifiMulti;
WiFiServer server(80);

unsigned char bmpHeader[BMP::headerSize];

void serve()
{
    Serial.println("serviram");
  WiFiClient client = server.available();
  if (client)
  {
    Serial.println("New Client.");
    String currentLine = "";
    while (client.connected())
    {
      if (client.available())
      {
        char c = client.read();
        Serial.write(c);
        if (c == '\n')
        {
          if (currentLine.length() == 0)
          {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();
            client.print(
              "<style>body{margin: 0}\nimg{height: 100%; width: auto}</style>"
              "<img id='a' src='/camera' onload='this.style.display=\"initial\"; var b = document.getElementById(\"b\"); b.style.display=\"none\"; b.src=\"camera?\"+Date.now(); '>"
              "<img id='b' style='display: none' src='/camera' onload='this.style.display=\"initial\"; var a = document.getElementById(\"a\"); a.style.display=\"none\"; a.src=\"camera?\"+Date.now(); '>");
            client.println();
            break;
          }
          else
          {
            currentLine = "";
          }
        }
        else if (c != '\r')
        {
          currentLine += c;
        }

        if(currentLine.endsWith("GET /camera"))
        {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:image/bmp");
            client.println();

            for(int i = 0; i < BMP::headerSize; i++)
               client.write(bmpHeader[i]);
            for(int i = 0; i < camera->xres * camera->yres * 2; i++)
               client.write(camera->frame[i]);
        }
      }
    }
    // close the connection:
    client.stop();
    Serial.println("Client Disconnected.");
  }
}

void setup()
{
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
  mqtt.subscribe(&requestForCameraImage);
  MQTTConnect();


  camera = new OV7670(OV7670::Mode::QQVGA_RGB565, SIOD, SIOC, VSYNC, HREF, XCLK, PCLK, D0, D1, D2, D3, D4, D5, D6, D7);
  BMP::construct16BitHeader(bmpHeader, camera->xres, camera->yres);
  server.begin();
  Serial.println("server begin");
}


void loop()
{  int retry = 3;

    // waiting for a message on "iot/camera/frontDoorCamera"
    Adafruit_MQTT_Subscribe *subscription;
    while ((subscription = mqtt.readSubscription(5000))) {
      if (subscription == &requestForCameraImage) {
        Serial.print("signal primljen\n");
         delay(500);
        Serial.println((char *)requestForCameraImage.lastread);
        if(mqttcamera.publish(WiFi.localIP().toString().c_str()))
        {
          Serial.println("IP address sent");
        }
      //  Serial.println((char*)tCommand.lastread);
      }
    }

/*  Serial.println(WiFi.localIP());

  camera->oneFrame();
  Serial.println("kamera slikana");
  Serial.println(WiFi.localIP());

  serve();
*/
}
