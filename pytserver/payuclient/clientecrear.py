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


import cgi, cgitb
import requests
import json, settings
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


##############BUILD POST BODY#################
# data = {
            
#             "fullName": "Cesar",
#             "email": "jmarin@e-dentalsys.com"                             
                
#         }
################### ENVIO POST ######################

def crearPeticion(dataPost):
    data= {
        "fullName": dataPost['fullName'],
        "email": dataPost['email']
    }    
    # print(data)
    return data

def enviarPeticion(URL, dataPost):
    data = crearPeticion(dataPost)    
    response = requests.post(URL, data= json.dumps(data), headers= HEADERS)    
    response =json.loads(response.content)
    # print(response)
    return response
    
def crearCliente(response):
    id_cliente=bl3.conexion_base_sp("""    
    INSERT INTO dba_pagos_clientes 
    VALUES ('{token}',
    '{fullName}',
    '{email}', 
    '{activo}'
    );     
     
    select scope_identity() as serial
    
    """.format(
        token=response['id'],
        fullName = response['fullName'],
        email= response['email'],
        activo = 1 )
    )
    
    id_cliente =id_cliente[0]['serial'].to_string(index=False)
    return id_cliente

def tokenPlan(id_plan):
    token_plan = """
        
        SELECT token FROM dba_pagos_planes
        WHERE serial_pago_plan = {serial_pago_plan}
        """.format(serial_pago_plan= id_plan) 
    token=bl.conexion_base(token_plan)
    token =token[0]['token'].to_string(index=False)
    token = token[1:]
    return token


def main():    
    URL_CREACION= 'rest/v4.9/customers/'    
    URL = URL_API_PRODUCCION+URL_CREACION
    #POST DATA
    form = cgi.FieldStorage()
    dataPost= form.getvalue('texto')
    dataPost=json.loads(dataPost)

    #SEND PAYU
    response = enviarPeticion(URL, dataPost)

    #data storage
    serial_pago_cliente= crearCliente(response)
    
    #token= tokenPlan(dataPost['planCode'])
    # token= tokenPlan(26)
    # print(token)
    returnData = {
        'id': response['id'],
        'serial_pago_cliente': serial_pago_cliente
    } 
    
    print(json.dumps(returnData))

main()

