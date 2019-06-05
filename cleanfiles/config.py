
import json, os


CONF = '\\glrutas.json'
cwd = os.path.dirname(os.path.realpath(__file__)) + CONF

with open(cwd, 'r') as file:
    rutas = json.load(file)

RUTA_ARCHIVO = rutas['RUTA']
print(rutas['RUTA'])
