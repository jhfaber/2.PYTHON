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
reload(sys)
sys.setdefaultencoding("utf-8")



form = cgi.FieldStorage()
tipo2 = form.getvalue("tipo")
#tipo2="transacciones"



glarchivos_config={"asociados":
                   {
                       "archivo":"asociados2.xls",
                       "config":"asociados.json"
                   },
                   "canales":
                   {
                       "archivo":"canales.xls",
                       "config":"canales.json"
                   },
                   "productos":
                   {
                       "archivo":"productos.xls",
                       "config":"productos.json"
                   },
                   "asociadosxproductos":
                   {
                       "archivo":"asociadosxproductos.xlsx",
                       "config":"asociadosxproductos.json"
                   },
                   "transacciones":
                   {
                       "archivo":"transacciones.xlsx",
                       "config":"transacciones.json"
                   }}



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
    if tipo==1:        
        consulta="select "+columna["tabla_llave"]+","+columna["tabla_texto"]+" from "+columna["tabla_homologa"]
        dts=conexion_base(consulta)
    
        
        gldfcompara[gldfcompara.columns[numero]+"_min"]=gldfcompara[gldfcompara.columns[numero]].apply(lambda x: elimina_tildes(x).lower().strip().replace(".0","").replace(",",""))
        #print(dts)
        
        dts[0][columna["tabla_texto"]]=dts[0][columna["tabla_texto"]].astype('unicode')
        dts[0][columna["tabla_texto"]]=dts[0][columna["tabla_texto"]].apply(unidecode)
        dts[0][columna["tabla_texto"]].apply(lambda x: elimina_tildes(x).lower())
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
    glhomologa.append(arr1)
    
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
    if valida_vacio==1:
        arr2=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.match('^ {1,}$')
        arr2=arr2==False
    else:
        arr2=pd.Series(range(len(gldfcompara)))
        arr2.iloc[:]=True
    
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
    else:
        arr2=pd.Series(range(len(gldfcompara)))
        arr2.iloc[:]=True
    glfun_valida_nulo.append(arr2)
    #print(arr2)

def fun_valida_caracteres_especiales(indice):
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
    
    glfun_valida_caracteres_especiales.append(arr2)

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
    
    glfun_valida_caracteres_especiales.append(arr2)

def fun_valida_fecha(indice):
    #global gldfcompara
    columna=glvalidacion_asociado["datos_archivo"][indice]
    numero=columna["numero_columna_excel"]-1

    es_fecha=columna["es_fecha"]
    if es_fecha==1:
        arr3=gldfcompara[gldfcompara.columns[numero]].isnull()
        gldfcompara[gldfcompara.columns[numero]]=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.replace(' 00:00:00','').str.replace('NaT','')
        #print gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.replace(' 00:00:00','').str.lower()
        arr2=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.match('^(((([1-2]{1})([0-9]{1}))|(([0]{1})([1-9]{1}))|(([3]{1})([0-1]{1})))/((([0]{1})([1-9]{1}))|(([1]{1})([0-2]{1})))/([0-9]{4}))$')
        arr4=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.match('^(([0-9]{4})-((([0]{1})([1-9]{1}))|(([1]{1})([0-2]{1})))-((([0]{1})([1-9]{1}))|(([1-2]{1})([0-9]{1}))|(([3]{1})([0-1]{1}))))$')
        #print arr2
        #if indice==3:
            #print arr2
    
        #gldfcompara.loc[arr2==True,gldfcompara.columns[numero]]=pd.to_datetime(gldfcompara[gldfcompara.columns[numero]], errors='coerce', format='%d/%m/%Y')
        gldfcompara.loc[arr2==True,gldfcompara.columns[numero]]=gldfcompara.loc[arr2==True,gldfcompara.columns[numero]].apply(lambda x: str(datetime.datetime.strptime(str(x), '%d/%m/%Y').date()))
        #gldfcompara.loc[arr4==True,gldfcompara.columns[numero]]=gldfcompara.loc[arr2==True,gldfcompara.columns[numero]].apply(lambda x: datetime.datetime.strptime(str(x), '%Y/%m/%d'))
        #print numero
        #print gldfcompara.iloc[0,12]
        #print gldfcompara.iloc[1,12]
        #print gldfcompara.iloc[2,12]
        #print gldfcompara.iloc[:,12]
              
        arr2[arr3==True]=True
        arr2[arr4==True]=True
        #print arr2  
        #arr2=arr2==False
    else:
        arr2=pd.Series(range(len(gldfcompara)))
        arr2.iloc[:]=True
    #print(len(arr2))
    
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
        #arr2=arr2==False
    else:
        arr2=pd.Series(range(len(gldfcompara)))
        arr2.iloc[:]=True
    #print(len(arr2))
    glfun_valida_correo.append(arr2)    

