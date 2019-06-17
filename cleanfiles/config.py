
import json, os
import pandas as pd


CONF = '\\conf\\glrutas.json'
cwd = os.path.dirname(os.path.realpath(__file__)) + CONF
with open(cwd, 'r') as file:
    RUTAS = json.load(file)


RUTA_LIQUIDA = RUTAS['LIQUIDA']
RUTA_AOBC =RUTAS['AOBC']
RUTA_RECAUDOS =RUTAS['RECAUDOS']
RUTA_RESUMEN =RUTAS['RESUMEN']

    
ESTRUCTURA_ARCHIVO= '\\conf\\glarchivo_estructura.json'
cwd2 = os.path.dirname(os.path.realpath(__file__)) + ESTRUCTURA_ARCHIVO
with open(cwd2, 'r') as file:
    ESTRUCTURA = json.load(file)



LIQUIDA = pd.read_csv(RUTA_LIQUIDA, names=['original'])



