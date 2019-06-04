""" Consulta las facturas en la base de datos """

print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")


import requests
import json, settings
import cgi, cgitb
#
import cgi, cgitb
import PAYUsql as PAYU
import facturacomprobar








    
def main():
    #dataPost
    form = cgi.FieldStorage()
    dataPost= form.getvalue('texto')
    dataPost=json.loads(dataPost)
    
    token_suscripcion = PAYU.consultarTokenSuscripcionPorID(dataPost['serial_pago_suscripcion']) 
    #comprobar
    facturacomprobar.main(token_suscripcion)
    #consultar
    df_facturas = PAYU.consultarFacturas(dataPost['serial_pago_suscripcion'])    
    json_facturas = df_facturas.to_json(orient="records")
    print(json_facturas)
   
    
main()