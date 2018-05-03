# HomeIOT
Home automation with IOT, using networked ESP32 microcontroller

Hardware:

2 ESP32 microcontrollers<br/>
OV2640 camera<br/>
PIR sensor
Linux system with OpenHab2 and MQTT broker (also can be implemented on Windows or Mac)

Software folders:

esp32-motion - code for esp32 written in Arduino framework. If motion happens, MQTT event is published and catched by Openhab2
esp32-nofifo - code for connecting no fifo camera to esp32. Written in Arduino framework 
esp32-ov2640 - code for connecting ov2640 camero to esp32. Written in esp-idf (code by: https://github.com/igrr/esp32-cam-demo)
recognition api - tensorflow object detection (https://github.com/tensorflow/models/tree/master/research/object_detection) packed in Django server, available at API point /object_detection_api. Everything is inside docker container

