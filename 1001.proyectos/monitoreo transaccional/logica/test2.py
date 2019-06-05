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
reload(sys)
sys.setdefaultencoding("utf-8")



form = cgi.FieldStorage()
tipo2 = form.getvalue("tipo")
#tipo2="transacciones"

json_asociado=open("C:\\consofi\\general.json").read()
arr_general=ast.literal_eval(json_asociado)
glarchivos_config=arr_general["configuracion"]
gl_archivos=arr_general["orden"]



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


def homolga(indice):

    #print(indice)
    columna=glvalidacion_asociado["datos_archivo"][indice]
    
    campo_destino=columna["campo_destino"]
    tipo=columna["tipo"]
    permite_valor_defecto=columna["permite_valor_defecto"]
    valor_defecto=columna["valor_defecto"]
    numero=columna["numero_columna_excel"]-1
    
    if columna.get("entero")==1:
        gldfcompara[gldfcompara.columns[numero]+"_bk"]=gldfcompara[gldfcompara.columns[numero]]
        #gldfcompara.loc[arr2==True,gldfcompara.columns[numero]]=int(float(gldfcompara[gldfcompara.columns[numero]]))
        arr2=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.replace(".","",1).str.isdigit()
        gldfcompara.loc[arr2,gldfcompara.columns[numero]+"_int"]=gldfcompara.loc[arr2,gldfcompara.columns[numero]].astype(float)
        gldfcompara[gldfcompara.columns[numero]+"_int"].fillna(0,inplace=True)
        gldfcompara[gldfcompara.columns[numero]+"_int"]=gldfcompara[gldfcompara.columns[numero]+"_int"].astype(int)
        gldfcompara[gldfcompara.columns[numero]]=gldfcompara[gldfcompara.columns[numero]+"_int"]
        
    if tipo==1:        
        consulta="select distinct "+columna["tabla_llave"]+","+columna["tabla_texto"]+" from "+columna["tabla_homologa"] + " tb1 "
        filtro_adicional=str(glvalidacion_asociado["datos_archivo"][n].get("filtro_adicional"))
        if filtro_adicional!="None":
            #print glentidad_id
            filtro_adicional=filtro_adicional.replace("@identidad@",str(glentidad_id))
            #print filtro_adicional
            consulta=consulta+" "+filtro_adicional
        #print consulta
        dts=conexion_base(consulta)
        if columna.get("entero")==1:
            arr2a=dts[0][columna["tabla_texto"]].astype('unicode').str.replace(".","",1).str.isdigit()
            dts[0].loc[arr2a,columna["tabla_texto"]+"_int"]=dts[0].loc[arr2a,columna["tabla_texto"]].astype(float)
            dts[0][columna["tabla_texto"]+"_int"].fillna(0,inplace=True)
            dts[0][columna["tabla_texto"]+"_int"]=dts[0][columna["tabla_texto"]+"_int"].astype(int)
            dts[0][columna["tabla_texto"]]=dts[0][columna["tabla_texto"]+"_int"]        

        gldfcompara[gldfcompara.columns[numero]+"_min"]=gldfcompara[gldfcompara.columns[numero]].apply(lambda x: elimina_tildes(x).lower().strip().replace(".0","").replace(",",""))

        
        dts[0][columna["tabla_texto"]]=dts[0][columna["tabla_texto"]].astype('unicode')
        dts[0][columna["tabla_texto"]]=dts[0][columna["tabla_texto"]].apply(unidecode)
        #dts[0][columna["tabla_texto"]].apply(lambda x: elimina_tildes(x).lower())
        dts[0][columna["tabla_texto"]+"_min"]=dts[0][columna["tabla_texto"]].apply(lambda x: elimina_tildes(x).lower().strip().replace(".0","").replace(",",""))
        #dts[0].loc[dts[0][dts[0][columna["tabla_texto"]+"_min"]]=='otros',[columna["tabla_texto"]]]
        cadena='|'.join(dts[0][columna["tabla_texto"]+"_min"])
        valor_otros=valor_defecto
        #if permite_valor_defecto==1:
            #dfotros=dts[0].loc[dts[0][columna["tabla_texto"]+"_min"]=='otros',columna["tabla_texto"]+"_min"]
            #print dfotros.index[0]
            #print columna["tabla_texto"]+"_min"
            #print dfotros.loc[dfotros.index[0],columna["tabla_texto"]+"_min"]
            #if len(dfotros)>0:valor_otros=dfotros.loc[dfotros.index[0],columna["tabla_texto"]+"_min"]
            
        #dts[0]=dts[0].set_index(columna["tabla_texto"]+"_min")       
        #arr1=gldfcompara[gldfcompara.columns[numero]+"_min"].str.match('^'+cadena+'$')
        #print(dts[0].index)
        #print(cadena)
        #arr2=arr1.index
        #print(gldfcompara[gldfcompara.columns[numero]+"_min"].head())
        #print(dts[0][columna["tabla_texto"]+"_min"].head())
        #gldfcompara.loc[gldfcompara[gldfcompara.columns[0]]=='cesar','columna_'+str(numero+1)] = gldfcompara[gldfcompara.columns[numero]+"_min"].apply(lambda x: dts[0].loc[x.strip()][columna["tabla_llave"]])
        df2b_left= pd.merge(gldfcompara, dts[0], how='left',left_on=gldfcompara.columns[numero]+"_min", right_on=columna["tabla_texto"]+"_min")
        gldfcompara.loc[df2b_left[columna["tabla_texto"]+"_min"].isnull()==False,campo_destino]=df2b_left[columna["tabla_llave"]]
           
        
        arr1=df2b_left[columna["tabla_texto"]+"_min"].isnull()==False
        arr2=arr1.index

        if permite_valor_defecto==1:
            gldfcompara.loc[arr1==False,campo_destino] = valor_otros
            arr1[:]=True
        glgeneral[campo_destino]=gldfcompara[campo_destino]
        #print(gldfcompara.head())
        #if indice==10:
            #print dts[0]
            #print df2b_left[gldfcompara.columns[numero]+"_min"]
            #print df2b_left.iloc[0]
            #print columna["tabla_texto"]+"_min"
            #print campo_destino
            #print gldfcompara.iloc[gldfcompara.columns.get_loc(gldfcompara.columns[numero]+"_min")]
            #print gldfcompara.columns
            #print gldfcompara.columns.get_loc()
        
    if tipo==2: 
        arr1=pd.Series(range(len(gldfcompara)))
        arr1.iloc[:]=True
        gldfcompara[campo_destino]=gldfcompara[gldfcompara.columns[numero]]
        glgeneral[campo_destino]=gldfcompara[campo_destino]
    if tipo==4: 
        arr1=pd.Series(range(len(gldfcompara)))
        arr1.iloc[:]=True      
    if tipo==3:
        valor_defecto_texto=columna["valor_defecto_texto"]
        arrvalor_defecto_texto=str(valor_defecto_texto).split(',')
        arrvalor_defecto=str(valor_defecto).split(',')
        gldfcompara[gldfcompara.columns[numero]+"_min"]=gldfcompara[gldfcompara.columns[numero]].apply(lambda x: elimina_tildes(x).lower())
        arr4=[]
        i=0
        while i<len(arrvalor_defecto_texto):
            arr4.append({'texto':arrvalor_defecto_texto[i],'valor_tmp':arrvalor_defecto[i]})
            i=i+1
        arr4df=pd.DataFrame(arr4)
        df2b_left= pd.merge(gldfcompara, arr4df, how='left',left_on=gldfcompara.columns[numero]+"_min", right_on="texto")
        gldfcompara.loc[df2b_left[gldfcompara.columns[numero]+"_min"].isnull()==False,campo_destino]=df2b_left['valor_tmp']
        arr1=pd.Series(range(len(gldfcompara)))
        arr1.iloc[:]=True
        glgeneral[campo_destino]=gldfcompara[campo_destino]
    
    rechazar_registro=columna["rechazar_registro"]
    if rechazar_registro==1:
        glregistos_rechazados.loc[arr1==False]=False
        
    agrega_tabla_validacion(indice,columna,arr1,"mensaje_no_encuentra")
        #print glgeneral_calidad
    glhomologa.append(arr1)

