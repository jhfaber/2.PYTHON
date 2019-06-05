#!/usr/bin/python
# coding: latin-1
print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n\n\n")
print("Ñolá")
import pandas as pd
import unicodedata

def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
    return s.decode()
def elimina_acentos_columnas(df):
    n=0
    lista_col={}
    while n<len(df.columns):
        lista_col[df.columns[n]]=elimina_tildes(df.columns[n])
        
        n=n+1
        
    df.rename(columns=lista_col, inplace = True) 
    return df

print("Ñolá")
df = pd.read_excel("C:\\archivos_lectura\\test.xlsx")
print df.iloc[0,[0]]
d2=df.copy()
d2["calculo"]=1
import os.path
writer = pd.ExcelWriter("C:\\archivos_lectura\\test2.xlsx")
d2.to_excel(writer,'Hoja1')
writer.save()

df = pd.read_excel("C:\\archivos_lectura\\ASOCIADOS.xlsx")
print df.columns
print("CASTAÑEDA")

print df.iloc[0,:]


df=elimina_acentos_columnas(df)
print df.iloc[0,:]