def fun_valida_numerico(indice):
    
    columna=glvalidacion_asociado["datos_archivo"][indice]
    numero=columna["numero_columna_excel"]-1

    es_numerico=columna["es_numerico"]
    if es_numerico==1:
        arr3=gldfcompara[gldfcompara.columns[numero]].isnull()
        #gldfcompara[gldfcompara.columns[numero]]=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.replace(' 00:00:00','').str.replace('NaT','')
        #print gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.replace(' 00:00:00','').str.lower()
        arr2=gldfcompara[gldfcompara.columns[numero]].astype('unicode').str.replace(".","",1).str.isdigit()
        if columna.get("entero")==1:
            #gldfcompara.loc[arr2==True,gldfcompara.columns[numero]]=int(float(gldfcompara[gldfcompara.columns[numero]]))
            gldfcompara.loc[arr2,gldfcompara.columns[numero]+"_int"]=df.loc[arr2,gldfcompara.columns[numero]].astype(float)
            gldfcompara[gldfcompara.columns[numero]+"_int"].fillna(0,inplace=True)
            gldfcompara[gldfcompara.columns[numero]+"_int"]=gldfcompara[gldfcompara.columns[numero]+"_int"].astype(int)
            gldfcompara.loc[arr2,gldfcompara.columns[numero]]=gldfcompara.loc[arr2,gldfcompara.columns[numero]+"_int"]
        arr2[arr3==True]=True
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
    else:
        arr2=pd.Series(range(len(gldfcompara)))
        arr2.iloc[:]=True
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
        #arr2=arr2==False
    else:
        arr2=pd.Series(range(len(gldfcompara)))
        arr2.iloc[:]=True
    
    glfun_valida_unico.append(arr2)





def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
    return s.decode()

#Inicio Programa

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

glentidad='ENTIDAD_DEMO'
glentidad_id=form.getvalue("entidad")
glentidad_id=8
obj1=conexion_base("select ENTID_NombreEntidad from KP_ENTIDAD where ENTID_idInterno="+str(glentidad_id))
glentidad=obj1[0].iloc[0,0]
glarr_datos_validacion=pd.DataFrame([])

