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
import numpy as np  
reload(sys)
sys.setdefaultencoding("utf-8")

form = cgi.FieldStorage()
glentidad_id=form.getvalue("entidad")
glfecha_ini=form.getvalue("fecha_ini")
glfecha_fin=form.getvalue("fecha_fin")

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
            #print obj1
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

def reporte_perfilamiento(fecha_ini,fecha_fin,entidad):
    #print fecha_ini
    #print fecha_fin
    consulta="""select CLIEN_NumeroIdentificacion as [Numero de Identificacion],ISNULL(CLIEN_Nombre1,'') + ' '+ISNULL(CLIEN_Nombre2,'')+' '+
ISNULL(CLIEN_Apellido1,'')+ ' '+ISNULL(CLIEN_Apellido2,'') as Nombre,
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Cliente=ci.CLIEN_idInterno and tr.TRANS_TipoTransaccion=2 
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'
  ) as [Monto Transacciones Debito],
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Cliente=ci.CLIEN_idInterno and tr.TRANS_TipoTransaccion=1 
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'
  )  as [Monto Transacciones Credito],
  (select ISNULL(count(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Cliente=ci.CLIEN_idInterno and tr.TRANS_TipoTransaccion=2 
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'
  ) as [Cantidad Transacciones Debito],
    (select ISNULL(count(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Cliente=ci.CLIEN_idInterno and tr.TRANS_TipoTransaccion=1
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'
  ) as [Cantidad Transacciones Credito],
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Cliente=ci.CLIEN_idInterno and tr.TRANS_TipoTransaccion=2 
 and tr.TRANS_FechaRealizada>dateadd(MM,-1,'{fecha_ini} 00:00:00')
 and tr.TRANS_FechaRealizada<dateadd(MM,-1,'{fecha_fin} 00:00:00')
  ) as [Monto Transacciones Debito_ant],
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Cliente=ci.CLIEN_idInterno and tr.TRANS_TipoTransaccion=1 
 and tr.TRANS_FechaRealizada>dateadd(MM,-1,'{fecha_ini} 00:00:00')
 and tr.TRANS_FechaRealizada<dateadd(MM,-1,'{fecha_fin} 00:00:00')
  )  as [Monto Transacciones Credito_ant],
  (select ISNULL(count(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Cliente=ci.CLIEN_idInterno and tr.TRANS_TipoTransaccion=2 
 and tr.TRANS_FechaRealizada>dateadd(MM,-1,'{fecha_ini} 00:00:00')
 and tr.TRANS_FechaRealizada<dateadd(MM,-1,'{fecha_fin} 00:00:00')
  ) as [Cantidad Transacciones Debito_ant],
    (select ISNULL(count(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Cliente=ci.CLIEN_idInterno and tr.TRANS_TipoTransaccion=1
 and tr.TRANS_FechaRealizada>dateadd(MM,-1,'{fecha_ini} 00:00:00')
 and tr.TRANS_FechaRealizada<dateadd(MM,-1,'{fecha_fin} 00:00:00')
  ) as [Cantidad Transacciones Credito_ant]



 from VA_CLIENTE ci
   where CLIEN_Entidad={entidad}
""".format(entidad=entidad,fecha_ini=fecha_ini,fecha_fin=fecha_fin)
    pd.options.mode.chained_assignment = None
    dts=conexion_base(consulta)
    #print consulta
    dts[0].loc[:,'sum_op_deb']=(100*dts[0].loc[:,'Monto Transacciones Debito']/dts[0].loc[:,'Monto Transacciones Debito_ant'])-100
    dts[0].loc[:,'sum_op_cred']=(100*dts[0].loc[:,'Monto Transacciones Credito']/dts[0].loc[:,'Monto Transacciones Credito_ant'])-100
    dts[0].loc[:,'sum_cant_op_deb']=(100*dts[0].loc[:,'Cantidad Transacciones Debito']/dts[0].loc[:,'Cantidad Transacciones Debito_ant'])-100
    dts[0].loc[:,'sum_cant_op_cred']=(100*dts[0].loc[:,'Cantidad Transacciones Credito_ant']/dts[0].loc[:,'Cantidad Transacciones Credito_ant'])-100
    
    #print dts[0].iloc[0,:]
    df1=dts[0].loc[dts[0]['sum_op_deb']>300,:]
    if len(df1)>0:
        df1.loc[:,'Motivo']='Operaciones Debito Monto'
        df1.loc[:,'Veces']=df1.loc[:,'sum_op_deb']
    df2=dts[0].loc[dts[0]['sum_op_cred']>300,:]
    if len(df2)>0:
        df2.loc[:,'Motivo']='Operaciones Credito Monto'   
        df2.loc[:,'Veces']=df2.loc[:,'sum_op_cred']
        df1 = df1.append(df2, ignore_index=True)
    df3=dts[0].loc[dts[0]['sum_cant_op_deb']>300,:]
    if len(df3)>0:    
        df3.loc[:,'Motivo']='Operaciones Debito Frecuencia' 
        df3.loc[:,'Veces']=df3.loc[:,'sum_cant_op_deb']
        df1 = df1.append(df3, ignore_index=True)
    df4=dts[0].loc[dts[0]['sum_cant_op_cred']>300,:]
    if len(df4)>0:    
        df4.loc[:,'Motivo']='Operaciones Credito Frecuencia'
        df4.loc[:,'Veces']=df4.loc[:,'sum_cant_op_cred']
        df1 = df1.append(df4, ignore_index=True) 
    df1.drop(columns=['Monto Transacciones Debito',
                      'Monto Transacciones Debito_ant',
                      'Monto Transacciones Credito',
                      'Monto Transacciones Credito_ant',
                      'Cantidad Transacciones Debito',
                    'Cantidad Transacciones Debito_ant',
                      'Cantidad Transacciones Credito',
                    'Cantidad Transacciones Credito_ant',
                      'sum_op_deb',
                    'sum_op_cred',
                      'sum_cant_op_deb',
                    'sum_cant_op_cred'
                      
                      
                      ],inplace=True)
        #print df1.iloc[0,:]
    df1=df1.replace([np.inf, -np.inf], np.nan)
    df1.dropna(axis=0,inplace =True)
    #print df1.iloc[0,:]
    return df1

