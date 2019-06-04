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

import PAYUsql as PAYU
URL_API_PRODUCCION = settings.URL
HEADERS =settings.HEADER


#SELECT 1 para que devuelva la transaccion
def eliminarSuscripcion(serial_pago_suscripcion):
    eliminar_suscripcion = """       
        UPDATE dba_pagos_suscripciones
        SET activo = 0
        WHERE serial_pago_suscripcion = {serial_pago_suscripcion}
        SELECT 1
        """.format(serial_pago_suscripcion= serial_pago_suscripcion) 
    bl3.conexion_base_sp(eliminar_suscripcion)

# serial_pago_suscripcion
def main():

    #
    form = cgi.FieldStorage()
    dataPost= form.getvalue('texto')
    dataPost=json.loads(dataPost)

    #delete
    URL_ELIMINAR= 'rest/v4.9/subscriptions/{}'
    token_suscripcion = PAYU.consultarTokenSuscripcionPorID(dataPost['serial_pago_suscripcion'])
    URL = URL_API_PRODUCCION+(URL_ELIMINAR.format(token_suscripcion))
       
    
    
    response = requests.delete(URL, headers= HEADERS)    
    response = json.loads(response.content)
    
    
    if('type' in response):
        response['error'] = '1'        
        eliminarSuscripcion(dataPost['serial_pago_suscripcion'])
        

    else:
        response['error'] = '0'
        response['description'] = 'La suscripción fue eliminada con éxito'
        eliminarSuscripcion(dataPost['serial_pago_suscripcion'])
    print(json.dumps(response))

    

main()

