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
import json
from requests_toolbelt.utils import dump
import settings


URL_API_PRODUCCION = settings.URL
ENCODED= settings.ENCODED
API_LOGIN = settings.API_LOGIN
API_KEY= settings.API_KEY
HOST= settings.HOST

URL_CREACION= 'rest/v4.9/customers/'
URL_CONSULTA= 'rest/v4.9/customers/{}' #{clienteID}
ID='284aa042ejtn'
URL = URL_API_PRODUCCION+(URL_CONSULTA.format(ID))
HEADERS =settings.HEADER



# ENCODED = base64.b64encode(bytes(API_LOGIN+':'+API_KEY,'utf-8')).decode("utf-8")

##############BUILD BODY#################




# print(json.dumps(data, indent=4))
################### ENVIO POST ######################
response = requests.get(URL, headers= HEADERS)
content=print(response.content)

########################## IMPRIMIR LO QUE ENVIO Y RECIBO###############
# res=dump.dump_all(response)
# print(res.decode('utf-8'))




############################### DB ###########################
""" storage =json.loads(response.content)
string= '''INSERT INTO cliente VALUES (
            \''''+str(storage['id'])+'''\'
            )'''

# print(string)
settings.DB.db.execute(string)
settings.DB.commit()
settings.DB.closeConnection() """


