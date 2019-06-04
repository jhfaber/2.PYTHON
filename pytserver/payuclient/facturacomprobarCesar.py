
""" comprueba si existe la suscripcion en payu y la actualiza  """


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

#time converter
import time

URL_API_PRODUCCION = settings.URL
HEADERS =settings.HEADER


def crearPeticion(id_suscripcion):
    params={
        "subscriptionId": id_suscripcion
    }
    return params


def enviarPeticion(URL, id_suscripcion):
    params= crearPeticion(id_suscripcion)
    response = requests.get(URL, headers= HEADERS, params=params)
    # print(response.content)
    response = json.loads(response.content)
    
    # settings.beauty_print(response)
    return response

def consultarFacturas(serial_pago_suscripcion):
    consulta_facturas = """
       
        SELECT serial_pago_factura,
        serial_pago_suscripcion,
        token,
        orderid as orderid2,
        state as state2 ,
        amount as amount2,
        currency as currency2,
        fecha_cargo
        FROM dba_pagos_facturas
        WHERE utilizada=0 and serial_pago_suscripcion = '{serial_pago_suscripcion}'
        """.format(serial_pago_suscripcion= serial_pago_suscripcion) 
    facturas=bl.conexion_base(consulta_facturas)
    # id_cliente =id_cliente[0]['serial_pago_cliente'].to_string(index=False)
    return facturas

def consultarTokenSuscripcion(token):
    consulta_token = """
       
        SELECT serial_pago_suscripcion,
        token
        FROM dba_pagos_suscripciones
        WHERE token = '{token}'
        """.format(token= token) 
    consulta_token=bl.conexion_base(consulta_token)
    # id_cliente =id_cliente[0]['serial_pago_cliente'].to_string(index=False)
    return consulta_token




#recibe token de suscripcion
def main(ID_SUSCRIPCION):
    pd.options.mode.chained_assignment = None # default='warn'    
    
    # print(ID_SUSCRIPCION)
    URL_CONSULTA ='rest/v4.9/recurringBill'
    URL = URL_API_PRODUCCION+URL_CONSULTA.format(ID_SUSCRIPCION)

    dfsus = consultarTokenSuscripcion(ID_SUSCRIPCION)
    serial_pago_suscripcion = int(dfsus[0].loc[0,"serial_pago_suscripcion"])
    #print(serial_pago_suscripcion)
    # print(serial_pago_suscripcion)
    response= enviarPeticion(URL, ID_SUSCRIPCION)
    
    # print(response)
    if("recurringBillList" in response):
        response= response["recurringBillList"]
        #dataframe payu
        facturas = pd.DataFrame.from_dict(response)
        facturas['fecha'] = facturas['dateCharge'].apply(lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(x/1000))))
        #dataframe bd
        fac_bd = consultarFacturas(serial_pago_suscripcion)
        if(len(fac_bd[0])>0):
            df = pd.merge(facturas, fac_bd[0],  how='inner', left_on=['id'], right_on = ['token'])
        else:
            df=facturas
            
        if(len(fac_bd[0])>0):
            df2 = pd.merge(facturas, fac_bd[0],  how='left', left_on=['id'], right_on = ['token'])
            df3=df2.loc[df2["token"].isnull(),:]
        else:
            df2=facturas
            df3=df2
        
        df3["serial_pago_suscripcion"]=serial_pago_suscripcion
        
        
        
        #print(fecha1)
        #print(df3.iloc[2,:])
        consulta="""DECLARE @json NVARCHAR(MAX)
        SET @json =  
            N'{cadena_json}' 

        update pf set pf.state=a.state,pf.fecha_cargo=a.fecha
        FROM 
            OPENJSON ( @json ) 
        WITH (  
                    token   varchar(200) '$.token' ,
                    serial_pago_factura   int '$.serial_pago_factura' ,
                    state varchar(200) '$.state',
                    fecha varchar(200) '$.fecha' 
            ) a
            inner join dba_pagos_facturas pf
            on a.serial_pago_factura= pf.serial_pago_factura
        
            SET @json =  
            N'{cadena_json2}' 

            insert into dba_pagos_facturas (serial_pago_suscripcion,
                            token,
                            orderid,
                            state,
                            amount,
                            currency,
                            utilizada,
                            fecha_cargo)

            
            select serial_pago_suscripcion,id,orderId,state,amount,currency,0,fecha FROM 
            OPENJSON ( @json ) 
        WITH (  
                    amount   varchar(200) '$.amount' ,
                    currency    varchar(200) '$.currency' ,
                    state varchar(200) '$.state',
                    id varchar(200) '$.id',
                    orderId  varchar(200) '$.orderId',
                    fecha varchar(200) '$.fecha',
                    serial_pago_suscripcion int '$.serial_pago_suscripcion' 
            ) a
            select 1 as salida



        """.format(cadena_json=df.to_json(orient='records'),cadena_json2=df3.to_json(orient='records'))
        #print(consulta)
        d1=bl3.conexion_base_sp(consulta)  #quitar comentario al acabar las pruebas
        # print(d1[0].loc[0,:])

        
        # print(consulta)

      

