# crea suscripcion y tarjeta

print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")

import requests
import json, settings
import cgi, cgitb
#
import os, sys
import os
import pandas as pd
import cgi, cgitb
import numpy as np
from os import getenv
import pyodbc
import os.path
import base_leer as bl
import base_leer3 as bl3
import base_escribir as be
import sys
import json
import requests

URL_API_PRODUCCION = settings.URL
HEADERS =settings.HEADER




def crearPeticion(dataPost):
    data = {
    "quantity": "1",
    "installments": "1",
    "trialDays":"0",
    "immediatePayment" : "true"
    
    
    
    ""
    }

    customer = {
        "id": dataPost['id'],
        "creditCards": [
            {
                "name": dataPost['name'],
                "number": dataPost['number'],
                "expMonth": dataPost['expMonth'],
                "expYear": dataPost['expYear'],
                "type": dataPost['type'],
                
            }
        ]
    }

    plan= {
        "planCode": dataPost['planCode']
    }
    data['customer'] = customer
    data['plan']= plan
    
    return data

def enviarPeticion(dataPost, URL):
    data = crearPeticion(dataPost)
    response = requests.post(URL, data= json.dumps(data), headers= HEADERS)
    # settings.beauty_print(response)
    response = json.loads(response.content)
    
    response["trialDays"] = data["trialDays"] if "trialDays" in data else "0"
    if("immediatePayment" in data):
        response["immediatePayment"] = "1" if data["immediatePayment"]=="true" else "0"
    else:
        response["immediatePayment"] = "0" 
     
    response["notifyUrl"] =  data["notifyUrl"] if "notifyUrl"  in data else "NOT URL"
    return response


def consultarCliente(dataPost):
    consulta_cliente = """
        declare @serial int;
        SELECT serial_pago_cliente FROM dba_pagos_clientes 
        WHERE token = '{token}'
        set @serial=scope_identity()""".format(token= dataPost['id']) 
    id_cliente=bl.conexion_base(consulta_cliente)
    id_cliente =id_cliente[0]['serial_pago_cliente'].to_string(index=False)
    return id_cliente

def crearTarjeta(id_cliente, response):    
    id_tarjeta=bl3.conexion_base_sp(""" 
   
        INSERT INTO dba_pagos_tarjetas 
        VALUES (
        '{serial_pago_cliente}',
        '{token}', 
        '{activo}'
        

        );  
         select scope_identity() as serial""".format(
            serial_pago_cliente=id_cliente,
            token = response['id'],
            activo= 1)
        )
    id_tarjeta =id_tarjeta[0]['serial'].to_string(index=False)    
    return id_tarjeta

    

def crearSuscripcion(response,dataPost, id_tarjeta):   
    

    suscripcion="""declare @serial int;
    INSERT INTO dba_pagos_suscripciones (
        serial_pago_plan,
        token,
        trialDays,
        inmediatepayment,
        notifyUrl,
        activo,
        serial_pago_tarjeta,
        fecha_creacion 
    )
    VALUES (
    {serial_pago_plan},
    '{token}', 
    {trialDays}, 
    {inmediatepayment},
    '{notifyUrl}',
    {activo},
    {serial_pago_tarjeta},
    {fecha_creacion}

    );  
    set @serial=scope_identity()""" .format(
        serial_pago_plan=response['plan']['planCode'],
        token = response['id'],
        trialDays= response['trialDays'],
        inmediatepayment = response['immediatePayment'],
        notifyUrl = response["notifyUrl"] ,
        activo = 1,
        serial_pago_tarjeta = id_tarjeta,
        fecha_creacion = 'dateadd(HH,-5,GETUTCDATE())'
        )
    be.conexion_base_insert(suscripcion)
    # print(suscripcion)
    
    
def validarPlan(token):
    consulta_plan = """
    declare @serial int;
    SELECT serial_pago_plan FROM dba_pagos_planes
    WHERE token = '{token}'
    set @serial=scope_identity()""".format(token= token) 
    id_plan=bl.conexion_base(consulta_plan)

    if(id_plan[0].empty):
        id_plan= 0
    else:        
        id_plan =id_plan[0]['serial_pago_plan'].to_string(index=False)
    
    return int(id_plan)


def main():
    URL_CREACION= 'rest/v4.9/subscriptions/'     
    URL = URL_API_PRODUCCION+URL_CREACION
    #POST DATA
    form = cgi.FieldStorage()
    dataPost= form.getvalue('texto')
    dataPost=json.loads(dataPost)
    
    dataPost['planCode']=validarPlan(dataPost['planCode'])
    # print(dataPost['planCode'])
    
    
    
    # error 1 hubo error, error 0 no hubo error
    if(dataPost['planCode'] ==0):
        response = {'error': '1'}
        print(json.dumps(response))        
    else:        
        #SEND TO PAYU        
        response =enviarPeticion(dataPost, URL)
        if('type' in response):
            response['error'] = '1'
            print(json.dumps(response))
        else:
            #DB
            id_cliente = consultarCliente(dataPost)    
            id_tarjeta=crearTarjeta(id_cliente, response)
            crearSuscripcion(response,dataPost, id_tarjeta)    
                
            #return ok
            response['error'] = '0'
            print(json.dumps(response))  
    

main()


    
