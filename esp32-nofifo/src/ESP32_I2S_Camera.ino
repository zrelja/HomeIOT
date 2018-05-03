#include "OV7670.h"

#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library

#include <WiFi.h>
#include <WiFiMulti.h>
#include <WiFiClient.h>
#include "BMP.h"
#define USE_MQTT

const int SIOD = 26; //SDA
const int SIOC = 27; //SCL

const int VSYNC = 25;
const int HREF = 23;

const int XCLK = 21;
const int PCLK = 22;

const int D0 = 4;
const int D1 = 5;
const int D2 = 18;
const int D3 = 19;
const int D4 = 36;
const int D5 = 39;
const int D6 = 34;
const int D7 = 35;


// wifi creds
//ured
#define ssid1        "Tehnoloski_park_Zagreb"
#define password1    "TpZ232!Raza"
//#define ssid1        "blabla"
//#define password1    "hajduk1950"

//#define ssid1        "Vip WLAN_8BD492"
//#define password1    "DBBDBBEBCE"

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
  Serial.println(client);

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

  server.begin();
  Serial.println("server begin");

  camera = new OV7670(OV7670::Mode::QQQVGA_RGB565, SIOD, SIOC, VSYNC, HREF, XCLK, PCLK, D0, D1, D2, D3, D4, D5, D6, D7);

  BMP::construct16BitHeader(bmpHeader, camera->xres, camera->yres);

  Serial.println("Setup done");

}

void loop()
{
  Serial.println(WiFi.localIP());

  camera->oneFrame();
  Serial.println("kamera slikana");
  Serial.println(WiFi.localIP());
  serve();

}