def reporte_desviacion(fecha_ini,fecha_fin,entidad):
    consulta="""select ISNULL(CLIEN_Nombre1,'') + ' '+ISNULL(CLIEN_Nombre2,'')+' '+
ISNULL(CLIEN_Apellido1,'')+ ' '+ISNULL(CLIEN_Apellido2,'') as Nombre,
CLIEN_NumeroIdentificacion as [Numero de Identificacion],
cluster2 as cluster,
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Cliente=ci.CLIEN_idInterno and tr.TRANS_TipoTransaccion=2 
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'
  ) as [Monto Transacciones Debito],
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Cliente=ci.CLIEN_idInterno and tr.TRANS_TipoTransaccion=1 
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'
  )  as [Monto Transacciones Credito]



 from VA_CLIENTE ci
   where CLIEN_Entidad={entidad}
""".format(entidad=entidad,fecha_ini=fecha_ini,fecha_fin=fecha_fin)
    pd.options.mode.chained_assignment = None
    dts=conexion_base(consulta)
    agg1 = dts[0].groupby(['cluster'], axis=0).mean()
    agg1.columns=[str(i)+"_mean" for i in agg1.columns]
    agg1.reset_index(inplace=True)
    agg2 = dts[0].groupby(['cluster'], axis=0).std()
    agg2.columns=[str(i)+"_std" for i in agg2.columns]
    agg1.reset_index(inplace=True)
    df2b_left= pd.merge(dts[0], agg1, how='left',left_on='cluster', right_on='cluster')
    df2b_left= pd.merge(df2b_left, agg2, how='left',left_on='cluster', right_on='cluster')
    #df2b_left["Z Cantidad Transacciones Credito"]=(df2b_left['Cantidad Transacciones Credito']-df2b_left['Cantidad Transacciones Credito_mean'])/df2b_left['Cantidad Transacciones Credito_std']
    #df2b_left["Z Cantidad Transacciones Debito"]=(df2b_left['Cantidad Transacciones Debito']-df2b_left['Cantidad Transacciones Debito_mean'])/df2b_left['Cantidad Transacciones Debito_std']
    df2b_left["Z Monto Transacciones Debito"]=(df2b_left['Monto Transacciones Debito']-df2b_left['Monto Transacciones Debito_mean'])/df2b_left['Monto Transacciones Debito_std']
    df2b_left["Z Monto Transacciones Credito"]=(df2b_left['Monto Transacciones Credito']-df2b_left['Monto Transacciones Credito_mean'])/df2b_left['Monto Transacciones Credito_std']
    #df=df2b_left[(df2b_left["Z Cantidad Transacciones Credito"]>2) | (df2b_left["Z Cantidad Transacciones Debito"]>2) | (df2b_left["Z Monto Transacciones Debito"]>2) | (df2b_left["Z Monto Transacciones Credito"]>2)]
    df=df2b_left
    #print len(df)
    df2=df.loc[:,["Nombre","Numero de Identificacion","cluster","Monto Transacciones Debito","Monto Transacciones Credito","Z Monto Transacciones Debito","Z Monto Transacciones Credito"]]
    return df2

