
import requests
import json, settings
import cgi, cgitb
import pandas as pd

URL_API_PRODUCCION = settings.URL
HEADERS =settings.HEADER
ACCOUNDTID =settings.ACCOUNDTID

URL_FACTURA = 'rest/v4.9/recurringBill'
URL_CLIENTE = URL_CONSULTA= 'rest/v4.9/customers/{}'
URL_SUSCRIPCION = 'rest/v4.9/subscriptions/{}'
URL_PLAN = 'rest/v4.9/plans/{}'

def FacturaConsultarPorSuscripcion(token):
    #URL_CONSULTA ='rest/v4.9/recurringBill'
    URL = URL_API_PRODUCCION+URL_FACTURA
    params= params={
                "subscriptionId": token
            }
    response = requests.get(URL, headers= HEADERS, params=params)
    response = json.loads(response.content)
    if "recurringBillList" in response:
        response = response['recurringBillList']        
    else:
        response['error'] ='1'
    
    return response

def FacturaConsultarPorCliente(token):
    #URL_CONSULTA ='rest/v4.9/recurringBill'
    URL = URL_API_PRODUCCION+URL_FACTURA
    params= params={
                "customerId": token
            }
    response = requests.get(URL, headers= HEADERS, params=params)
    response = json.loads(response.content)
    if "recurringBillList" in response:
        response = response['recurringBillList']        
    else:
        response['error'] ='1'
    
    return response



def ClienteActualizarPorID(dataPost):
    #URL_CONSULTA= 'rest/v4.9/customers/{}'
    URL = URL_API_PRODUCCION+(URL_CLIENTE.format(dataPost['customerId']))
    data = {
        "email": dataPost['email']
    }
    response = requests.put(URL, data=json.dumps(data), headers= HEADERS)
    response = json.loads(response.content)
    return response

def ClienteConsultarPorID(dataPost):
    #URL_CONSULTA= 'rest/v4.9/customers/{}' 
    URL = URL_API_PRODUCCION+(URL_CLIENTE.format(dataPost['customerId']))
    response = requests.get(URL, headers= HEADERS)
    response = json.loads(response.content)
    return response

def ClienteCrear(dataPost):
    #URL_CONSULTA= 'rest/v4.9/customers/'
    URL = URL_API_PRODUCCION+URL_CLIENTE 
    data= {
        "fullName": dataPost['fullName'],
        "email": dataPost['email']
    } 
    response = requests.post(URL, data= json.dumps(data), headers= HEADERS)    
    response =json.loads(response.content)
    return response

def ClienteEliminarPorID(dataPost):
    #URL_CONSULTA= 'rest/v4.9/customers/{}'
    URL = URL_API_PRODUCCION+(URL_CLIENTE.format(dataPost['customerId']))
    response = requests.delete(URL, headers= HEADERS)
    response =json.loads(response.content)
    return response

def SuscripcionActualizarPorID(dataPost):
    #URL_CONSULTA= 'rest/v4.9/subscriptions/{}'
    URL = URL_API_PRODUCCION+(URL_SUSCRIPCION.format(dataPost['subscriptionId']))
    data = {
        "description": dataPost['description']
    }
    response = requests.put(URL, data=json.dumps(data), headers= HEADERS)
    response =json.loads(response.content)
    return response

def SuscripcionConsultarPorID(dataPost):
    #URL_CONSULTA= 'rest/v4.9/subscriptions/{}'
    URL = URL_API_PRODUCCION+(URL_SUSCRIPCION.format(dataPost['subscriptionId']))
    response = requests.get(URL, headers= HEADERS)
    response =json.loads(response.content)
    return response


# CLIENTE Y TARJETA YA DEBEN ESTAR CREADOS
def SuscripcionCrear(dataPost):
    #URL_CONSULTA= 'rest/v4.9/subscriptions/'
    URL = URL_API_PRODUCCION+URL_SUSCRIPCION
    data = {
            "quantity": dataPost['quantity'],
            "installments": dataPost['installments'],
            "trialDays": dataPost['trialDays'],   
            'immediatePayment': dataPost['immediatePayment']                              
                
        }
    customer = {
        "id": dataPost['id'],
    }
    creditCards = [{
        "token": dataPost['token'],
    }]
    customer['creditCards'] = creditCards
    plan= {
        "planCode": dataPost['token']
    }
    data['customer'] =customer
    data['plan']= plan
    response = requests.post(URL, data= data, headers= HEADERS)
    response =json.loads(response.content)
    return response

def SuscripcionEliminarPorID(dataPost):
    #URL_CONSULTA= 'rest/v4.9/subscriptions/{}'
    URL = URL_API_PRODUCCION+(URL_SUSCRIPCION.format(dataPost['subscriptionId']))
    response = requests.delete(URL, headers= HEADERS)
    response =json.loads(response.content)
    return response

def PlanActualizarPorID(dataPost):
    #URL_CONSULTA= 'rest/v4.9/plans/{}'
    URL = URL_API_PRODUCCION+(URL_PLAN.format(dataPost['planCode']))
    data = {
        "description": "Cambio de descripcion"
    }
    response = requests.put(URL, data=json.dumps(data), headers= HEADERS)
    response = json.loads(response.content)
    return response

def PlanConsultarPorID(dataPost):
    #URL_CONSULTA= '/rest/v4.9/plans/{}' #{clienteID}
    URL = URL_API_PRODUCCION+(URL_PLAN.format(dataPost['planCode']))
    response = requests.get(URL,headers=HEADERS)
    response = json.loads(response.content)

def PlanCrear(dataPost):
    #URL_CONSULTA = '/rest/v4.9/plans/'
    URL = URL_API_PRODUCCION+URL_PLAN
    data = {
                "accountId": ACCOUNDTID,
                "planCode": dataPost['planCode'],
                "description": dataPost['description'],
                "interval": dataPost['interval'],
                "intervalCount": dataPost['intervalCount'],
                "maxPaymentsAllowed": dataPost['maxPaymentsAllowed'],
                "paymentAttemptsDelay": dataPost['paymentAttemptsDelay'],
                "trialDays" : dataPost['trialDays']
                
        }
    additionalValues = {}
    additionalValues = [
                                {
                                        "name": "PLAN_VALUE",
                                        "value": dataPost['additionalValues']['value'],
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
    response = requests.post(URL, data= json.dumps(data), headers= HEADERS)
    response = json.loads(response.content)
    return response

def PlanEliminar(dataPost):
    #URL_CONSULTA= 'rest/v4.9/plans/{}'
    URL = URL_API_PRODUCCION+(URL_PLAN.format(dataPost['planCode']))
    response = requests.delete(URL, headers= HEADERS)
    response = json.loads(response.content)
    return response
