print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")


import requests
import json, settings
import cgi, cgitb
import pandas as pd
import time
#

import PAYUsql as ps
import PAYUpeticiones as pp
#
import base_leer3 as bl3



URL_API_PRODUCCION = settings.URL
HEADERS =settings.HEADER

facturasInsertar =""
facturasActualizar =""
facturasAuxiliar =""

def compararFacturas(facturas, facturas_db, serial_pago_suscripcion):
    global facturasInsertar
    global facturasActualizar
    global facturasAuxiliar
    
    
    #
    if(len(facturas_db)>0):
        facturasActualizar = pd.merge(facturas, facturas_db,how='inner', left_on=['id'], right_on=['token'])  
        facturasAuxiliar = pd.merge(facturas, facturas_db,  how='left', left_on=['id'], right_on = ['token'])
        facturasInsertar=facturasAuxiliar.loc[facturasAuxiliar["token"].isnull(),:]
    else:        
        facturasActualizar=facturas
        facturasAuxiliar = facturas
        facturasInsertar = facturasAuxiliar
    
    facturasInsertar["serial_pago_suscripcion"]=serial_pago_suscripcion   
        
    


def actualizaInserta():
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



        """.format(cadena_json=facturasActualizar.to_json(orient='records'),cadena_json2=facturasInsertar.to_json(orient='records'))
    
    d1=bl3.conexion_base_sp(consulta)
    


# recibe token suscripcion
def main(token_suscripcion):
    
    

    response = pp.FacturaConsultarPorSuscripcion(token_suscripcion)
    if(not "error" in response):
        serial_pago_suscripcion = ps.consultarSerialSuscripcionPortoken(token_suscripcion)     
        facturas_db=ps.consultarFacturas(serial_pago_suscripcion)
        
        
        facturas = pd.DataFrame.from_dict(response)
        facturas['fecha'] = facturas['dateCharge'].apply(lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(x/1000))))
        
        compararFacturas(facturas, facturas_db, serial_pago_suscripcion)
        actualizaInserta()
        data = {
            'error' : '0'
        }
        print(data)  
    else:
        print(response)


# main('cb8bdyy4nbj9')