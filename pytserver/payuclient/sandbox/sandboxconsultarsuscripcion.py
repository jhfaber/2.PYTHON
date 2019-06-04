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
HEADERS =settings.HEADER

URL_CREACION= 'rest/v4.9/subscriptions/' 
URL_CONSULTA= 'rest/v4.9/subscriptions/{}' #{susbcripcionID}
# ID_CLIENTE='a44a4fudq8by'
# TOKEN = 'fb5f927c-0f59-44fc-955e-d5989b4cf1c4'
# T_NUMERO='4323592726185547'
# PLAN_CODE = "22"
ID_SUSCRIPCION= 'cd508mgib217'
URL = URL_API_PRODUCCION+(URL_CONSULTA.format(ID_SUSCRIPCION))

print(URL)

################### ENVIO POST ######################
response = requests.get(URL, headers= HEADERS)
content=print(response.content)

settings.beauty_print(response)