def agrega_tabla_validacion(indice,columna,arr1,campo_mensaje):
    global glgeneral_calidad
    numero=columna["numero_columna_excel"]-1
    reportar_campo=columna["reportar_campo"]
    rechazar_registro=columna["rechazar_registro"]    
    if reportar_campo==1:
        mensaje_no_encuentra=columna.get(campo_mensaje)
        msj="ERROR CALIDAD"
        if rechazar_registro==1:
            msj="RECHAZADO"
        dfvalor=pd.DataFrame([])
        if columna.get("entero")==1:
            dfvalor["valor"]=gldfcompara.loc[arr1==False,gldfcompara.columns[numero]+"_bk"]
        else:
            dfvalor["valor"]=gldfcompara.loc[arr1==False,gldfcompara.columns[numero]]
        
        indice_excel=glvalidacion_asociado["numero_columna_llave_excel"]-1
        columna_llave=glvalidacion_asociado["datos_archivo"][indice_excel]
        dfvalor["llave"]=gldfcompara.loc[arr1==False,gldfcompara.columns[indice_excel]]
        dfvalor["entidad"]=glentidad
        dfvalor["tabla"]=gl_archivo_cargado        
        dfvalor["campo"]=columna["campo_excel"]
        dfvalor["motivo"]=mensaje_no_encuentra
        dfvalor["mensaje"]=msj
        glgeneral_calidad=pd.concat([glgeneral_calidad,dfvalor])    

