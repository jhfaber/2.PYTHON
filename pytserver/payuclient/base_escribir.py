def conexion_base_insert(sql): 
    from os import getenv
    import pyodbc
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
    numero_tabla = 0
    consulta = """ set nocount on;   """+sql
    cursor = conn.cursor()
    cursor.execute(consulta)
    conn.commit()
    conn.close()