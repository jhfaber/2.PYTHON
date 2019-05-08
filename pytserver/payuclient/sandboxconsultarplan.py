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
import base64
from requests_toolbelt.utils import dump


url= 'https://sandbox.api.payulatam.com/payments-api/rest/v4.9/plans/873468933'


headers = { 
        "Host": "sandbox.api.payulatam.com",
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json",
        "Accept-language": "es",
        "Content-Length": "length",
        "Authorization": "Basic cFJSWEtPbDhpa01tdDl1OjRWajhlSzRybG9VZDI3Mkw0OGhzcmFyblVB",
}





response = requests.get(url,headers=headers)
data=dump.dump_all(response)
print(data.decode('utf-8'))

content=print(response.content)