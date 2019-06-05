#!/usr/bin/env python
# -*- coding: utf-8 -*-
print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n\n\n")
#print("Hola")

import os
import pandas as pd
import ast
from unidecode import unidecode
import sys
import unicodedata
import cgi, cgitb
import datetime
import json
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.preprocessing import StandardScaler
reload(sys)
sys.setdefaultencoding("utf-8")

glvalor_mayor=0
glcantidad_cluster_mayor=0
modelo_kmean={}



form = cgi.FieldStorage()
tipo2 = form.getvalue("tipo")
#tipo2="transacciones"
def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
    return s.decode()

def agrupa_describe(df,clave,arrcualitativas,arrcualitativas_nombre):

  
    #objparametricas={}
    #n=0
    #while n<len(arrcualitativas):
        #dftmp=df.loc[:,[arrcualitativas[n],arrcualitativas_nombre[n]]]
        #dftmp=dftmp.drop_duplicates()
        #dftmp=dftmp.set_index(arrcualitativas[n])
        #objparametricas[arrcualitativas[n]]=dftmp
        #n=n+1
    #print len(objparametricas['actividad'])
    #print objparametricas['actividad']
    #print df.groupby("actividad").count()
    arrcualcopia=arrcualitativas_nombre[:]
    arrcualcopia.insert(0,clave)
    df_cual=df[arrcualcopia]
    df_cual_g=df_cual.groupby(arrcualcopia).size()
    df_cual_g2=df_cual.groupby(clave).size()
    #df_dato_act = pd.concat([df_cual_g.reset_index('actividad'), df], axis=1, join='inner')
    #df_dato_act=pd.merge(df_cual_g.reset_index('actividad'),df, left_on="actividad", right_on="actividad")
    #print df_dato_act
    df_cual_g3=pd.merge(df_cual_g.to_frame(),df_cual_g2.to_frame(),left_index=True,right_index=True)
    df_cual_g3["frecuencia"]=100*df_cual_g3["0_x"]/df_cual_g3["0_y"]
    df_cual_g3=df_cual_g3.sort_values(by='frecuencia',ascending=False)
    #print df_cual_g3.reset_index()
    arrclaves=df[clave].value_counts().sort_index()
    
    arr_resumen=[]
    n=0
    while n<len(arrclaves):
        dftmp=df_cual_g3.loc[arrclaves.index[n],:].head()
        dftmp.drop(['0_x','0_y'], axis=1,inplace=True) 
        arr_resumen.append({clave:arrclaves.index[n],'resumen': dftmp.to_string()})
        n=n+1
    df_resumen=pd.DataFrame(arr_resumen)
    df_resumen=df_resumen.set_index(clave)
    #print df_resumen.iloc[0,:]
    
    df.drop(arrcualitativas, axis=1,inplace=True)
    df.drop(arrcualitativas_nombre, axis=1,inplace=True) 
    
    df2=pd.value_counts(df['cluster']).to_frame()
    df2["descripcion"]="cesar"
    df3=df.groupby(clave).max()
    lista_columnas_cuant=[str(i) for i in df3.columns]
    lista_max=["max_"+str(i) for i in df3.columns]
    df3.columns=lista_max
    df4=df.groupby(clave).min()
    lista_min=["min_"+str(i) for i in df4.columns]
    df4.columns=lista_min
    dt5=pd.merge(df3,df4,left_index=True,right_index=True)
    dt5=pd.merge(dt5,df_resumen,left_index=True,right_index=True)
    #df4=df4[lista_min]
    cadena='+'.join(["'"+str(i) + "'+ ' Entre '+dt5['min_"+str(i)+"']+ ' y ' +dt5['max_"+str(i)+"']+'\\n'"   for i in lista_columnas_cuant])
    #dt5['total']='cantidad_credito'+ 'Entre'+str(dt5['max_cantidad_credito'])
    #'cantidad_credito' 'Entre'+dt5['max_cantidad_credito']
    #print cadena
    for col in lista_max:
        dt5[col] = dt5[col].astype('str')
    for col in lista_min:
        dt5[col] = dt5[col].astype('str') 

    exec("dt5['total']="+cadena)
    dt5=dt5.reset_index()
    
    #dt5['resumen']=dt5['resumen'].astype('unicode')
    dt5['total']=dt5['total']+dt5['resumen']
    dt6=dt5[[clave,'total']]
    
    #print dt5.loc[0,['resumen']]
    #f = open ("C:\\archivos_salida\\test.txt",'w')
    #f.write(str(dt5.loc[0,['resumen']]))
    #f.close()
    return dt6
    #escribir_excel(dt6,"C:\\archivos_salida\\test.xlsx","xlsxwriter",[20,100])

def conexion_base(sql): 
    from os import getenv
    import pyodbc
    conn = pyodbc.connect(open("C:\\consofi\\bd.config").read())
    numero_tabla = 0
    consulta = """ set nocount on;   """+sql
    cursor = conn.cursor()
    cursor.execute(consulta)
    arrgen = []
    objgen = {}
    while True:
        arr1 = []
        for row in cursor.fetchall():
            n = 0
            obj1 = {}
            for column in cursor.description:
                obj1[column[0]] = row[n]
                n = n + 1
            arr1.append(obj1)

        dfarr1 = pd.DataFrame(arr1)

        # arrgen.append(dfarr1)
        objgen[numero_tabla] = dfarr1
        numero_tabla = numero_tabla + 1
        if cursor.nextset() == False:
            break

    conn.close()
    return objgen


