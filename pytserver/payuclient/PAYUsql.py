
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
import time

#devuelve el token de la suscripcion
def consultarTokenSuscripcionPorID(serial_pago_suscripcion):
    consulta_token = """
       
        SELECT token
        FROM dba_pagos_suscripciones
        WHERE serial_pago_suscripcion = '{serial_pago_suscripcion}'
        """.format(serial_pago_suscripcion= serial_pago_suscripcion) 
    dict_token=bl.conexion_base(consulta_token)
    token = (dict_token[0].loc[0,"token"])    
    return token #string

def consultarSerialSuscripcionPortoken(token):
    consulta_token = """
       
        SELECT serial_pago_suscripcion,
        token
        FROM dba_pagos_suscripciones
        WHERE token = '{token}'
        """.format(token= token) 
    dict_serial_pago_suscripcion=bl.conexion_base(consulta_token)
    serial_pago_suscripcion =(dict_serial_pago_suscripcion[0].loc[0,"serial_pago_suscripcion"])
    return serial_pago_suscripcion


# def consultarFacturas(serial_pago_suscripcion):
#     consulta_facturas = """
       
#         SELECT serial_pago_factura,
#         serial_pago_suscripcion,
#         token,
#         orderid as orderid2,
#         state as state2 ,
#         amount as amount2,
#         currency as currency2,
#         fecha_cargo,
#         fecha_creacion
#         FROM dba_pagos_facturas
#         WHERE utilizada=0 and serial_pago_suscripcion = '{serial_pago_suscripcion}'
#         """.format(serial_pago_suscripcion= serial_pago_suscripcion) 
#     facturas=bl.conexion_base(consulta_facturas)
#     facturas = facturas[0]
#     return facturas

def consultarFacturas(serial_pago_suscripcion):
    consulta_facturas = """
       
        SELECT pf.serial_pago_factura,
        pf.serial_pago_suscripcion,
        pf.token,
        pf.orderid as orderid2,
        pf.state as state2 ,
        pf.amount as amount2,
        pf.currency as currency2,
        pf.fecha_cargo,
        ps.fecha_creacion
        FROM dba_pagos_facturas pf
		inner join dba_pagos_suscripciones ps on ps.serial_pago_suscripcion=pf.serial_pago_suscripcion
        WHERE pf.utilizada=0 and ps.serial_pago_suscripcion = '{serial_pago_suscripcion}'
        """.format(serial_pago_suscripcion= serial_pago_suscripcion) 
    facturas=bl.conexion_base(consulta_facturas)
    facturas = facturas[0]
    return facturas



def consultarSuscripcionesActivas():
    consulta_suscripcion = """        

        SELECT ps.serial_pago_suscripcion, ps.token, pf.state
        FROM dba_pagos_suscripciones ps
        inner join dba_pagos_facturas pf on ps.serial_pago_suscripcion = pf.serial_pago_suscripcion
        WHERE ps.activo = 1"""
    
    df_suscripciones=bl.conexion_base(consulta_suscripcion)
    df_suscripciones =df_suscripciones[0]    
    return df_suscripciones




# BORRAR LUEGO
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