def inserta_tabla_validacion(dato_llave,campo,dato,numero_columna,campo_mensaje,rechazar_registro):
    
    if rechazar_registro==1:
        mjs_fin="RECHAZADO"
    else:
        mjs_fin="ERROR CALIDAD"
         
    global glarr_datos_validacion
    mensaje=glvalidacion_asociado["datos_archivo"][numero_columna][campo_mensaje]
    df3=pd.DataFrame([{'NOMBRE DE LA ENTIDAD':glentidad,
                               'ARCHIVO/TABLA':glarchivo,
                               'IDENTIFICACIÓN DEL REGISTRO':dato_llave,
                               'CAMPO CON OBSERVACIÓN':campo,
                               'VALOR DEL CAMPO CON OBSERVACIÓN':dato,
                               'MOTIVO DE RECHAZO':mensaje,
                               'ESTADO DEL REGISTRO':mjs_fin
                              }])
    glarr_datos_validacion=glarr_datos_validacion.append(df3)

def fun_valida_vacio(indice):
    columna=glvalidacion_asociado["datos_archivo"][indice]
    numero=columna["numero_columna_excel"]-1
    valida_vacio=columna["valida_vacio"]
    rechazar_registro=columna["rechazar_registro"]
    if valida_vacio==1:
        arr2=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.match('^ {1,}$')
        arr2=arr2==False
        if rechazar_registro==1:
            glregistos_rechazados.loc[arr2==False]=False
    else:
        arr2=pd.Series(range(len(gldfcompara)))
        arr2.iloc[:]=True
    agrega_tabla_validacion(indice,columna,arr2,"mensaje_vacio")
    glfun_valida_vacio.append(arr2)
    #print(arr2)



def fun_valida_nulo(indice):
    columna=glvalidacion_asociado["datos_archivo"][indice]
    numero=columna["numero_columna_excel"]-1
    valida_nulos=columna["valida_nulos"]
    #print valida_nulos
    if valida_nulos==1:
        #print("qw")
        arr2=gldfcompara[gldfcompara.columns[numero]].isnull()
        arr2=arr2==False
        rechazar_registro=columna["rechazar_registro"]
        if rechazar_registro==1:
            glregistos_rechazados.loc[arr2==False]=False        
    else:
        arr2=pd.Series(range(len(gldfcompara)))
        arr2.iloc[:]=True
    agrega_tabla_validacion(indice,columna,arr2,"mensaje_nulo")
    glfun_valida_nulo.append(arr2)
    #print(arr2)

def fun_valida_caracteres_especiales(indice):
    columna=glvalidacion_asociado["datos_archivo"][indice]
    numero=columna["numero_columna_excel"]-1
    valida_caracteres_especiales=columna["valida_caracteres_especiales"]
    if valida_caracteres_especiales==1:
        #print("qw")
        #print(gldfcompara.columns[numero])
        arr2=gldfcompara[gldfcompara.columns[numero]].apply(lambda x: elimina_tildes(x)).str.match('^([ ,.,a-z,0-9,A-Z,Ñ,ñ]{0,})$')
        #arr4=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.match('^([Ñ,ñ]{0,})$')
        rechazar_registro=columna["rechazar_registro"]
        if rechazar_registro==1:
            glregistos_rechazados.loc[arr2==False]=False          
        #arr2=arr2==False
    else:
        arr2=pd.Series(range(len(gldfcompara)))
        arr2.iloc[:]=True
    agrega_tabla_validacion(indice,columna,arr2,"mensaje_caracteres_especiales")
    glfun_valida_caracteres_especiales.append(arr2)
    #if indice==7:
        #print gldfcompara.loc[arr2==False,gldfcompara.columns[numero]].apply(lambda x: elimina_tildes(x))
        #print arr2

