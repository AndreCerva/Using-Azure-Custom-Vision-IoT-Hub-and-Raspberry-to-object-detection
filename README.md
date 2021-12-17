# Using-Azure-Custom-Vision-IoT-Hub-and-Raspberry-to-object-detection
In this proyect we use the service of Azure Custom vision and IoT Hub to object detection with the SDK of Python of Custom Vision object detection, and the SDK of Azure IoT Hub to comunication C2D from our computer to a Raspberry Pi

*Consideraciones de codigo de BuscandoATommy.py*

Se requiere instalar las siguientes librerias para su correcto funcionamiento:
* pip install opencv-python
* pip install azure-cognitiveservices-vision-customvision
* pip install msrest

Tener en cuenta la relación de aspecto de la imagen cuando se modifique su tamaño

*Consideraciones de codigo de RaspDevice.py*

Se requiere instalar las siguientes librerias:
* sudo pip install azure-iot-hub
    *En caso de no tener instalado la libreria GPIO*
    * sudo apt-get update.
    * sudo apt-get upgrade.
    * sudo apt-get install python-dev.
    * sudo apt-get install pyton-rpi. gpio.

Para la elección de los pines, mediante la numeración locación fisica, ver GPIO_RASP3B.png o equivalente a tu modelo de Rasp