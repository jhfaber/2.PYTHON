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
from requests_toolbelt.utils import dump

URL_API_PRODUCCION = settings.URL
ENCODED= settings.ENCODED
API_LOGIN = settings.API_LOGIN
API_KEY= settings.API_KEY
HOST= settings.HOST
ACCOUNDTID =settings.ACCOUNDTID
HEADERS =settings.HEADER

URL_CREACION= 'rest/v4.9/plans'
URL_CONSULTA = '/rest/v4.9/plans/{planCode}'
URL_CREAR_PLAN = URL_API_PRODUCCION+URL_CREACION
# print(URL_CREAR_PLAN)

ID_CODE= "5"

##############BUILD POST BODY#################
data = {
                "accountId": ACCOUNDTID,
                "planCode": ID_CODE,
                "description": "nnmm",
                "interval": "MONTH",
                "intervalCount": "1",
                "maxPaymentsAllowed": "12",
                "paymentAttemptsDelay": "1",
                # [
                #         {
                #                 "name": "PLAN_VALUE",
                #                 "value": "20000",
                #                 "currency": "COP"
                #         },
                #         {
                #                 "name": "PLAN_TAX",
                #                 "value": "3193",
                #                 "currency": "COP"
                #         },
                #         {
                #                 "name": "PLAN_TAX_RETURN_BASE",
                #                 "value": "16806",
                #                 "currency": "COP"
                #         }
                # ]
                
        }

additionalValues = {}
additionalValues = [
                            {
                                    "name": "PLAN_VALUE",
                                    "value": "10000",
                                    "currency": "COP"
                            },
                            {
                                    "name": "PLAN_TAX",
                                    "value": "0",
                                    "currency": "COP"
                            },
                            {
                                    "name": "PLAN_TAX_RETURN_BASE",
                                    "value": "0",
                                    "currency": "COP"
                            }
                        ]

data['additionalValues']=additionalValues

# print(json.dumps(data, indent=4))
############################# BUILD POST HEADERS ############################


data= json.dumps(data)


################### ENVIO POST ######################
response = requests.post(URL_CREAR_PLAN, data= data, headers= HEADERS)
content=print(response.content)

########################## IMPRIMIR LO QUE ENVIO Y RECIBO###############
# res=dump.dump_all(response)
# print(res.decode('utf-8'))