def reporte_pep(fecha_ini,fecha_fin,entidad):
    consulta="""select CLIEN_NumeroIdentificacion as [Numero de Identificacion],ISNULL(CLIEN_Nombre1,'') + ' '+ISNULL(CLIEN_Nombre2,'')+' '+
ISNULL(CLIEN_Apellido1,'')+ ' '+ISNULL(CLIEN_Apellido2,'') as Nombre,
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Cliente=ci.CLIEN_idInterno and tr.TRANS_TipoTransaccion=2 
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'
  ) as [Monto Transacciones Debito],
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Cliente=ci.CLIEN_idInterno and tr.TRANS_TipoTransaccion=1 
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'
  )  as [Monto Transacciones Credito],CLIEN_MontoTotalIngresoMensual

 from VA_CLIENTE ci
   where CLIEN_Entidad={entidad}

  
""".format(entidad=entidad,fecha_ini=fecha_ini,fecha_fin=fecha_fin)
    pd.options.mode.chained_assignment = None
    dts=conexion_base(consulta)
    #print dts[0].iloc[0,:]
    df=pd.DataFrame([])
    if len(dts[0])>0:
        df=dts[0][(dts[0]["Monto Transacciones Debito"]>2*dts[0]["CLIEN_MontoTotalIngresoMensual"]) | (dts[0]["Monto Transacciones Credito"]>2*dts[0]["CLIEN_MontoTotalIngresoMensual"])]
    
    #print len(df)
    return df