def fun_valida_tres_caracteres(indice):
    columna=glvalidacion_asociado["datos_archivo"][indice]
    numero=columna["numero_columna_excel"]-1
    valida_tres_caracteres_iguales=columna["valida_tres_caracteres_iguales"]
    if valida_tres_caracteres_iguales==1:
        #print("qw")
        #print(gldfcompara.columns[numero])
        #arr1=df2[df2.columns[0]].str.lower().str.contains('[a]{3,}|[b]{3,}|[c]{3,}|[d]{3,}|[e]{3,}|[f]{3,}|[g]{3,}|[h]{3,}|[i]{3,}|[j]{3,}|[k]{3,}|[l]{3,}|[m]{3,}|[n]{3,}|[ñ]{3,}|[o]{3,}|[p]{3,}|[q]{3,}|[r]{3,}|[s]{3,}|[t]{3,}|[u]{3,}|[v]{3,}|[w]{3,}|[x]{3,}|[y]{3,}|[z]{3,}')
        arr2=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.lower().str.match('[a]{3,}|[b]{3,}|[c]{3,}|[d]{3,}|[e]{3,}|[f]{3,}|[g]{3,}|[h]{3,}|[i]{3,}|[j]{3,}|[k]{3,}|[l]{3,}|[m]{3,}|[n]{3,}|[ñ]{3,}|[o]{3,}|[p]{3,}|[q]{3,}|[r]{3,}|[s]{3,}|[t]{3,}|[u]{3,}|[v]{3,}|[w]{3,}|[x]{3,}|[y]{3,}|[z]{3,}')
        arr2=arr2==False
        rechazar_registro=columna["rechazar_registro"]
        if rechazar_registro==1:
            glregistos_rechazados.loc[arr2==False]=False          
    else:
        arr2=pd.Series(range(len(gldfcompara)))
        arr2.iloc[:]=True
    #print(len(arr2))
    glfun_valida_tres_caracteres.append(arr2)

    columna=glvalidacion_asociado["datos_archivo"][indice]
    numero=columna["numero_columna_excel"]-1
    valida_caracteres_especiales=columna["valida_caracteres_especiales"]
    if valida_caracteres_especiales==1:
        #print("qw")
        #print(gldfcompara.columns[numero])
        arr2=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.match('^([a-z,0-9,A-Z]{0,})$')
        #arr2=arr2==False
    else:
        arr2=pd.Series(range(len(gldfcompara)))
        arr2.iloc[:]=True
    
    agrega_tabla_validacion(indice,columna,arr2,"mensaje_tres_caracteres_iguales")
    glfun_valida_caracteres_especiales.append(arr2)

def fun_valida_fecha(indice):
    #global gldfcompara
    columna=glvalidacion_asociado["datos_archivo"][indice]
    numero=columna["numero_columna_excel"]-1

    es_fecha=columna["es_fecha"]
    if es_fecha==1:
        campo_destino=columna["campo_destino"]
        arr3=gldfcompara[gldfcompara.columns[numero]].isnull()
        gldfcompara[gldfcompara.columns[numero]]=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.replace(' 00:00:00','').str.replace('NaT','')
        #print gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.replace(' 00:00:00','').str.lower()
        arr2=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.match('^(((([1-2]{1})([0-9]{1}))|(([0]{1})([1-9]{1}))|(([3]{1})([0-1]{1})))/((([0]{1})([1-9]{1}))|(([1]{1})([0-2]{1})))/([0-9]{4}))$')
        arr4=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.match('^(([0-9]{4})-((([0]{1})([1-9]{1}))|(([1]{1})([0-2]{1})))-((([0]{1})([1-9]{1}))|(([1-2]{1})([0-9]{1}))|(([3]{1})([0-1]{1}))))$')
        #print arr2

    
        #gldfcompara.loc[arr2==True,gldfcompara.columns[numero]]=pd.to_datetime(gldfcompara[gldfcompara.columns[numero]], errors='coerce', format='%d/%m/%Y')
        gldfcompara.loc[arr2==True,gldfcompara.columns[numero]]=gldfcompara.loc[arr2==True,gldfcompara.columns[numero]].apply(lambda x: str(datetime.datetime.strptime(str(x), '%d/%m/%Y').date()))
        
        glgeneral.loc[arr2==True,campo_destino]=gldfcompara.loc[arr2==True,gldfcompara.columns[numero]]
        
        #glgeneral[campo_destino]=gldfcompara[gldfcompara.columns[numero]]
        #gldfcompara.loc[arr4==True,gldfcompara.columns[numero]]=gldfcompara.loc[arr2==True,gldfcompara.columns[numero]].apply(lambda x: datetime.datetime.strptime(str(x), '%Y/%m/%d'))
        #print numero
        #print gldfcompara.iloc[0,12]
        #print gldfcompara.iloc[1,12]
        #print gldfcompara.iloc[2,12]
        #print gldfcompara.iloc[:,12]
              
        
        arr2[arr4==True]=True
        #print str(glgeneral.iloc[0,3])
        #glgeneral.iloc[[0],[3]]=glgeneral.iloc[[0],[3]].astype(str)
        #print glgeneral.loc[:,campo_destino]
        #print arr2
        glgeneral.loc[arr2==True,campo_destino]=glgeneral.loc[arr2==True,campo_destino].astype(str)
        glgeneral.loc[arr2==False,campo_destino]=None
        arr2[arr3==True]=True
        #glgeneral.loc[glgeneral[campo_destino],campo_destino]=None
        #if indice==3:
            #print arr4
            #print gldfcompara[gldfcompara.columns[numero]].to_json()
        rechazar_registro=columna["rechazar_registro"]
        if rechazar_registro==1:
            glregistos_rechazados.loc[arr2==False]=False          
        #print arr2  
        #arr2=arr2==False
    else:
        arr2=pd.Series(range(len(gldfcompara)))
        arr2.iloc[:]=True
    #print(len(arr2))
    
    agrega_tabla_validacion(indice,columna,arr2,"mensaje_fecha")
    glfun_valida_fecha.append(arr2)

