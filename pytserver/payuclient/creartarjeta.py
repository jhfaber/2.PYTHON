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
# from requests_toolbelt.utils import dump

URL_API_PRODUCCION = settings.URL
ENCODED= settings.ENCODED
API_LOGIN = settings.API_LOGIN
API_KEY= settings.API_KEY
HOST= settings.HOST
ACCOUNDTID =settings.ACCOUNDTID
HEADERS =settings.HEADER

URL_CREACION= 'rest/v4.9/customers/{}/creditCards' #{clienteID}
URL_CONSULTA= 'rest/v4.9/creditCards/{}' #{creditCard}

#OBLIGATORIOS
ID_CLIENTE='7b5951r6hwk3'

URL = URL_API_PRODUCCION+(URL_CREACION.format(ID_CLIENTE))


##############BUILD BODY#################
data = {
            "name": "TEST E-DENTALSYS",
            "document": "1020304050",
            "number": "4323592726185547",
            "expMonth": "03",
            "expYear": "2020",
            "type": "VISA",                           
                
        }

address={}
address= {
            "line1": "Address Name",
            "line2": "17 25",
            "line3": "Of 301",
            "postalCode": "00000",
            "city": "City Name",
            "state": "State Name",
            "country": "CO",
            "phone": "300300300"
        }
data['address']=address

# print(json.dumps(data, indent=4))
############################# BUILD POST HEADERS ############################


data= json.dumps(data)


################### ENVIO POST ######################
response = requests.post(URL, data= data, headers= HEADERS)
content=print(response.content)





###############################DB ########################3
diccionario =json.loads(response.content)

settings.DB.crearTarjeta(diccionario)