reportes=[
{'reporte':'1.Segmentacion riesgo cliente (Asociado) general',
'consulta':"""
select CLUS_nombre as [Factor de Riesgo],cl.cluster as [Nombre Segmento],
count(*) as Poblacion,CLUS_Descripcion as [Descripcion Segmento],
CLUS_fechA_SEGMENTACION AS [Fecha Segmentacion]
 from VA_CLUSTER cl
 left join VA_CLIENTE cli 
 on cl.cluster=cli.cluster2  and CLIEN_Entidad={entidad}
 where Clus_entidad={entidad} and CLUS_nombre='Cliente'
 group by CLUS_nombre,cl.cluster,CLUS_Descripcion,CLUS_fechA_SEGMENTACION
 

""".format(entidad=glentidad_id),
 'ancho_columnas':[10,10,10,100,25],
 'alias_columnas':['Factor de Riesgo','Nombre Segmento','Poblacion','Descripcion Segmento','Fecha Segmentacion']
 },
{'reporte':'2.Segmentacion factor de riesgo producto general',
'consulta':"""select CLUS_nombre as [Factor de Riesgo],cluster as [Nombre Segmento],clus_poblacion as Poblacion,CLUS_Descripcion as [Descripcion Segmento],
CLUS_fechA_SEGMENTACION AS [Fecha Segmentacion]
 from VA_CLUSTER where Clus_entidad={entidad} and CLUS_nombre='Producto'
""".format(entidad=glentidad_id),
 'ancho_columnas':[10,10,10,100,25],
 'alias_columnas':['Factor de Riesgo','Nombre Segmento','Poblacion','Descripcion Segmento','Fecha Segmentacion']
 },
{'reporte':'3.Segmentacion factor de riesgo canal general',
'consulta':"""

select CLUS_nombre as [Factor de Riesgo],cl.cluster as [Nombre Segmento],count(*) as Poblacion,
 CLUS_Descripcion as [Descripcion Segmento],
CLUS_fechA_SEGMENTACION AS [Fecha Segmentacion]
 from VA_CLUSTER cl 
  left join KP_CANAL can
 on cl.cluster=can.cluster2  and CANAL_Entidad={entidad}
 where Clus_entidad={entidad} and CLUS_nombre='Canal'
 group by CLUS_nombre ,cl.cluster,CLUS_Descripcion,CLUS_fechA_SEGMENTACION
 
""".format(entidad=glentidad_id),
 'ancho_columnas':[10,10,10,100,25],
 'alias_columnas':['Factor de Riesgo','Nombre Segmento','Poblacion','Descripcion Segmento','Fecha Segmentacion']
 },
{'reporte':'4.Segmentacion factor de riesgo jurisdiccion general',
'consulta':"""

 select CLUS_nombre as [Factor de Riesgo],cl.cluster as [Nombre Segmento],count(*) as Poblacion,CLUS_Descripcion as [Descripcion Segmento],
CLUS_fechA_SEGMENTACION AS [Fecha Segmentacion]
 from VA_CLUSTER cl
 left join KP_JURISDICCION jur
  on cl.cluster=jur.cluster2 and JURIS_Entidad={entidad}
 where Clus_entidad={entidad} and CLUS_nombre='Jurisdiccion'
  group by CLUS_nombre,cl.cluster,clus_poblacion,CLUS_Descripcion,CLUS_fechA_SEGMENTACION
  
""".format(entidad=glentidad_id),
 'ancho_columnas':[10,10,10,100,25],
 'alias_columnas':['Factor de Riesgo','Nombre Segmento','Poblacion','Descripcion Segmento','Fecha Segmentacion']
 },
{'reporte':'5.Segmentacion factor riesgo cliente especifico',
'consulta':"""

declare @diferencia int
set @diferencia=datediff(MM,'{fecha_ini}','{fecha_fin}')

select CLIEN_NumeroIdentificacion as [Numero de Identificacion],ISNULL(CLIEN_Nombre1,'') + ' '+ISNULL(CLIEN_Nombre2,'')+' '+
ISNULL(CLIEN_Apellido1,'')+ ' '+ISNULL(CLIEN_Apellido2,'') as Nombre,
tp.TIPER_Codigo  as [Tipo de Persona],ai.ACECO_Descripcion as [Actividad Economica],
oc.OCUPA_DescripcionGeneral as Ocupacion,
ISNULL(ci.CLIEN_MontoIngresoMensual,0) + ISNULL(ci.CLIEN_MontoOtrosIngresosMensual,0) as [Monto Total Ingreso Mensual],
ci.CLIEN_TotalPatrimonio as  [Total Patrimonio],
ci.CLIEN_MontoEgresoMensual  [Monto Total Egreso Mensual],
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Cliente=ci.CLIEN_idInterno and tr.TRANS_TipoTransaccion=2 
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'
  )/@diferencia as [Monto Transacciones Debito],
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Cliente=ci.CLIEN_idInterno and tr.TRANS_TipoTransaccion=1 
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'
  )/@diferencia  as [Monto Transacciones Credito],
  (select ISNULL(count(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Cliente=ci.CLIEN_idInterno and tr.TRANS_TipoTransaccion=2 
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'
  )/@diferencia as [Cantidad Transacciones Debito],
    (select ISNULL(count(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Cliente=ci.CLIEN_idInterno and tr.TRANS_TipoTransaccion=1
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'
  )/@diferencia as [Cantidad Transacciones Credito],cluster2 as Cluster


 from VA_CLIENTE ci
 left join KG_TIPOPERSONA tp 
 on ci.CLIEN_TipoPersona=TIPER_IdInterno
 left join KG_ACTIVIDADECONOMICA ai
 on ci.CLIEN_ActividadEconomicacliente=ai.ACECO_IdInterno
 left join KG_OCUPACION oc
 on ci.CLIEN_Ocupacion= oc.OCUPA_IdInterno
   where CLIEN_Entidad={entidad}


""".format(entidad=glentidad_id,fecha_ini=glfecha_ini,fecha_fin=glfecha_fin),
 'ancho_columnas':[10,10,10,10,10,10,10,10,10,10,10,10,10],
 'alias_columnas':['Numero de Identificacion','Nombre','Tipo de Persona','Actividad Economica','Ocupacion',
                   'Monto Total Ingreso Mensual','Monto Total Egreso Mensual','Total Patrimonio','Monto Transacciones Debito','Monto Transacciones Credito',
                   'Cantidad Transacciones Debito','Cantidad Transacciones Credito','Cluster'
                   ]
 },
{'reporte':'6.Segmentacion factor riesgo producto especifico',
'consulta':"""

declare @diferencia int
set @diferencia=datediff(MM,'{fecha_ini}','{fecha_fin}')

select PRODU_Codigo as [Codigo del Producto],nm.NICME_Codigo as [Nicho],
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Producto=pro.PRODU_IdInterno and tr.TRANS_TipoTransaccion=2 
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'

  )/@diferencia as [Monto Transacciones Debito],
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Producto=pro.PRODU_IdInterno and tr.TRANS_TipoTransaccion=1 
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'

  )/@diferencia as [Monto Transacciones Credito],
  (select ISNULL(count(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Producto=pro.PRODU_IdInterno and tr.TRANS_TipoTransaccion=2 
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'

  )/@diferencia  as [Cantidad Transacciones Debito],
(select ISNULL(count(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr
 inner join VA_CLIENTExPRODUCTO cp2 on tr.TRANS_CLIENTExPRODUCTO=cp2.CLXPR_IdInterno
  where tr.TRANS_Entidad={entidad} and 
 cp2.CLXPR_Producto=pro.PRODU_IdInterno and tr.TRANS_TipoTransaccion=1 
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'

  )/@diferencia as [Cantidad Transacciones Credito],cluster2 as Cluster
 from KP_PRODUCTO pro
inner join KG_NICHOMERCADO nm
on pro.PRODU_NichoMercado=nm.NICME_IdInterno
where pro.PRODU_Entidad={entidad}



""".format(entidad=glentidad_id,fecha_ini=glfecha_ini,fecha_fin=glfecha_fin),
 'ancho_columnas':[10,10,10,10,10,10,10],
 'alias_columnas':['Codigo del Producto','Nicho','Monto Transacciones Debito','Monto Transacciones Credito','Cantidad Transacciones Debito',
                   'Cantidad Transacciones Credito','Cluster'
                   ]
 },
{'reporte':'7.Segmentacion factor riesgo canal especifico',
'consulta':"""

declare @diferencia int
set @diferencia=datediff(MM,'{fecha_ini}','{fecha_fin}')

select CANAL_Codigo as [Nombre Canal], CANAL_Descripcion as [Descripcion Canal],
nc.NATCA_Codigo as [Naturaleza Canal],cc.CARCA_Codigo as [Caracteristica Canal],
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr where tr.TRANS_Entidad={entidad} and 
 tr.TRANS_Canal=cn.CANAL_idInterno and tr.TRANS_TipoTransaccion=2 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'
)/@diferencia as [Monto Transacciones Debito],
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr where tr.TRANS_Entidad={entidad} and 
 tr.TRANS_Canal=cn.CANAL_idInterno and tr.TRANS_TipoTransaccion=1 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'
)/@diferencia as [Monto Transacciones Credito],
(select ISNULL(count(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr where tr.TRANS_Entidad={entidad} and 
 tr.TRANS_Canal=cn.CANAL_idInterno and tr.TRANS_TipoTransaccion=2 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'
)/@diferencia as [Cantidad Transacciones Debito],
(select ISNULL(count(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr where tr.TRANS_Entidad={entidad} and 
 tr.TRANS_Canal=cn.CANAL_idInterno and tr.TRANS_TipoTransaccion=1 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'
)/@diferencia as [Cantidad Transacciones Credito],cluster2 as Cluster
  from KP_CANAL cn
  inner join KG_NATURALEZACANAL nc
  on cn.CANAL_Naturaleza=nc.NATCA_IdInterno
  inner join KG_CARACTERISTICACANAL cc
  on cn.CANAL_Caracteristica=cc.CARCA_IdInterno
  where CANAL_Entidad={entidad}




""".format(entidad=glentidad_id,fecha_ini=glfecha_ini,fecha_fin=glfecha_fin),
 'ancho_columnas':[10,10,10,10,10,10,10,10,10],
 'alias_columnas':['Nombre Canal','Naturaleza Canal','Caracteristica Canal','Descripcion Canal','Monto Transacciones Debito','Monto Transacciones Credito',
                   'Cantidad Transacciones Debito',
                   'Cantidad Transacciones Credito','Cluster'
                   ]
 },
{'reporte':'8.Segmentacion factor riesgo jurisdiccion especifica',
'consulta':"""

declare @diferencia int
set @diferencia=datediff(MM,'{fecha_ini}','{fecha_fin}')

select cj.CARJU_NombreDepartamentoDivipol as [Departamento], cj.CARJU_NombreCiudadDivipol as [Ciudad],
 cj.CARJU_RiesgoIndiceTransparecia as [Riesgo Indice Transparencia],
 cj.CARJU_RiesgoCultivoIlicito as [Riesgo Ilicito],
 cj.CARJU_RiesgoActosTerroristas as [Riesgo Terrorista],
 cj.CARJU_RiesgoZonaFronteriza as [Riesgo Zona Frontera],
 cj.CARJU_RiesgoDeZonaFranca as [Riesgo Zona Franca],
 cj.CARJU_AsentamientoFARCDepartamento as [Riesgo FARC],
 cj.CARJU_PresenciaGruposArmados as  [Riesgo Armados],
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr where tr.TRANS_Entidad={entidad} and 
 tr.TRANS_CARACTERISTICAJURISDICCION=cj.CARJU_IdInterno and tr.TRANS_TipoTransaccion=2 
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'

)/@diferencia as [Monto Transacciones Debito],
(select ISNULL(sum(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr where tr.TRANS_Entidad={entidad} and 
 tr.TRANS_CARACTERISTICAJURISDICCION=cj.CARJU_IdInterno and tr.TRANS_TipoTransaccion=1
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'

)/@diferencia as [Monto Transacciones Credito],
(select ISNULL(count(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr where tr.TRANS_Entidad={entidad} and 
 tr.TRANS_CARACTERISTICAJURISDICCION=cj.CARJU_IdInterno and tr.TRANS_TipoTransaccion=2
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'

)/@diferencia as [Cantidad Transacciones Debito],
(select ISNULL(count(tr.trans_montoMonedaOriginal),0)
 from VA_TRANSACCION tr where tr.TRANS_Entidad={entidad} and 
 tr.TRANS_CARACTERISTICAJURISDICCION=cj.CARJU_IdInterno and tr.TRANS_TipoTransaccion=1
 and tr.TRANS_FechaRealizada>'{fecha_ini} 00:00:00'
 and tr.TRANS_FechaRealizada<'{fecha_fin} 00:00:00'

)/@diferencia as [Cantidad Transacciones Credito],cluster2 as Cluster
  from KG_CARACTERISTICAJURISDICCION cj
 inner join KP_JURISDICCION jur
 on cj.CARJU_IdInterno=jur.JURIS_Caracteristica
where jur.JURIS_Entidad={entidad}


""".format(entidad=glentidad_id,fecha_ini=glfecha_ini,fecha_fin=glfecha_fin),
 'ancho_columnas':[10,10,10,10,10,10,10,10,10,10,10,10,10,10],
 'alias_columnas':['Departamento','Ciudad','Riesgo Indice Transparencia','Riesgo Ilicito','Riesgo Terrorista','Riesgo Zona Frontera',
                   'Riesgo Zona Franca','Riesgo FARC',
                   'Riesgo Armados','Monto Transacciones Debito','Monto Transacciones Credito',
                   'Cantidad Transacciones Debito','Cantidad Transacciones Credito','Cluster'
                   ]
 },
{'reporte':'9.Alerta por Factor Riesgo',
'consulta':"""

select 
(select distinct  CLUS_Fecha_Segmentacion from VA_CLUSTER where CLUS_Entidad={entidad} and CLUS_Nombre='Cliente') as [Fecha Segmentacion],
'Cliente' as Factor,CLIEN_NumeroIdentificacion as Identificacion,cluster as [Segmento Anterior],cluster2  as [Segmento Actual] from VA_CLIENTE where CLIEN_Entidad={entidad} and cluster<>cluster2
union
select 
(select distinct  CLUS_Fecha_Segmentacion from VA_CLUSTER where CLUS_Entidad={entidad} and CLUS_Nombre='Producto') as [Fecha Segmentacion],
'Producto' as Factor,PRODU_Codigo as Identificacion,cluster as [Segmento Anterior],cluster2  as [Segmento Actual] from KP_PRODUCTO where PRODU_Entidad={entidad} and cluster<>cluster2

union
select 
(select distinct  CLUS_Fecha_Segmentacion from VA_CLUSTER where CLUS_Entidad={entidad} and CLUS_Nombre='Canal') as [Fecha Segmentacion],
'Canal' as Factor,CANAL_Codigo as Identificacion,cluster as [Segmento Anterior],cluster2  as [Segmento Actual] from KP_CANAL where CANAL_Entidad={entidad} and cluster<>cluster2



""".format(entidad=glentidad_id,fecha_ini=glfecha_ini,fecha_fin=glfecha_fin),
 'ancho_columnas':[30,10,10,10,10],
 'alias_columnas':['Fecha Segmentacion','Factor','Identificacion','Segmento Anterior','Segmento Actual']
 }
]

