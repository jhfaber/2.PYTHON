#!/usr/bin/env python
# -*- coding: utf-8 -*-
print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n\n\n")
#print("Hola")

import warnings
warnings.filterwarnings("ignore")

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

def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
    return s.decode()
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
    global modelo_kmean
    columnas=[]
    cluster_labels=[]
    df_2=datos.loc[:,columnas_cluster]
    #print("Columnas Cluster ",columnas_cluster)
    #print range_n_clusters 
    scaler = StandardScaler()
    X = scaler.fit_transform(df_2)
    for n_clusters in range_n_clusters:
        if (len(datos)-1)>n_clusters:
            #print len(datos)
            #print n_clusters
            plt.figure(figsize=(3, 3))
            fig, (ax1, ax2) = plt.subplots(1, 2)
            fig.set_size_inches(18, 7)
            ax1.set_xlim([-0.1, 1])
            ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])
        
            clusterer = KMeans(n_clusters=n_clusters, random_state=10)
            #print "Datos"
            #print X
            cluster_labels = clusterer.fit_predict(X)
            
            
            silhouette_avg = silhouette_score(X, cluster_labels)
            #print("Para n cluster =", n_clusters, "Promedio del coeficiente de silueta :", silhouette_avg)
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

        else:
            print "Cantidad de registros insuficientes 1"
    return cluster_labels
def guarda_clusterizacion(dts,entidad,nombre,clave,arrcualitativas,arrcualitativas_nombre):
    #print dts.iloc[0,:]
    df2=pd.value_counts(dts[clave]).to_frame()
    df2=df2.reset_index()
    df2.columns=['cluster','cantidad']
    
   
    n=0
    
    while n<len(arrcualitativas_nombre):
        dts[arrcualitativas_nombre[n]]=dts[arrcualitativas_nombre[n]].apply(lambda x: elimina_tildes(x))
        n=n+1
    dsres=agrupa_describe(dts,clave,arrcualitativas,arrcualitativas_nombre)
    dsres=pd.merge(dsres,df2, left_on="cluster", right_on="cluster")
    #print dres2.iloc[0,:]
    #dsres['total'].apply(lambda x: elimina_tildes(x))
    caden=dsres.to_json(orient='records')
    caden=caden.replace("'","''")
    
    cadena_act=""" DECLARE @json NVARCHAR(MAX) SET @json = N'{caden}'
    delete from VA_CLUSTER where CLUS_Entidad={entidad} and CLUS_Nombre='{nombre}'
    insert into VA_CLUSTER (CLUS_Entidad,CLUS_Fecha_Segmentacion,cluster,CLUS_Descripcion,CLUS_Nombre,CLUS_Poblacion)
    SELECT {entidad},dateadd(HH,-5,getutcdate()),{clave},total,'{nombre}',cantidad FROM 
     OPENJSON (@json) 
    WITH (  
                    {clave}   varchar(200) '$.{clave}' , 
                    total varchar(max) '$.total',
                    cantidad int  '$.cantidad'
     
         ) 
    """.format(caden=caden,entidad=entidad,nombre=nombre,clave=clave)
    #print cadena_act
    conexion_base_insert(cadena_act)

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
                    if len(datos)>2:
                        analiza_pinta_cluster(datos,arrcol,pdf,fila["cantidad_cluster_estudio"],fila)
                        #print "Promedio Mayor "+str(glvalor_mayor)
                        #print "Cantidad de Cluster Recomendada "+str(glcantidad_cluster_mayor)
                    else:
                        print "Cantidad de registros insuficientes 2"
                    
                except:
                    print "Error "+sys.exc_info()[0]
                    mmmm=8888
                salto=salto+1
            
            inicial=inicial+1
        cantidad=cantidad+1

