""" actualiza los estados suscripciones activas de PAYU """


print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")


import requests
import json, settings
import cgi, cgitb
import pandas as pd
#

import sqlPAYU as PAYU
import facturacomprobar



def main():
    df_suscripciones = PAYU.consultarSuscripcionesActivas()
    
    df_token = list(df_suscripciones['token'])   
    # for token_suscripcion in df_token:
    #     facturacomprobar.main(token_suscripcion)
    df_state =list(df_suscripciones['state'])
    ls_serial_pago_suscripcion =list(df_suscripciones['serial_pago_suscripcion'])
    for (i, item) in enumerate(df_state):

        if(item == "CANCELLED"):
            print(str(ls_serial_pago_suscripcion[i]) + "pasar a inactivo")



main()
