consulta="""DECLARE @json NVARCHAR(MAX)
SET @json =  
  N'{cadena_json}' 


INSERT INTO dba_test
(Serial_PPAC,
nocarnet)

SELECT a.serial_ppac,a.propuesta

FROM 
 OPENJSON ( @json ) 
WITH (  
             prima  int '$.prima',
             propuesta varchar(1000) '$propuesta'
 ) a
 
 select 1 as salida
""".format(cadena_json=df2.to_json(orient='records'))
#print(consulta)
d1=bl3.conexion_base_sp(consulta)