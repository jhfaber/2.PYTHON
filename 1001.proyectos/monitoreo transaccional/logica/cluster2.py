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


glvalor_mayor=0
glcantidad_cluster_mayor=0
modelo_kmean={}

reload(sys)
sys.setdefaultencoding("utf-8")

form = cgi.FieldStorage()
tipo2 = form.getvalue("tipo")
#tipo2="transacciones"


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
    
def analiza_pinta_cluster(datos,columnas_cluster,pdf,range_n_clusters,fila):
    global glvalor_mayor
    global glcantidad_cluster_mayor
    columnas=[]
    df_2=datos.loc[:,columnas_cluster]
    print("Columnas Cluster ",columnas_cluster)
    X = StandardScaler().fit_transform(df_2)
    print X
    
    for n_clusters in range_n_clusters:        
        plt.figure(figsize=(3, 3))
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.set_size_inches(18, 7)
        ax1.set_xlim([-0.1, 1])
        ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])
    
        clusterer = KMeans(n_clusters=n_clusters, random_state=10)
        cluster_labels = clusterer.fit_predict(X)
        
        
        silhouette_avg = silhouette_score(X, cluster_labels)
        print("Para n cluster =", n_clusters, "Promedio del coeficiente de silueta :", silhouette_avg)
        if silhouette_avg>glvalor_mayor:
            glvalor_mayor=silhouette_avg
            glcantidad_cluster_mayor=n_clusters
            modelo_kmean=clusterer
        sample_silhouette_values = silhouette_samples(X, cluster_labels)
    
        y_lower = 10
        for i in range(n_clusters):
    
            ith_cluster_silhouette_values = \
                sample_silhouette_values[cluster_labels == i]
    
            ith_cluster_silhouette_values.sort()
    
            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i
    
            color = cm.nipy_spectral(float(i) / n_clusters)
            ax1.fill_betweenx(np.arange(y_lower, y_upper),
                              0, ith_cluster_silhouette_values,
                              facecolor=color, edgecolor=color, alpha=0.7)
    
    
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
    
    
            y_lower = y_upper + 10  # 10 for the 0 samples
    
        ax1.set_title("Grafica del coeficiente de silueta")
        ax1.set_xlabel("Valores del coeficiente de silueta")
        ax1.set_ylabel("Cluster")
    
        
        ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
    
        ax1.set_yticks([])
        ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
    
        # Pinta las 2 dimensiones
        colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
        ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
                    c=colors, edgecolor='k')
    
        
        centers = clusterer.cluster_centers_
        # Dibujar circulos en los centroides
        ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
                    c="white", alpha=1, s=200, edgecolor='k')
    
        for i, c in enumerate(centers):
            ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
                        s=50, edgecolor='k')
    
        ax2.set_title("Datos Clusterizados")
        ax2.set_xlabel("Primera Caracteristica")
        ax2.set_ylabel("Segunda Caracteristica")
        plt.text(0.05,0.926,columnas_cluster, transform=fig.transFigure, size=10)
        plt.suptitle((fila["nombre"]+" - Analisis  de Silueta "
                      "con n clusters = %d" % n_clusters),
                     fontsize=14, fontweight='bold')
    
        pdf.savefig()
        plt.close()

    
    return cluster_labels
def rotacion_columnas_cluster(datos,columnas,pdf,fila):
    cantidad=fila["minimo_cantidad_estudio"]
    while cantidad<=len(columnas) and cantidad<=fila["maximo_cantidad_estudio"]:    
        inicial=0
        while inicial+cantidad<=len(columnas):
            salto=1
            if cantidad==1:
                salto=len(columnas)-inicial
            while inicial+salto+cantidad-1<=len(columnas):
                arrcol=[]
                #print inicial
                n=inicial
                arrcol.append(columnas[n])
                n=n+salto
                while len(arrcol)<cantidad:
                    arrcol.append(columnas[n])
                    n=n+1
                #print arrcol
                try:
                    analiza_pinta_cluster(datos,arrcol,pdf,fila["cantidad_cluster_estudio"],fila)
                    print "Promedio Mayor "+str(glvalor_mayor)
                    print "Cantidad de Cluster Recomendada "+str(glcantidad_cluster_mayor)
                    
                except:
                    print "error"
                salto=salto+1
            
            inicial=inicial+1
        cantidad=cantidad+1

