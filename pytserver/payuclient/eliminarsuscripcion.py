""" implementacion pagos recurrentes
1- Crear plan
2- Crear cliente
3- Crear tarjeta de credito
4- Suscripcion (relacion entre un plan de pagos, un pagador y una tarjeta de credito)
5- Cargos adicionales (Pagos o descuentos sobre uno de los pagos que conforman el plan de pagos recurrentes)
6- Facturas (intento de pago sobre suscripcion)

 """


print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")



import requests
import json, settings


URL_API_PRODUCCION = settings.URL
ENCODED= settings.ENCODED
API_LOGIN = settings.API_LOGIN
API_KEY= settings.API_KEY
HOST= settings.HOST
ACCOUNDTID =settings.ACCOUNDTID
HEADERS =settings.HEADER


#OBLIGATORIO
ID= 'f82dabxg9jv0'
URL_ELIMINAR= '/rest/v4.9/subscriptions/{}'

#URL
URL = URL_API_PRODUCCION+(URL_ELIMINAR.format(ID))


################### ENVIO ######################
response = requests.delete(URL, headers= HEADERS)
content=print(response.content)

###############################DB ########################3
# diccionario =json.loads(response.content)
settings.DB.eliminarSuscripcion(ID)