def fun_valida_correo(indice):
    columna=glvalidacion_asociado["datos_archivo"][indice]
    numero=columna["numero_columna_excel"]-1

    es_correo=columna["es_correo"]
    if es_correo==1:
        arr3=gldfcompara[gldfcompara.columns[numero]].isnull()
        #gldfcompara[gldfcompara.columns[numero]]=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.replace(' 00:00:00','').str.replace('NaT','')
        #print gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.replace(' 00:00:00','').str.lower()
        arr2=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$')
        arr2[arr3==True]=True
        rechazar_registro=columna["rechazar_registro"]
        if rechazar_registro==1:
            glregistos_rechazados.loc[arr2==False]=False          
        #arr2=arr2==False
    else:
        arr2=pd.Series(range(len(gldfcompara)))
        arr2.iloc[:]=True
    #print(len(arr2))
    agrega_tabla_validacion(indice,columna,arr2,"mensaje_correo")
    glfun_valida_correo.append(arr2)    

def fun_valida_numerico(indice):
    
    columna=glvalidacion_asociado["datos_archivo"][indice]
    numero=columna["numero_columna_excel"]-1

    es_numerico=columna["es_numerico"]
    if es_numerico==1:
        campo_destino=columna["campo_destino"]
        arr3=gldfcompara[gldfcompara.columns[numero]].isnull()
        #gldfcompara[gldfcompara.columns[numero]]=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.replace(' 00:00:00','').str.replace('NaT','')
        #print gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.replace(' 00:00:00','').str.lower()
        arr2=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.replace(".","",1).str.isdigit()
        
        arr2[arr3==True]=True
        gldfcompara[gldfcompara.columns[numero]].fillna(0,inplace=True)
        glgeneral[campo_destino]=gldfcompara[gldfcompara.columns[numero]]
        rechazar_registro=columna["rechazar_registro"]
        if rechazar_registro==1:
            glregistos_rechazados.loc[arr2==False]=False          
        #if indice==8:
            #print arr2
            #print gldfcompara.iloc[0,8]
            #print gldfcompara.iloc[5,8]
            #print gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.isdigit()
        #arr2=arr2==False
    else:
        arr2=pd.Series(range(len(gldfcompara)))
        arr2.iloc[:]=True
    #print(len(arr2))
    agrega_tabla_validacion(indice,columna,arr2,"mensaje_numerico")
    glfun_valida_numerico.append(arr2) 
    #if indice==4:
        #print arr2
        #print gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.replace('.0','').str.isdigit()
def fun_valida_calculo(indice):
    columna=glvalidacion_asociado["datos_archivo"][indice]
    numero=columna["numero_columna_excel"]-1

    verifica_calculo=columna["verifica_calculo"]
    calculo_verificado=columna["calculo_verificado"].split('+')
    #print(es_fecha)
    if verifica_calculo==1:
        arr3=gldfcompara[gldfcompara.columns[numero]].isnull()
        #print gldfcompara[gldfcompara.columns[int(calculo_verificado[0])-1]].astype(float)+gldfcompara[gldfcompara.columns[int(calculo_verificado[1])-1]].astype(float)
        gldfcompara[gldfcompara.columns[numero]]==gldfcompara[gldfcompara.columns[int(calculo_verificado[0])-1]].astype(float)+gldfcompara[gldfcompara.columns[int(calculo_verificado[1])-1]].astype(float)
        #print gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.replace(' 00:00:00','').str.lower()
        arr2=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.match('^(([0-9]{4})-((([0]{1})([1-9]{1}))|(([1]{1})([0-2]{1})))-((([0]{1})([1-9]{1}))|(([1-2]{1})([0-9]{1}))|(([3]{1})([0-1]{1}))))|(((([1-2]{1})([0-9]{1}))|(([0]{1})([1-9]{1}))|(([3]{1})([0-1]{1})))/((([0]{1})([1-9]{1}))|(([1]{1})([0-2]{1})))/([0-9]{4}))$')
        arr2[arr3==True]=True
        rechazar_registro=columna["rechazar_registro"]
        if rechazar_registro==1:
            glregistos_rechazados.loc[arr2==False]=False          
    else:
        arr2=pd.Series(range(len(gldfcompara)))
        arr2.iloc[:]=True
    agrega_tabla_validacion(indice,columna,arr2,"mensaje_calculo")
    glfun_valida_calculo.append(arr2) 