def actualizacion_cluster(datos,columnas,pdf,fila,cantidad_cluster):
    cluster_labels=analiza_pinta_cluster(datos,columnas,pdf,[cantidad_cluster],fila)
    
   #print "Paso1"
    
    if len(cluster_labels)>0:
        #print "Paso2"
        arr=datos[fila["llave_consulta"]]
        df2= arr.to_frame()
        datos["cluster"]=cluster_labels
        df2["cluster"]=cluster_labels
        df3=df2.loc[1:2,:]
        #df2[arr_clusterizacion[n]["llave_consulta"]]=arr
        #print type(arr.to_frame())
        caden=df2.to_json(orient='records')
        #caden=df3.to_json(orient='records')
        llave_tabla=fila["llave_tabla"]
        llave_consulta=fila["llave_consulta"]
        tabla=fila["tabla"]
        
        datos.drop(columns=[llave_consulta], axis=1,inplace=True) 
        #print datos.iloc[0,:]
        
        cadena_sql="""DECLARE @json NVARCHAR(MAX) SET @json = N'{caden}'
     
        update b set b.cluster=a.cluster, b.cluster2=a.cluster FROM 
         OPENJSON ( @json ) 
        WITH (  
                        {llave_consulta}   varchar(200) '$.{llave_consulta}' , 
                        cluster varchar(200) '$.cluster'
        
         )a
         inner join {tabla} b on a.{llave_consulta}=b.{llave_tabla}
        
        """.format(caden=caden,llave_tabla=llave_tabla,llave_consulta=llave_consulta,tabla=tabla)
        #print "Hola"
        #print cadena_sql
        conexion_base_insert(cadena_sql)
        
        #arrcat=fila["columnas_cluster_5"]
        #arrcat2=fila["nombre_cluster_categoricas"]
        
        
        #arrcolcluster=np.array(fila["columnas_cluster"])
        #arrcatnp=np.array(arrcat)
        #arrcat2np=np.array(arrcat2)
        #arrl1=list(arrcolcluster[arrcatnp!=0])
        #print arrcat2np
        #arrl2=list(arrcat2np[arrcatnp!=0])
        #print list(arrcat2np[arrcat2np!=0])
        arrl1=list(fila["categoricas"])
        arrl2=list(fila["categoricas_descripcion"])
        #print arrl1
        #print arrl2
        guarda_clusterizacion(datos,glentidad_id,fila["nombre"],'cluster',arrl1,arrl2)


def agrupa_describe(df,clave,arrcualitativas,arrcualitativas_nombre):

    #print arrcualitativas
    #print arrcualitativas_nombre
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
    if len(arrcualitativas)>0:
        n=0
        while n<len(arrclaves):
            dftmp=df_cual_g3.loc[arrclaves.index[n],:].head()
            dftmp.drop(['0_x','0_y'], axis=1,inplace=True) 
            arr_resumen.append({clave:arrclaves.index[n],'resumen': dftmp.to_string()})
            n=n+1
            df_resumen=pd.DataFrame(arr_resumen)
            df_resumen=df_resumen.set_index(clave)
    #print df.iloc[0,:]
    
    
    if len(arrcualitativas)>0:
        #print "Elimina"
        df.drop(arrcualitativas, axis=1,inplace=True)
        df.drop(arrcualitativas_nombre, axis=1,inplace=True) 
    
    df2=pd.value_counts(df['cluster']).to_frame()
    df2["descripcion"]=""
    
   
    
    #print df_curt.iloc[0,:]
    #print clave
    df3=df.groupby(clave).max()
    df3a=df3.copy()
    #print df.dtypes
    #print clave
    #print df.iloc[0,:]
    cadena2=""
    from scipy.stats import kurtosis
    j=0
    while j<len(df3):
        #print "Cluster"
        cluster_t=df3.iloc[j,:].name
        #print cluster_t
        cadena3=""
        i=0
        while i<len(df.columns):
            #print df.types[i]
            #print df.loc[:,df.columns[i]]
            
            try:
                if df.columns[i]!=clave:
                    #print df.columns[i]
                    s1=df.loc[df[clave]==j,df.columns[i]]
                    s1.dropna(inplace=True)            
                    s1=pd.to_numeric(s1, errors='ignore')
                    #print s1
                    kur=kurtosis(s1,nan_policy='omit')
                    #df3a.loc[cluster_t,'curtosis_'+df.columns[i]]=kur
                    
                    media=np.mean(s1)
                    #df3a.loc[cluster_t,'media_'+df.columns[i]]=media
                    
                    desv=np.std(s1)
                    #df3a.loc[cluster_t,'desviacion_'+df.columns[i]]=desv
                    
                    cadena3=cadena3+'Desviación '+df.columns[i]+' = '+str(desv) +'\n' +'Media '+df.columns[i]+' = '+str(media) +'\n' + 'Curtosis '+df.columns[i]+' = '+str(kur) +'\n'
            except:
                c=1        
            i=i+1
        df3a.loc[cluster_t,'total']=cadena3
        j=j+1
    

        
    #df3, Fila por cluster
    #print df.shape
    #print df3a.iloc[0,:]
    #print df3.iloc[1,:]
    lista_columnas_cuant=[str(i) for i in df3.columns]
    lista_max=["max_"+str(i) for i in df3.columns]
    df3.columns=lista_max
    df4=df.groupby(clave).min()
    lista_min=["min_"+str(i) for i in df4.columns]
    df4.columns=lista_min
    dt5=pd.merge(df3,df4,left_index=True,right_index=True)
    if len(arrcualitativas)>0:
        dt5=pd.merge(dt5,df_resumen,left_index=True,right_index=True)
    #df4=df4[lista_min]
    #print dt5.iloc[0,:]
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
    if len(arrcualitativas)>0:
        dt5['total']=dt5['total']+dt5['resumen']
        
    dt5['total2']=df3a['total']
    dt5['total']=dt5['total']+'\n'+dt5['total2']
    dt6=dt5[[clave,'total']]
    
    
    #print dt5.loc[0,['resumen']]
    #f = open ("C:\\archivos_salida\\test.txt",'w')
    #f.write(str(dt5.loc[0,['resumen']]))
    #f.close()
    return dt6
    #escribir_excel(dt6,"C:\\archivos_salida\\test.xlsx","xlsxwriter",[20,100])

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