formato={
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#203764',
    'font_color': 'white',
    'border': 1}
writer = pd.ExcelWriter('C:\\archivos_salida\\Reportes.xlsx', engine='xlsxwriter')
cont=0
while cont<len(reportes):
    k=cont
    nombre_reporte=reportes[k]['reporte'][0:31]
    print reportes[k]['reporte']    
    dts=conexion_base(reportes[k]['consulta'])
    if len(dts[0])>0:
        
        #dts[0].columns=reportes[k]['alias_columnas']
        #print dts[0].loc[:,reportes[k]['alias_columnas']]
        #print dts[0].loc[0,:]
        df=dts[0].loc[:,reportes[k]['alias_columnas']]
         
        df.to_excel(writer, sheet_name=nombre_reporte,index=False)
        workbook = writer.book
        worksheet = writer.sheets[nombre_reporte]
        
        
        header_format = workbook.add_format(formato)
        arrancho_columnas=reportes[k]['ancho_columnas']
        ncol=0
        while ncol<len(df.columns):
            worksheet.write(0, ncol, df.columns[ncol], header_format)
            worksheet.set_column(ncol, ncol, int(arrancho_columnas[ncol]))
            ncol=ncol+1
    cont=cont+1




#Reporte2
print "10.Reporte Desviacion"
df=reporte_desviacion(glfecha_ini,glfecha_fin,glentidad_id)
df.to_excel(writer, sheet_name='10.Reporte Desviacion',index=False)
workbook = writer.book
worksheet = writer.sheets['10.Reporte Desviacion']
header_format = workbook.add_format(formato)
arrancho_columnas=[10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]
ncol=0
while ncol<len(df.columns):
    worksheet.write(0, ncol, df.columns[ncol], header_format)
    worksheet.set_column(ncol, ncol, int(arrancho_columnas[ncol]))
    ncol=ncol+1