def fun_valida_unico(indice):
    columna=glvalidacion_asociado["datos_archivo"][indice]
    #print columna
    numero=columna["numero_columna_excel"]-1
    es_unico=columna["es_unico"]
    #print(es_unico)
    if es_unico==1:
        arr3=gldfcompara[gldfcompara.columns[numero]].isnull()
        gldfcompara["cantidad"]=1
        df3=gldfcompara.groupby([gldfcompara.columns[numero]], axis=0).sum()
        df3.reset_index(inplace=True)
        df4=gldfcompara.merge(df3, left_on=gldfcompara.columns[numero], right_on=gldfcompara.columns[numero], how='left')
        arr2=df4["cantidad_y"]==1
        arr2[arr3==True]=True
        rechazar_registro=columna["rechazar_registro"]
        if rechazar_registro==1:
            glregistos_rechazados.loc[arr2==False]=False          
        #arr2=arr2==False
    else:
        arr2=pd.Series(range(len(gldfcompara)))
        arr2.iloc[:]=True
    
    agrega_tabla_validacion(indice,columna,arr2,"mensaje_unico")
    glfun_valida_unico.append(arr2)





def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
    return s.decode()

#Inicio Programa

glgeneral_calidad=pd.DataFrame([])
glhomologa=[]
glfun_valida_vacio=[]
glfun_valida_nulo=[]
glfun_valida_caracteres_especiales=[]
glfun_valida_unico=[]
glfun_valida_tres_caracteres=[]
glfun_valida_fecha=[]
glfun_valida_correo=[]
glfun_valida_numerico=[]
glfun_valida_calculo=[]
gl_archivo_cargado=""
glentidad='ENTIDAD_DEMO'
glentidad_id=form.getvalue("entidad")
#glentidad_id=8
obj1=conexion_base("select ENTID_NombreEntidad from KP_ENTIDAD where ENTID_idInterno="+str(glentidad_id))
glentidad=obj1[0].iloc[0,0]
glarr_datos_validacion=pd.DataFrame([])

