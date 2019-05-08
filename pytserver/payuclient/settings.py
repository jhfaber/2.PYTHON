""" implementacion pagos recurrentes
1- Crear plan
2- Crear cliente
3- Crear tarjeta de credito
4- Suscripcion (relacion entre un plan de pagos, un pagador y una tarjeta de credito)
5- Cargos adicionales (Pagos o descuentos sobre uno de los pagos que conforman el plan de pagos recurrentes)
6- Facturas (intento de pago sobre suscripcion)

 """

import json, os
import base64

CONF = '\\config.json'
cwd = os.path.dirname(os.path.realpath(__file__)) + CONF
with open(cwd, 'r') as file:
    config = json.load(file)

API_KEY = config['DEFAULT']['API_KEY']
API_LOGIN = config['DEFAULT']['API_LOGIN']
ACCOUNDTID = config['DEFAULT']['ACCOUNTID']
HOST = config['HOST']['HOST']
URL = config['HOST']['URL']
ENCODED = base64.b64encode(bytes(API_LOGIN+':'+API_KEY,'utf-8')).decode("utf-8")
HEADER = { 
        "Host": HOST,
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json",
        "Accept-language": "es",
        "Content-Length": "length",
        "Authorization": "Basic "+ENCODED,
}

# print(ENCODED+URL+HOST+ACCOUNDTID+API_KEY+API_LOGIN)