#Reporte1
print "11.Reporte Perfilamiento"
df=reporte_perfilamiento(glfecha_ini,glfecha_fin,glentidad_id)
df.to_excel(writer, sheet_name='11.Reporte Perfilamiento',index=False)
workbook = writer.book
worksheet = writer.sheets['11.Reporte Perfilamiento']
header_format = workbook.add_format(formato)
arrancho_columnas=[10,10,10,10]
ncol=0
while ncol<len(df.columns):
    worksheet.write(0, ncol, df.columns[ncol], header_format)
    worksheet.set_column(ncol, ncol, int(arrancho_columnas[ncol]))
    ncol=ncol+1
    
#Reporte3
print "12.Reporte Ingreso"
df=reporte_pep(glfecha_ini,glfecha_fin,glentidad_id)
df.to_excel(writer, sheet_name='12.Reporte Ingreso',index=False)
workbook = writer.book
worksheet = writer.sheets['12.Reporte Ingreso']
header_format = workbook.add_format(formato)
arrancho_columnas=[10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]
ncol=0
while ncol<len(df.columns):
    worksheet.write(0, ncol, df.columns[ncol], header_format)
    worksheet.set_column(ncol, ncol, int(arrancho_columnas[ncol]))
    ncol=ncol+1
        
writer.save()    

    
  
