import cv2#Libreria OpenCV para procesamiento de imagenes(Visión artificial)
from PIL import Image#Python Imaging Library, libreria para la edición y manipulación de imagenes
from azure.iot.hub import IoTHubRegistryManager #Libreria de Azure para IoT Hub
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient#Libreria de Azure para Custom Vision service
from msrest.authentication import ApiKeyCredentials#Libreria de Azure para autenticar credenciales de servicio
credentials = ApiKeyCredentials(in_headers={"Prediction-key": "Your Prediction key"})#La clave para hacer uso del servicio de custom vision desplegado
predictor = CustomVisionPredictionClient("Your End-Point", credentials)#Endpoint donde se encuentra nuestro servicio de custom vision desplegado
CONNECTION_STRING = "Your Connection string IoT Hub"#Cadena de conección para el servicio de Azure IoT Hub.
DEVICE_ID = "ID device IoT Hub"#ID con el que se ha registrado el dispositivo con el que se va a comunicar
def iothub_messaging(data):#Función para enviar mensaje a nuestro dispositivo, recibe como parametro la información a mandar
    try:
        registry_manager = IoTHubRegistryManager(CONNECTION_STRING)#Creamos un IoTHubRegistryManager que nos permitira mandar el mensaje a nuestro dispositivo
        print ( 'Sending message... ' )#Indicamos en consola que estamos mandando el mensaje
        registry_manager.send_c2d_message(DEVICE_ID, data)#Con ayuda del metodo enviamos un mensaje dando como parametro el dispositivo y el mensaje
        input("Message send, please press Enter...\n")#Avisamos que hemos enviado el mensaje a nuestro dispositivo correctamente
        im = Image.open('capture.png')#Abrimos la imagen que capturamos y mandamos al servicio de custom vision
        im.show()#Mostramos la imagen que abrimos
        exit(0)#Terminamos el programa con exito
    except Exception as ex:#En caso de no poder enviar el mensaje se abre la excepción
        print ( "Unexpected error {0}" % ex )#Se muestra que no se pudo mandar el mensaje por el inesperado error
        exit(1)#Se termina el programa con error
        return
    except KeyboardInterrupt:#Excepción debida a interrupción por teclado ctrl c 
        print ( "IoT Hub C2D Messaging service sample stopped" )#Mostramos en pantalla pq se detuvo la ejecución del script
if __name__ == '__main__':#Cuando se inicie la ejecución del programa, entrara a este condicional
    camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)#abrir la cámara y completar la inicialización de la cámara
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)#Cambiamos el ancho de la imagen 
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)#Cambiamos la altura de la imagen
    while (camera.isOpened()):#detectar si la inicialización se realizó correctamente
        ret, image = camera.read() #capturar fotogramas, image devuelve el fotograma capturado, ret true si es éxitoso la captura
        if ret== True:#Si se ha capturado correctamente el fotograma
            cv2.imshow('video',image)#Mostrar la serie de fotogramas que se están tomando
            if cv2.waitKey(1) & 0xFF == ord('t'):#Si se preciona la tecla: t , entra al condicional
                cv2.imwrite('capture.png', image)#Se guarda el fotograma cuando se presiono la tecla
                camera.release()#Apaga la camara
                cv2.destroyAllWindows()#Destruir todas las ventanas que se hayan mostrado anteriormente con cv2
                break#Sale del ciclo while
        else: #En caso de no poder capturar un fotograma
            print('Error al intentar ingresar a la camara')#Mostrar posible error de pq no se capturo fotograma
    with open("capture.png", mode="rb") as captured_image: #Abre la imagen guardada en formato de lectura
        results = predictor.detect_image("Your ID Project CV", "Project Name CV", captured_image)#Se envia la imagen tomada con el id y el nombre del proyecto
    for prediction in results.predictions:#Se miran todas las predicciones hechas por Azure almacenadas en results cuando enviamos la imagen
        if prediction.probability > 0.1:#Para todas las predicciones que se hayan tenido que sean mayores a un 50% de seguridad
            print(prediction.probability)#Imprime el porcentaje de seguridad con la que está de que es tommy
            bbox = prediction.bounding_box#Cuadros delimetadores que se obtienen de la predicción
            #Para los cuadros delimitadores, hacemos un cálculo simple basado en el tamaño de la imagen, establecemos el color del cuadro delimitador y el grosor del borde. 
            #Dibujamos estos cuadros delimetadores en la imagen
            result_image = cv2.rectangle(image, (int(bbox.left * 640), int(bbox.top * 480)), (int((bbox.left + bbox.width) * 640), int((bbox.top + bbox.height) * 480)), (0, 255, 0), 3)
            cv2.imwrite('capture.png', result_image)#Se guarda la imagen que se mando al servicio de custom vision
            iothub_messaging('TOMMY HAS BEEN FOUND')#Envia el mensaje al dispositivo de que se ha encontrado a tommy 
        else:
            iothub_messaging('TOMMY HAS NOT BEEN FOUND YET')#Envia el mensaje de que no se ha encontrado a Tommy