gl_archivos=["asociados","canales","productos","asociadosxproductos","transacciones"]
gl_archivos=["asociados"]
cont_arc=0
while cont_arc<len(gl_archivos):
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
    print tipo2
    #tipo2="asociados"
    df = pd.read_excel("C:\\archivos_lectura\\"+glarchivos_config[tipo2]["archivo"])
    #print df.iloc[1]
    #print df.iloc[1]
    df = df.rename(columns=lambda n: n.replace('\n', ''.replace('\r', '')))
    gldfcompara=df.copy()
    
    

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
    while n<len(glvalidacion_asociado["datos_archivo"]):
        #print(n)
        if n==11:
            c=1
        homolga(n)
        #if n==11:
            #print gldfcompara.iloc[0]
        
        fun_valida_vacio(n)
        fun_valida_nulo(n)
        fun_valida_caracteres_especiales(n)
        fun_valida_unico(n)
        fun_valida_tres_caracteres(n)
        fun_valida_fecha(n)
        fun_valida_correo(n)
        fun_valida_numerico(n)
        fun_valida_calculo(n)
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
    #print glfun_valida_vacio
    while fila<len(gldfcompara):
    #196
    #while fila<10:
        #print str(fila) + "<br>"
        dato_llave=gldfcompara.iloc[fila,numero_columna_llave]
        if glvalidacion_asociado.get("llave_entero")==1:
            if str(dato_llave).replace(".","",1).isdigit()== True:
                dato_llave=int(float(dato_llave))        
        #if fila==196:
            #print gldfcompara.iloc[fila]
        #print gldfcompara.iloc[fila]
        obj_fila={}
        cadena_sql_act=" update "+tabla_destino +" set "
        if inserta_llave_externa==1:
            cadena_sql_ins=" insert into "+tabla_destino +" ("+campo_llave_externa+","
            cadena_sql_ins2=" select "+str(glentidad_id)+","
        else:
            cadena_sql_ins=" insert into "+tabla_destino +" ("
            cadena_sql_ins2=" select "
            
        permite_registro=True
        n=0
        while n<len(glvalidacion_asociado["datos_archivo"]):
            paso_registro_correcto=True
            reportar_campo=glvalidacion_asociado["datos_archivo"][n]["reportar_campo"]
            rechazar_registro=glvalidacion_asociado["datos_archivo"][n]["rechazar_registro"]
            campo=glvalidacion_asociado["datos_archivo"][n]["campo_excel"]
            campo_destino=glvalidacion_asociado["datos_archivo"][n]["campo_destino"]
            
            tipo=glvalidacion_asociado["datos_archivo"][n]["tipo"]
            numero_columna_excel=glvalidacion_asociado["datos_archivo"][n]["numero_columna_excel"]-1
            #numero_columna_llave_excel=glvalidacion_asociado["datos_archivo"][n]["numero_columna_llave_excel"]-1
            if tipo==2:
                dato=gldfcompara.iloc[fila,numero_columna_excel]
            else:
                dato=gldfcompara.iloc[fila,gldfcompara.columns.get_loc(campo_destino)]
            
            if glvalidacion_asociado["datos_archivo"][n].get("entero")==1:
                if str(dato).replace(".","",1).isdigit()== True:
                    dato=int(float(dato))                
                       
            dato=str(dato).replace("nan","")
            if glhomologa[n].iloc[fila]==False:
                if reportar_campo==1:
                    inserta_tabla_validacion(dato_llave,campo,gldfcompara.iloc[fila,numero_columna_excel],n,'mensaje_no_encuentra',rechazar_registro)
                paso_registro_correcto=False
            if glfun_valida_vacio[n].iloc[fila]==False:
                if reportar_campo==1:
                    inserta_tabla_validacion(dato_llave,campo,dato,n,'mensaje_vacio',rechazar_registro)
                paso_registro_correcto=False
            if glfun_valida_nulo[n].iloc[fila]==False:
                if reportar_campo==1:
                    inserta_tabla_validacion(dato_llave,campo,dato,n,'mensaje_nulo',rechazar_registro)
                paso_registro_correcto=False
            if glfun_valida_unico[n].iloc[fila]==False:
                if reportar_campo==1:
                    inserta_tabla_validacion(dato_llave,campo,dato,n,'mensaje_unico',rechazar_registro)
                paso_registro_correcto=False
            if glfun_valida_tres_caracteres[n].iloc[fila]==False:
                    if reportar_campo==1:
                        inserta_tabla_validacion(dato_llave,campo,dato,n,'mensaje_tres_caracteres_iguales',rechazar_registro)
                    paso_registro_correcto=False            
            if glfun_valida_fecha[n].iloc[fila]==False:
                    if reportar_campo==1:
                        inserta_tabla_validacion(dato_llave,campo,dato,n,'mensaje_fecha',rechazar_registro)
                    paso_registro_correcto=False              
            if glfun_valida_correo[n].iloc[fila]==False:
                    if reportar_campo==1:
                        inserta_tabla_validacion(dato_llave,campo,dato,n,'mensaje_correo',rechazar_registro)
                    paso_registro_correcto=False  
            if glfun_valida_numerico[n].iloc[fila]==False:
                    if reportar_campo==1:
                        inserta_tabla_validacion(dato_llave,campo,dato,n,'mensaje_numerico',rechazar_registro)
                    paso_registro_correcto=False 
            if glfun_valida_calculo[n].iloc[fila]==False:
                    if reportar_campo==1:
                        inserta_tabla_validacion(dato_llave,campo,dato,n,'mensaje_calculo',rechazar_registro)
                    paso_registro_correcto=False
                    
            if paso_registro_correcto==False and rechazar_registro==1:
                permite_registro=False
            
            if paso_registro_correcto==True:
                cadena_sql_act=cadena_sql_act+campo_destino+"='"+dato.replace("'","''")+"',"
                cadena_sql_ins=cadena_sql_ins + campo_destino+","
                cadena_sql_ins2=cadena_sql_ins2 +" '"+ str(dato).replace("'","''")+"',"
                
            obj_fila[campo_destino]=dato
            print n
            n=n+1
            
        if  permite_registro==True:
            arr_destino.append(obj_fila)
            cadena_sql_act=cadena_sql_act[0:len(cadena_sql_act)-1]
            cadena_sql_act=cadena_sql_act+" where "+campo_llave_externa+"="+str(glentidad_id) +" and "+llave_tabla+"='"+str(dato_llave)+ "'"
            cadena_sql_ins=cadena_sql_ins[0:len(cadena_sql_ins)-1]
            cadena_sql_ins=cadena_sql_ins+" )"
            cadena_sql_ins2=cadena_sql_ins2[0:len(cadena_sql_ins2)-1]
            if llave_tabla!="":
                cadena_sql_ins2=cadena_sql_ins2+" where (select count(*) from "+tabla_destino+" where "+campo_llave_externa+"="+str(glentidad_id) +" and "+llave_tabla+"='"+str(dato_llave)+"')=0"
            
            cadena_sql_act_total=cadena_sql_act_total+cadena_sql_act + " "
            cadena_sql_ins_total=cadena_sql_ins_total+ cadena_sql_ins+cadena_sql_ins2 + " "  
            
            if fila%100 == 0:
                consulta=""
                if glvalidacion_asociado["inserta"]==1:
                    consulta=consulta+ " "+ cadena_sql_ins_total
                if glvalidacion_asociado["actualiza"]==1:
                    consulta=consulta+ " "+ cadena_sql_act_total
                if consulta!="":
                    #print "fila "+str(fila)
                    #print consulta
                    conexion_base_insert(consulta)
                cadena_sql_ins_total=""
                cadena_sql_act_total=""
        if fila == 1465:
            c=987878
        print fila        
        fila=fila+1
    
    

    print "test1"
    #Crear Script Actualiza Inserta
    glarr_datos_destino=pd.DataFrame(arr_destino)
    #if glvalidacion_asociado["actualiza"]==1:
        #print cadena_sql_act_total
    
    consulta=""
    if glvalidacion_asociado["inserta"]==1:
        consulta=consulta+ " "+ cadena_sql_ins_total
    if glvalidacion_asociado["actualiza"]==1:
        consulta=consulta+ " "+ cadena_sql_act_total
    print "test2"
    import json
    #cadena2=json.dumps(arr_destino) # '[1, 2, [3, 4]]'
    #print consulta 
    
    print consulta
    if consulta!="":
        conexion_base_insert(consulta)    
    cont_arc=cont_arc+1

if len(glarr_datos_validacion)>0:
    glarr_datos_validacion = glarr_datos_validacion[['NOMBRE DE LA ENTIDAD', 'ARCHIVO/TABLA', 'IDENTIFICACIÓN DEL REGISTRO'
                                   , 'CAMPO CON OBSERVACIÓN', 'VALOR DEL CAMPO CON OBSERVACIÓN'
                                    , 'MOTIVO DE RECHAZO','ESTADO DEL REGISTRO'
                                   ]]
    
    escribir_excel(glarr_datos_validacion,'C:\\archivos_salida\\ReporteCalidad.xlsx','xlsxwriter',
               glanchocolumnas_valida.split(','))