#gl_archivos=["asociados","canales","productos","jurisdicciones","asociadosxproductos","transacciones"]
#gl_archivos=["asociados","canales","productos","jurisdicciones","asociadosxproductos"]
#gl_archivos=["asociados"]
cont_arc=0
while cont_arc<len(gl_archivos):
    glgeneral=pd.DataFrame([])
    cadena_sql_ins_total=""
    cadena_sql_act_total=""
    glhomologa=[]
    glfun_valida_vacio=[]
    glfun_valida_nulo=[]
    glfun_valida_caracteres_especiales=[]
    glfun_valida_unico=[]
    glfun_valida_tres_caracteres=[]
    glfun_valida_fecha=[]
    glfun_valida_correo=[]
    glfun_valida_numerico=[]
    glfun_valida_calculo=[]
    
    
    tipo2=gl_archivos[cont_arc]
    gl_archivo_cargado=tipo2
    print tipo2
    #tipo2="asociados"
    df = pd.read_excel("C:\\archivos_lectura\\"+glarchivos_config[tipo2]["archivo"])
    #print df.iloc[1]
    #print df.iloc[1]
    df = df.rename(columns=lambda n: n.replace('\n', ''.replace('\r', '')))
    gldfcompara=df.copy()
    glregistos_rechazados=pd.Series(range(len(gldfcompara)))
    glregistos_rechazados.iloc[:]=True    
    

    #print glarchivos_config[tipo]["archivo"]
    json_asociado=open("C:\\consofi\\"+glarchivos_config[tipo2]["config"]).read()
    glvalidacion_asociado=ast.literal_eval(json_asociado)
    glanchocolumnas_valida=glvalidacion_asociado["ancho_columnas_valida"]
    arr_datos_inserta=[]
    
    n=0
    while n<len(glvalidacion_asociado["datos_archivo"]):
        columna=glvalidacion_asociado["datos_archivo"][n]
        campo=columna["campo_excel"]
        numero=columna["numero_columna_excel"]-1
        inserta_no_existe=columna["inserta_no_existe"]
        #print inserta_no_existe
        if inserta_no_existe==1:
            consulta="select "+columna["tabla_llave"]+","+columna["tabla_texto"]+" from "+columna["tabla_homologa"]
            dts=conexion_base(consulta)
            gldfcompara[gldfcompara.columns[numero]+"_min"]=gldfcompara[gldfcompara.columns[numero]].apply(lambda x: elimina_tildes(x).lower())
            dts[0][columna["tabla_texto"]]=dts[0][columna["tabla_texto"]].astype('unicode')
            dts[0][columna["tabla_texto"]]=dts[0][columna["tabla_texto"]].apply(unidecode)
            dts[0][columna["tabla_texto"]].apply(lambda x: elimina_tildes(x).lower())
            dts[0][columna["tabla_texto"]+"_min"]=dts[0][columna["tabla_texto"]].apply(lambda x: elimina_tildes(x).lower())
            #dts[0].loc[dts[0][dts[0][columna["tabla_texto"]+"_min"]]=='otros',[columna["tabla_texto"]]]
            cadena='|'.join(dts[0][columna["tabla_texto"]+"_min"])
            arr1=gldfcompara[gldfcompara.columns[numero]+"_min"].str.match('^'+cadena+'$')
            #print dts[0]
            #print gldfcompara[gldfcompara.columns[numero]+"_min"]
            ser=pd.value_counts(gldfcompara.loc[arr1==False,gldfcompara.columns[numero]])
            ind=0
            while ind<len(ser.index):
                arr_datos_inserta.append({'tabla':columna["tabla_homologa"],
                                      'llave':columna["tabla_llave"],
                                      'texto':columna["tabla_texto"],
                                      'valor':ser.index[ind]
                                     })
                ind=ind+1
            
        n=n+1
        
    n=0
    while n<len(arr_datos_inserta):
        consulta="INSERT INTO "+arr_datos_inserta[n]["tabla"] + "("+arr_datos_inserta[n]["texto"]+") values ('"+str(arr_datos_inserta[n]["valor"])+"') select 1 as salida"
        conexion_base_insert(consulta)
        #print(consulta)
        n=n+1
        
    n=0
    cadena_ent=""
    cadena_ent2=""
    cadena_filtro=""
    if glvalidacion_asociado["inserta_llave_externa"]==1:
        cadena_ent= glvalidacion_asociado["campo_llave_externa"]+","
        cadena_ent2=  str(glentidad_id)+","
        cadena_filtro=""+glvalidacion_asociado["campo_llave_externa"] + "="+str(glentidad_id)
        
    cadena_in=" INSERT INTO "+glvalidacion_asociado["tabla"]+ "("+cadena_ent 
    cadena_ac=" "
    cadena_js=""
    while n<len(glvalidacion_asociado["datos_archivo"]):
        #print(n)
        if n==11:
            c=1
        if glvalidacion_asociado["datos_archivo"][n]["tipo"]!=4:
            homolga(n)
            fun_valida_vacio(n)
            fun_valida_nulo(n)
            fun_valida_caracteres_especiales(n)
            fun_valida_unico(n)
            #fun_valida_tres_caracteres(n)
            fun_valida_fecha(n)
            fun_valida_correo(n)
            fun_valida_numerico(n)
            fun_valida_calculo(n)
            columna_nom=glvalidacion_asociado["datos_archivo"][n]["campo_destino"]
            cadena_in=cadena_in +columna_nom + ","
            cadena_ac=cadena_ac+" b."+columna_nom+"=a."+columna_nom+","
            tipo_dato=""
            if glvalidacion_asociado["datos_archivo"][n].get("entero")==1:
                tipo_dato="decimal(10,0)"
            elif  glvalidacion_asociado["datos_archivo"][n]["es_fecha"]==1:
                tipo_dato="varchar(1000)"
            else:
                tipo_dato="varchar(1000)"
             
            cadena_js=cadena_js+" "+columna_nom+"   "+tipo_dato+" '$."+columna_nom+"',"
        n=n+1
        
    
    glarr_datos_destino=pd.DataFrame([])
    numero_columna_llave=int(glvalidacion_asociado["numero_columna_llave_excel"])-1
    glarchivo=glvalidacion_asociado["nombre"]
    #print int(gldfcompara.iloc[1,1])
    #print gldfcompara.iloc[1,gldfcompara.columns.get_loc("CLIEN_NumeroIdentificacion")]
    #print(gldfcompara.to_html())
    arr_destino=[]
    arr_destino_act=[]
    arr_destino_sql=[]
    #196
    fila=0;
    tabla_destino=glvalidacion_asociado["tabla"]
    llave_tabla=glvalidacion_asociado["llave_tabla"]
    cadena_sql_act_total=""
    cadena_sql_ins_total=""
    inserta_llave_externa=glvalidacion_asociado["inserta_llave_externa"]
    campo_llave_externa=glvalidacion_asociado["campo_llave_externa"]
    

    #caden=glgeneral.iloc[[0],:].to_json(orient='records')
    #print glregistos_rechazados 
    caden=glgeneral.loc[glregistos_rechazados,:].to_json(orient='records')
    caden=caden.replace("'","''")
    #print caden 
    #print glgeneral.columns
    
    cadena_js= cadena_js[0:len(cadena_js)-1]
    cadena_in=cadena_in[0:len(cadena_in)-1]
    cadena_ac=cadena_ac[0:len(cadena_ac)-1]
    cadena_in=cadena_in+") "
    
    cadena_ins_llave="""  left join {tabla_destino} b on a.{llave_tabla}=b.{llave_tabla} and b.{cadena_filtro}
     where b.{llave_tabla} is null 
     """.format(caden=caden,cadena_in=cadena_in,cadena_ent2=cadena_ent2,
               cadena_js=cadena_js,tabla_destino=tabla_destino,
               llave_tabla=llave_tabla,cadena_ac=cadena_ac,
               cadena_filtro=cadena_filtro
               )
    if llave_tabla=="":
        cadena_ins_llave=""
    
    cadena_sql_ins="""DECLARE @json NVARCHAR(MAX) SET @json = N'{caden}'
    {cadena_in}
    SELECT {cadena_ent2}a.* FROM 
     OPENJSON ( @json ) 
    WITH (  
                  {cadena_js}
    
     ) a
     {cadena_ins_llave}
    
     
    """.format(caden=caden,cadena_in=cadena_in,cadena_ent2=cadena_ent2,
               cadena_js=cadena_js,tabla_destino=tabla_destino,
               llave_tabla=llave_tabla,cadena_ac=cadena_ac,
               cadena_filtro=cadena_filtro,cadena_ins_llave=cadena_ins_llave
               )
    
    cadena_act=""" DECLARE @json NVARCHAR(MAX) SET @json = N'{caden}'
        
     update b set {cadena_ac} from
     OPENJSON ( @json ) 
    WITH (  
                  {cadena_js}
    
     ) a   
     inner join {tabla_destino} b on b.{llave_tabla}=a.{llave_tabla}     
     where b.{cadena_filtro}
     
    """.format(caden=caden,cadena_in=cadena_in,cadena_ent2=cadena_ent2,
               cadena_js=cadena_js,tabla_destino=tabla_destino,
               llave_tabla=llave_tabla,cadena_ac=cadena_ac,
               cadena_filtro=cadena_filtro
               )
    

    
    #print cadena_sql_ins
    #print cadena_act
    
    
    if glvalidacion_asociado["inserta"]==1:
        conexion_base_insert(cadena_sql_ins)
    if glvalidacion_asociado["actualiza"]==1:
        conexion_base_insert(cadena_act)

    cont_arc=cont_arc+1 
    
