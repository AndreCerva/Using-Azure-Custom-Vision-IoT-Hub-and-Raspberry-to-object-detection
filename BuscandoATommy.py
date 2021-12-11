import cv2
from PIL import Image
from azure.iot.hub import IoTHubRegistryManager
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
credentials = ApiKeyCredentials(in_headers={"Prediction-key": "Your Prediction key"})
predictor = CustomVisionPredictionClient("Your End-Point", credentials)
CONNECTION_STRING = "Your Connection string IoT Hub"
DEVICE_ID = "ID device IoT Hub"
def iothub_messaging(data):
    try:
        registry_manager = IoTHubRegistryManager(CONNECTION_STRING)#Create IoTHubRegistryManager
        print ( 'Sending message... ' )
        registry_manager.send_c2d_message(DEVICE_ID, data)
        input("Message send, please press Enter...\n")
        im = Image.open('capture.png')
        im.show()
        exit(0)
    except Exception as ex:
        print ( "Unexpected error {0}" % ex )
        exit(1)
        return
    except KeyboardInterrupt:
        print ( "IoT Hub C2D Messaging service sample stopped" )
if __name__ == '__main__':
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
                cv2.destroyAllWindows()
                break#Sale del ciclo while
        else: #En caso de no poder capturar un fotograma
            print('Error al intentar ingresar a la camara')#Mostrar posible error de pq no se capturo fotograma
    with open("capture.png", mode="rb") as captured_image: #Abre la imagen guardada en formato de lectura
        results = predictor.detect_image("Your ID Proyect CV", "Proyect Name CV", captured_image)
    for prediction in results.predictions:
        if prediction.probability > 0.1:
            data='TOMMY HAS BEEN FOUND'
            print(prediction.probability)
            bbox = prediction.bounding_box
            result_image = cv2.rectangle(image, (int(bbox.left * 640), int(bbox.top * 480)), (int((bbox.left + bbox.width) * 640), int((bbox.top + bbox.height) * 480)), (0, 255, 0), 3)
            cv2.imwrite('capture.png', result_image)
            iothub_messaging(data)
        else:
            data='TOMMY HAS NOT BEEN FOUND YET'
            iothub_messaging(data)  
