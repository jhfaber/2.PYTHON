print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")



import requests
import json, settings
import pandas as pd
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
import time

#
import facturacomprobar

URL_API_PRODUCCION = settings.URL
HEADERS =settings.HEADER

def consultarFacturas(token_suscripcion):
    consulta_facturas = """    
    select ps.token,ps.fecha_creacion,pf.state,pf.fecha_cargo from dba_pagos_suscripciones ps
    inner join  dba_pagos_tarjetas pt on ps.serial_pago_tarjeta=pt.serial_pago_tarjeta
    left join dba_pagos_facturas pf on ps.serial_pago_suscripcion=pf.serial_pago_suscripcion
    where serial_pago_cliente= {serial_pago_suscripcion}
    """.format(serial_pago_suscripcion= token_suscripcion) 
    facturas=bl.conexion_base(consulta_facturas) 
    # print(consulta_facturas)   
    return facturas

def consultarCliente(token):
    consulta_cliente = """
        declare @serial int;
        SELECT serial_pago_cliente FROM dba_pagos_clientes 
        WHERE token = '{token}'
        set @serial=scope_identity()""".format(token= token) 
    id_cliente=bl.conexion_base(consulta_cliente)
    id_cliente =id_cliente[0]['serial_pago_cliente'].to_string(index=False)
    # print(consulta_cliente)
    return id_cliente
    


def main():
    form = cgi.FieldStorage()
    dataPost= form.getvalue('texto')
    dataPost=json.loads(dataPost)
    
    
    ID_SUSCRIPCION=consultarCliente(dataPost['serial_pago_cliente']) 
    
    facturas = consultarFacturas(ID_SUSCRIPCION) 
    
    # print(facturas)
    facturas = pd.DataFrame.from_dict(facturas[0])

    if(not facturas.empty):

        token_suscripcion= facturas['token'].tolist()
        
        for factura in token_suscripcion :
            facturacomprobar.main(factura)
            
        del facturas['token']  
        
        facturasPost = facturas.to_json(orient="records")
        print(facturasPost)
    else:
        #no hay facturas
        data = { 
            "error": "1",
            "type": "NOT-FACTURES"
        }
        print(json.dumps(data))
    

main()