glgeneral_calidad=glgeneral_calidad.sort_values(['tabla','campo'], ascending=[1,1])
lista=["entidad","tabla","llave","campo","valor","motivo","mensaje"]
glgeneral_calidad = glgeneral_calidad[lista]
    
    #glgeneral_calidad = glgeneral_calidad[['NOMBRE DE LA ENTIDAD', 'ARCHIVO/TABLA', 'IDENTIFICACIÓN DEL REGISTRO'
     #                              , 'CAMPO CON OBSERVACIÓN', 'VALOR DEL CAMPO CON OBSERVACIÓN'
     #                               , 'MOTIVO DE RECHAZO','ESTADO DEL REGISTRO'
      #                             ]]
    
    #gglgeneral_calidad.columns[0]="NOMBRE DE LA ENTIDAD"
    #gglgeneral_calidad.columns[1]="ARCHIVO/TABLA"
    #gglgeneral_calidad.columns[2]="IDENTIFICACIÓN DEL REGISTRO"
    #gglgeneral_calidad.columns[3]="CAMPO CON OBSERVACIÓN"
    #gglgeneral_calidad.columns[4]="VALOR DEL CAMPO CON OBSERVACIÓN"
    #gglgeneral_calidad.columns[5]="MOTIVO DE RECHAZO"
    #gglgeneral_calidad.columns[6]="ESTADO DEL REGISTRO" 
glgeneral_calidad.rename(columns={'mensaje':'ESTADO DEL REGISTRO','motivo':'MOTIVO DE RECHAZO','campo':'CAMPO CON OBSERVACIÓN','valor':'VALOR DEL CAMPO CON OBSERVACIÓN','entidad':'NOMBRE DE LA ENTIDAD','tabla':'ARCHIVO/TABLA','llave':'IDENTIFICACIÓN DEL REGISTRO'}, inplace=True)
    
escribir_excel(glgeneral_calidad,'C:\\archivos_salida\\ReporteCalidad.xlsx','xlsxwriter',glanchocolumnas_valida.split(','))    
    

    
    #print glgeneral_calidad
