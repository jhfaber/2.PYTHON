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
HEADERS =settings.HEADER

URL_CONSULTA= '/rest/v4.9/plans/{}' #{clienteID}
ID='5'
URL = URL_API_PRODUCCION+(URL_CONSULTA.format(ID))






response = requests.get(URL,headers=HEADERS)
# data=dump.dump_all(response)
# print(data.decode('utf-8'))

content=print(response.content)
####################### DB ###########################


storage =json.loads(response.content)
# print(storage['id'])



            
string= '''INSERT INTO plan VALUES (
            \''''+str(storage['id'])+'''\',
            \''''+str(storage['planCode'])+'''\',
            \''''+str(storage['description'])+'''\',
            \''''+str(storage['accountId'])+'''\',
            \''''+str(storage['intervalCount'])+'''\',
            \''''+str(storage['interval'])+'''\',
            \''''+str(storage['maxPaymentsAllowed'])+'''\',
            \''''+str(storage['maxPaymentAttempts'])+'''\',
            \''''+str(storage['paymentAttemptsDelay'])+'''\',
            \''''+str(storage['maxPendingPayments'])+'''\',
            \''''+str(storage['trialDays'])+'''\'
            )
            '''

# print(string)
settings.DB.db.execute(string)
settings.DB.commit()
# settings.DB.selectData()
settings.DB.closeConnection()