def actualizacion_cluster(datos,columnas,pdf,fila,cantidad_cluster):
    cluster_labels=analiza_pinta_cluster(datos,columnas,pdf,[cantidad_cluster],fila)
    arr=datos[fila["llave_consulta"]]
    df2= arr.to_frame()
    df2["cluster"]=cluster_labels
    df3=df2.loc[1:2,:]
    #df2[arr_clusterizacion[n]["llave_consulta"]]=arr
    #print type(arr.to_frame())
    caden=df2.to_json(orient='records')
    llave_tabla=fila["llave_tabla"]
    llave_consulta=fila["llave_consulta"]
    tabla=fila["tabla"]
    
    
    cadena_sql="""DECLARE @json NVARCHAR(MAX) SET @json = N'{caden}'
 
    update b set b.cluster=a.cluster FROM 
     OPENJSON ( @json ) 
    WITH (  
                    {llave_consulta}   varchar(200) '$.{llave_consulta}' , 
                    cluster varchar(200) '$.cluster'
    
     )a
     inner join {tabla} b on a.{llave_consulta}=b.{llave_tabla}
    
    """.format(caden=caden,llave_tabla=llave_tabla,llave_consulta=llave_consulta,tabla=tabla)
    conexion_base_insert(cadena_sql)
     



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




json_asociado=open("C:\\consofi\\cluster2.json").read()
arr_clusterizacion=ast.literal_eval(json_asociado)

import pickle
glentidad_id=form.getvalue("entidad")
glfecha_ini=form.getvalue("fecha_ini")
glfecha_fin=form.getvalue("fecha_fin")

n=0
while n<len(arr_clusterizacion):
    fila=arr_clusterizacion[n]
    consulta=arr_clusterizacion[n]["consulta"]
    consulta=consulta.replace("@identidad@",str(glentidad_id))
    consulta=consulta.replace("@fecha_ini@",str(glfecha_ini))
    consulta=consulta.replace("@fecha_fin@",str(glfecha_fin))
    
    df=conexion_base(consulta)
    columnas_cluster=arr_clusterizacion[n]["columnas_cluster"]
    llave="id_cliente"
    try:
        if arr_clusterizacion[n]["realiza_estudio"]==1:
            print arr_clusterizacion[n]["nombre"]
            modelo_archivo = "modelo_archivo_"+str(glentidad_id)+"_"+arr_clusterizacion[n]["nombre"]+".pkl"
            modelo_archivo_pkl = open(modelo_archivo, 'rb')
            modelo_kmean=pickle.load(modelo_archivo_pkl)
            modelo_archivo_pkl.close()
            llave_tabla=fila["llave_tabla"]
            llave_consulta=fila["llave_consulta"]
            columnas_cluster=fila["columnas_cluster"]
            tabla=fila["tabla"]
            
    
            df_2=df[0].loc[:,columnas_cluster]
            #print("Columnas Cluster ",columnas_cluster)
            scaler = StandardScaler()
            X = scaler.fit_transform(df_2)        
            #actualizacion_cluster(df[0],columnas_cluster,pdf,arr_clusterizacion[n],glcantidad_cluster_mayor)
            y_kmeans2=modelo_kmean.fit_predict(X)
            columnas_cluster.append(llave_consulta)
            df_3=df[0].loc[:,columnas_cluster]
            df_3["cluster2"]=y_kmeans2
            caden=df_3.to_json(orient='records')
    
            
           
            cadena_sql="""DECLARE @json NVARCHAR(MAX) SET @json = N'{caden}'
            
             update b set b.cluster=b.cluster2 FROM 
             OPENJSON ( @json ) 
            WITH (  
                            {llave_consulta}   varchar(200) '$.{llave_consulta}' , 
                            cluster2 varchar(200) '$.cluster2'
            
             )a
             inner join {tabla} b on a.{llave_consulta}=b.{llave_tabla}
             
            update b set b.cluster2=a.cluster2 FROM 
             OPENJSON ( @json ) 
            WITH (  
                            {llave_consulta}   varchar(200) '$.{llave_consulta}' , 
                            cluster2 varchar(200) '$.cluster2'
            
             )a
             inner join {tabla} b on a.{llave_consulta}=b.{llave_tabla}
            
            """.format(caden=caden,llave_tabla=llave_tabla,llave_consulta=llave_consulta,tabla=tabla)
            
            #print cadena_sql
            conexion_base_insert(cadena_sql)
            
        #print df_2.iloc[0,:]
        
    except:
        error=""
        arrerr=sys.exc_info()
        er=0
        while er<len(arrerr):
            error=error+str(arrerr[er])+" "
            er=er+1
        print "Error "+error
    n=n+1
