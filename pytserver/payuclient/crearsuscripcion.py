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

URL_CREACION= 'rest/v4.9/subscriptions/' 
URL_CONSULTA= 'rest/v4.9/subscriptions/{}' #{susbcripcionID}

#OBLIGATORIOS
ID_CLIENTE='fdaccycyj8x2'
TOKEN = '748a8731-e39f-4671-8920-16318c1c3158'
PLAN_CODE = "888"

#URL
URL = URL_API_PRODUCCION+URL_CREACION

##############BUILD BODY#################
data = {
            "quantity": "1",
            "installments": "1",
            "trialDays": "1",   
            #'immediatePayment': "true"                              
                
        }
customer = {
    "id": ID_CLIENTE,
}
creditCards = [{
    "token": TOKEN,
}]
customer['creditCards'] = creditCards
plan= {
    "planCode": PLAN_CODE
}
data['customer'] =customer
data['plan']= plan

############################# BUILD POST HEADERS ############################

data= json.dumps(data)


################### ENVIO POST ######################
response = requests.post(URL, data= data, headers= HEADERS)
content=print(response.content)

###############################DB ########################3
diccionario =json.loads(response.content)
settings.DB.crearSuscripcion(diccionario)



