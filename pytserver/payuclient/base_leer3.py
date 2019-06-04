def conexion_base(sql):
    import os
    import pandas as pd
    import cgi, cgitb
    import numpy as np
    #form = cgi.FieldStorage()
    # t1 = form.getvalue('t1')
    t1 = 10
    from os import getenv
    import pyodbc
    import os.path
    import sys
    
    server = getenv("bdglobal.database.windows.net")
    user = getenv("globalde")
    password = getenv("global&112008d")
    # conn = pymssql.connect(server, user, password, "globalde",as_dict=True)

    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 13 for SQL Server};'
        r'SERVER=bdglobal.database.windows.net;'
        r'DATABASE=globalde;'
        r'UID=globalde;'
        r'PWD=global&112008d2;'
    )
    # conn = pypyodbc.connect(host='bdglobal.database.windows.net', user='globalde', password='global&112008d2', database='globalde')
    cursor = conn.cursor()
    # cursor = conn.cursor(as_dict=True)

    # consulta="SELECT top {0} serial_prm,nombre_prm from dba_promotor select top 10 serial_suc,nombreempresa from dba_sucursales".format(t1)
    # consulta="select 1 as salida11";
    nombre_tablas = ["excluidos"]
    numero_tabla = 0
    consulta = """ set nocount on; 

     """+sql
    #print(consulta)
    
    cursor.execute(consulta)
    arrgen = []
    objgen = {}
    while True:
        arr1 = []
        for row in cursor.fetchall():
            n = 0
            obj1 = {}
            for column in cursor.description:
                # print column[0]
                # print row[n]
                obj1[column[0]] = row[n]
                n = n + 1
            arr1.append(obj1)
            # columns = [column[0] for column in cursor.description]
            # print row[1]
            # print column[0]
            # aList.append({column[0]:

        dfarr1 = pd.DataFrame(arr1)

        # arrgen.append(dfarr1)
        objgen[numero_tabla] = dfarr1
        numero_tabla = numero_tabla + 1
        if cursor.nextset() == False:
            break
       
            

    # print(Data[(Data['serial_prm'] == 13895) | (Data['serial_prm'] == 13890)])
    # print(Data[Data['serial_prm'].isin([13895,13890])])
    conn.close()
    return objgen

def conexion_base_sp(sql):
    import os
    import pandas as pd
    import cgi, cgitb
    import numpy as np
    #form = cgi.FieldStorage()
    # t1 = form.getvalue('t1')
    t1 = 10
    from os import getenv
    import pyodbc
    import os.path

    server = getenv("bdglobal.database.windows.net")
    user = getenv("globalde")
    password = getenv("global&112008d")
    # conn = pymssql.connect(server, user, password, "globalde",as_dict=True)

    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 13 for SQL Server};'
        r'SERVER=bdglobal.database.windows.net;'
        r'DATABASE=globalde;'
        r'UID=globalde;'
        r'PWD=global&112008d2;'
    )
    # conn = pypyodbc.connect(host='bdglobal.database.windows.net', user='globalde', password='global&112008d2', database='globalde')
    cursor = conn.cursor()
    # cursor = conn.cursor(as_dict=True)

    # consulta="SELECT top {0} serial_prm,nombre_prm from dba_promotor select top 10 serial_suc,nombreempresa from dba_sucursales".format(t1)
    # consulta="select 1 as salida11";
    nombre_tablas = ["excluidos"]
    numero_tabla = 0
    
    consulta = """  
SET NOCOUNT ON
     """+sql
    error=0
    try:
        #print(consulta)
        cursor.execute(consulta)
        #cursor.callproc('Spu_insertapaciente_interfaces2', ("""{salida_json}""".format(salida_json=salida_json),))
        arrgen = []
        objgen = {}
        while True:
            arr1 = []
            for row in cursor.fetchall():
                n = 0
                obj1 = {}
                for column in cursor.description:
                    # print column[0]
                    # print row[n]
                    obj1[column[0]] = row[n]
                    n = n + 1
                arr1.append(obj1)
                # columns = [column[0] for column in cursor.description]
                # print row[1]
                # print column[0]
                # aList.append({column[0]:

            dfarr1 = pd.DataFrame(arr1)

            # arrgen.append(dfarr1)
            objgen[numero_tabla] = dfarr1
            numero_tabla = numero_tabla + 1
            if cursor.nextset() == False:
                break
    except:
        error=1
        conn.rollback()
        #print sys.exc_info()[0]
    # print(Data[(Data['serial_prm'] == 13895) | (Data['serial_prm'] == 13890)])
    # print(Data[Data['serial_prm'].isin([13895,13890])])
    if error==0:
        conn.commit()
    conn.close()
    return objgen