import RPi.GPIO as GPIO#librerias que nos permite trabajar con los pines de la rasp
import time #Libreria para tiempos de espera
from azure.iot.device import IoTHubDeviceClient#Libreria para hacer uso del servicio de Azure IoT Hub
GPIO.setwarnings(False)#No mostrar advertencias
#La siguiente connection_string se encuentra en el portal de azure en el registo del device
CONNECTION_STRING = "Aquí tu connection_string" #Aquí pegamos la cadena de conexion tomada desde nuestro portal de azure
pinledV=16 #Pin positivo al que ira conectado el led verde
pinledR=18 #Pin positivo al que ira conectado el led rojo
GPIO.setmode(GPIO.BOARD) #Numeraremos los pines del rasp con la numeración board (locación fisica)
GPIO.setup(pinledV,GPIO.OUT)#Indicamos que en el pin del led v estará mandando señal
GPIO.setup(pinledR,GPIO.OUT)#Indicamos que en el pin del led r estará mandando señal
#Funcion que imprime los mensajes recibidos en la consola
def message_handler(message): #Recibe el mensaje con todos sus atributos y metodos
  print("Message received\n")#Parametro message es una instancia de la clase Message, tiene varios atributos y metodos
  if message.data.decode() == 'TOMMY': #Si el mensaje que se envia es que se encontro a tommy
      GPIO.output(pinledR,GPIO.LOW) #Apagar el led rojo
      GPIO.output(pinledV,GPIO.HIGH) #Encender led verde
      print("Se ha encontrado a Tommy")
  else: #No se ha encontrado a tommy aún
      print("No se ha encontrado")
      GPIO.output(pinledV,GPIO.LOW) #Apagar led verde
      GPIO.output(pinledR,GPIO.HIGH) #encender led rojo
#Funcion para inicializar el cliente y esperar a recibir el mensaje de la nube al dispositivo
def main():
    GPIO.output(pinledR,GPIO.HIGH)# iniciamos en alto el led rojo que indica que no se ha encontrado aún
    GPIO.output(pinledV,GPIO.LOW) # Iniciamos en bajo el led verde 
    print ("Buscando a Tommy...")#indicamos que se empieza la busqueda
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)#instanciamos el cliente 
    print ("Esperando por un mensaje")#Estamos esperando algún mensaje
    try:
        # Attach the handler to the client
        client.on_message_received = message_handler#Leemos el mensaje que se ha enviado a nuestro device 
        while True: 
            time.sleep(1000) #mil segundos esperando un mensaje, por poner un numero, puede ser otro.
    except KeyboardInterrupt:
        print("IoT Hub C2D Messaging stopped") #se detiene la ejecución debido a una interrupción de teclado
    finally:
        GPIO.cleanup()
        print("Shutting down IoT Hub Client")#Terminamos con éxito la ejecución del programa
        client.shutdown()#Se deja de esperar el envio de mensajes
if __name__ == '__main__':
    main()
    
