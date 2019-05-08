

#conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=test;DATABASE=test;UID=user;PWD=password')

import pyodbc
import pandas
from querys import sql
import os


# CONNECT TO SQLSERVER DATABASE

server = 'consofi.database.windows.net'
database = 'DB_SARLAFT'
username = 'consofi'
password = 'azuconsof2018i*-'
cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


meses = ['ENERO','FEBRERO','MARZO','ABRIL', 'MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE']
mes = 1

########################      CONFIGURACION           ######################################
#seleccionar entidad SOLO FUNCIONA PARA MESES (MES TRAS MES) EL AGREGADO NO TIENE PROBLEMAS.
entidad = '23'
#Configurar un mes
fecha_ini_reporte = '2018-1-1'
#Fecha menor a:
fecha_fin_reporte= '2019-1-1'


#PATH
cwd = os.getcwd() + '\\informes_agregados'


##############################           CODIGO            ####################################

fecha_ini =fecha_ini_reporte.split("-")
fecha_fin =fecha_fin_reporte.split("-")
mes_inicio = int(fecha_ini[1])
mes_final = int(fecha_fin[1])


#SOLO UN MES

#VARIABLES

#CONSTRUCCION DEL QUERY

agregado_mes_asociado= sql.asociados_agregado(entidad,fecha_ini_reporte,fecha_fin_reporte)

#CONTRUIR EXCEL Y CONSULTA A LA BASE DE DATOS
data = pandas.read_sql(agregado_mes_asociado,cnxn)

writer = pandas.ExcelWriter(os.path.join(cwd,'0_TOTAL_AGREGADO_ID_'+entidad+'.xlsx'), engine='xlsxwriter')
data.to_excel(writer, sheet_name='ASOCIADOS')
writer.save()



#VARIOS MESES
"""
while(mes_inicio < mes_final):
    #ITERACION DE MESES

    inicio = str(mes_inicio)
    fin = str(mes_inicio+1)
    #CONTRUCCION FECHAS
    fecha_ini_0 = fecha_ini[0]+'-'+inicio+'-'+fecha_ini[2]
    fecha_fin_0 = fecha_ini[0]+'-'+fin+'-'+fecha_ini[2]


    print(meses[mes_inicio-1])
    print(fecha_ini_0)
    print(fecha_fin_0)




    #CONSTRUCCION DEL QUERY
    agregado_mes_asociado= sql.asociados_agregado(entidad,fecha_ini_0,fecha_fin_0)


    #CONTRUIR EXCEL Y CONSULTA A LA BASE DE DATOS

    data = pandas.read_sql(agregado_mes_asociado,cnxn)

    #WRITER CON PAHT DINAMICO, SI NO FUNCIONA SE DEBE CREAR LA CARPETA
    writer = pandas.ExcelWriter(os.path.join(cwd,str(mes_inicio)+'_ID_'+entidad+'_ASOCIADOS_AGREGADO_'+meses[mes_inicio-1]+ '.xls'), engine='xlsxwriter')
    data.to_excel(writer, sheet_name='ASOCIADOS')
    writer.save()
    mes_inicio = mes_inicio+1   


"""
