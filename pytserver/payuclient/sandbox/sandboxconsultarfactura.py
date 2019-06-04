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


# TOKEN = '09ab5af6-00f7-47c1-bdad-c6d124862e49'
# T_NUMERO='4323592726185547'
# PLAN_CODE = "1"
serial_pago_suscripcion= 'cd508mgib217'
serial_pago_cliente = '92abaol8td8a'

URL_CONSULTA ='rest/v4.9/recurringBill'
URL = URL_API_PRODUCCION+URL_CONSULTA

""" 
    subscriptionId = subscriptionId
 """
# /rest/v4.9/recurringBill?subscriptionId={subscriptionId}
############################# BUILD POST HEADERS ############################
params ={
    "subscriptionId" : serial_pago_suscripcion
}

# params ={
#     "customerId" : serial_pago_cliente
# }


################### ENVIO POST ######################

def main():
    response = requests.get(URL, headers= HEADERS, params= params)
    settings.beauty_print(response)
    # content=print(response.content)


main()