json_asociado=open("C:\\consofi\\cluster.json").read()
arr_clusterizacion=ast.literal_eval(json_asociado)

import pickle
with PdfPages('C:\\archivos_salida\\salida_cluster.pdf') as pdf:
    glentidad_id=form.getvalue("entidad")
    glfecha_ini=form.getvalue("fecha_ini")
    glfecha_fin=form.getvalue("fecha_fin")
    n=0
    while n<len(arr_clusterizacion):
        print arr_clusterizacion[n]["nombre"]
        consulta=arr_clusterizacion[n]["consulta"]
        consulta=consulta.replace("@identidad@",str(glentidad_id))
        consulta=consulta.replace("@fecha_ini@",str(glfecha_ini))
        consulta=consulta.replace("@fecha_fin@",str(glfecha_fin))
        
        reset=arr_clusterizacion[n]["reset"]
        reset=reset.replace("@identidad@",str(glentidad_id))
        reset=reset.replace("@fecha_ini@",str(glfecha_ini))
        reset=reset.replace("@fecha_fin@",str(glfecha_fin))
        
        df=conexion_base(consulta)
        conexion_base_insert(reset)
        columnas_cluster=arr_clusterizacion[n]["columnas_cluster"]
        llave="id_cliente"
        
        if arr_clusterizacion[n]["realiza_estudio"]==1:
            rotacion_columnas_cluster(df[0],columnas_cluster,pdf,arr_clusterizacion[n])
        elif  arr_clusterizacion[n]["realiza_actualizacion_cluster"]==1 and len(df[0])>2:
            actualizacion_cluster(df[0],columnas_cluster,pdf,arr_clusterizacion[n],arr_clusterizacion[n]["cantidad_cluster_actualizacion"])
             
        #print arr_clusterizacion[n]["realiza_estudio"]
        #print arr_clusterizacion[n]["realiza_actualizacion_cluster_mayor"]
        #print len(df[0])
        if  arr_clusterizacion[n]["realiza_estudio"]==1 and arr_clusterizacion[n]["realiza_actualizacion_cluster_mayor"]==1 and len(df[0])>2:
            #print "Actualiza"
            actualizacion_cluster(df[0],columnas_cluster,pdf,arr_clusterizacion[n],glcantidad_cluster_mayor)
            
            modelo_archivo = "modelo_archivo_"+str(glentidad_id)+"_"+arr_clusterizacion[n]["nombre"]+".pkl"
            modelo_archivo_pkl = open(modelo_archivo, 'wb')
            pickle.dump(modelo_kmean, modelo_archivo_pkl)
            modelo_archivo_pkl.close()
        else:
            if len(df[0])<2:
                print "Cantidad de registros insuficientes 3 "+str(len(df[0]))
    
        
        n=n+1