def conexion_base_insert(sql): 
    from os import getenv
    import pyodbc
    conn = pyodbc.connect(open("C:\\consofi\\bd.config").read())
    numero_tabla = 0
    consulta = """ set nocount on;   """+sql
    cursor = conn.cursor()
    cursor.execute(consulta)
    conn.commit()
    conn.close()   



def escribir_excel(df,ubicacion,motor,arrancho_columnas):
   
    
    writer = pd.ExcelWriter(ubicacion, engine=motor)

    df.to_excel(writer, sheet_name='Hoja1',index=False)
    workbook = writer.book
    worksheet = writer.sheets['Hoja1']


    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#203764',
        'font_color': 'white',
        'border': 1})

    ncol=0
    while ncol<len(df.columns):
        worksheet.write(0, ncol, df.columns[ncol], header_format)
        worksheet.set_column(ncol, ncol, int(arrancho_columnas[ncol]))
        ncol=ncol+1
    writer.save()


    
    #print glgeneral_calidad


def guarda_clusterizacion(dts,entidad,nombre,clave):
    n=0
    arrcualitativas_nombre=['actividad_descripcion']
    while n<len(arrcualitativas_nombre):
        dts[0][arrcualitativas_nombre[n]]=dts[0][arrcualitativas_nombre[n]].apply(lambda x: elimina_tildes(x))
        n=n+1
    dsres=agrupa_describe(dts[0],clave,['actividad'],arrcualitativas_nombre)
    #dsres['total'].apply(lambda x: elimina_tildes(x))
    caden=dsres.to_json(orient='records')
    caden=caden.replace("'","''")
    
    cadena_act=""" DECLARE @json NVARCHAR(MAX) SET @json = N'{caden}'
    delete from VA_CLUSTER where CLUS_Entidad={entidad}
    insert into VA_CLUSTER (CLUS_Entidad,CLUS_Fecha_Segmentacion,cluster,CLUS_Descripcion,CLUS_Nombre)
    SELECT {entidad},dateadd(HH,-5,getutcdate()),{clave},total,'{nombre}' FROM 
     OPENJSON (@json) 
    WITH (  
                    {clave}   varchar(200) '$.{clave}' , 
                    total varchar(max) '$.total'
     
         ) 
    """.format(caden=caden,entidad=entidad,nombre=nombre,clave=clave)
    #print cadena_act
    conexion_base_insert(cadena_act)
     


consulta="""select vc.cluster, vc.CLIEN_idInterno as id_cliente,
    vc.CLIEN_ActividadEconomicacliente as actividad,
	ac.ACECO_Descripcion as actividad_descripcion,
    ISNULL(vc.CLIEN_MontoIngresoMensual,0) +ISNULL(vc.CLIEN_MontoOtrosIngresosMensual,0) as monto_ingreso,
    ISNULL(vc.CLIEN_MontoEgresoMensual,0) as monto_egreso,
    ISNULL(vc.CLIEN_TotalPatrimonio,0) as total_patrimonio,
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad=13 and 
 cp2.CLXPR_Cliente=vc.CLIEN_idInterno and tr.TRANS_TipoTransaccion=2 
 and tr.TRANS_FechaRealizada>'2017-02-01 00:00:00'
 and tr.TRANS_FechaRealizada<'2019-03-01 00:00:00'

  ) as total_debito,
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad=13 and 
 cp2.CLXPR_Cliente=vc.CLIEN_idInterno and tr.TRANS_TipoTransaccion=1 
 and tr.TRANS_FechaRealizada>'2017-02-01 00:00:00'
 and tr.TRANS_FechaRealizada<'2019-03-01 00:00:00'

  ) as total_credito,
  (select ISNULL(count(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad=13 and 
 cp2.CLXPR_Cliente=vc.CLIEN_idInterno and tr.TRANS_TipoTransaccion=2 
 and tr.TRANS_FechaRealizada>'2017-02-01 00:00:00'
 and tr.TRANS_FechaRealizada<'2019-03-01 00:00:00'

  ) as cantidad_debito,
    (select ISNULL(count(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad=13 and 
 cp2.CLXPR_Cliente=vc.CLIEN_idInterno and tr.TRANS_TipoTransaccion=1
 and tr.TRANS_FechaRealizada>'2017-02-01 00:00:00'
 and tr.TRANS_FechaRealizada<'2019-03-01 00:00:00'

  ) as cantidad_credito

     from VA_CLIENTE vc 
	 inner join KG_ACTIVIDADECONOMICA ac
	 on vc.CLIEN_ActividadEconomicacliente=ac.ACECO_IdInterno
    where vc.CLIEN_Entidad=13
"""
dts=conexion_base(consulta)
guarda_clusterizacion(dts,13,'cliente','cluster')

