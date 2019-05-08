

#conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=test;DATABASE=test;UID=user;PWD=password')

import pyodbc
import pandas
from querys import sql
import sys

# CONNECT TO SQLSERVER DATABASE

server = 'consofi.database.windows.net'
database = 'DB_SARLAFT'
username = 'consofi'
password = 'azuconsof2018i*-'
cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


##########################  CONFIGURATION  ###################################


entidad = '22'


##########################     CODE           ##################################
canal = sql.canales(entidad)
transacciones = sql.transacciones(entidad)
asociado = sql.asociados(entidad)

#EXCEL FORMAT NO FUNCIONA EL FORMATO
"""
cell_format = workbook.add_format()
cell_format.set_bold()
cell_format.set_font_color('white')
cell_format.sert_font_name('Times New Roman')
"""


#LAS CREACIONES DE LOS ARCHIVOS OTROS ESTAN PARADAS, DESCOMENTAR SI SE NECESITAN.

#CREATE ASOCIADOS
data = pandas.read_sql(asociado,cnxn)
writer = pandas.ExcelWriter('ASOCIADOS.xls', engine='xlsxwriter')
data.to_excel(writer, sheet_name='ASOCIADOS')
writer.save()

#CREATE CANALES
data = pandas.read_sql(canal,cnxn)
writer = pandas.ExcelWriter('CANALES.xls', engine='xlsxwriter')
data.to_excel(writer, sheet_name='CANALES')
writer.save()

#CREATE TRANSACCIONES
data = pandas.read_sql(transacciones,cnxn)
writer = pandas.ExcelWriter('TRANSACCIONES.xls', engine='xlsxwriter')
data.to_excel(writer, sheet_name='CANALES')
writer.save()







#EXAMPLE OF QUERY
"""
sqlcanal = "SELECT * FROM KP_CANAL;"
data = pandas.read_sql(sql.asociadossql,cnxn)
writer = pandas.ExcelWriter('CANALES.xls', engine='xlsxwriter')
data.to_excel(writer, sheet_name='CANALES')
writer.save()
"""



#print(sql.asociadossql)
