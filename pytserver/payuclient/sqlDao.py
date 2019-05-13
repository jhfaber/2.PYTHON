import sqlite3, os

class sqlDao:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "clientpayu.db")
        conn = sqlite3.connect(db_path)
        self.conn = conn
        self.db = conn.cursor()


    # Create table
    def createTables(self):
                  
        self.db.execute(
            '''
            CREATE TABLE IF NOT EXISTS plan (
                planCode,
                id,
                trialdays,
                interval,
                estado
                
                            
                            )

            '''           
             )
        print("TABLAN plan CREADA")
        self.db.execute(
            '''
            CREATE TABLE IF NOT EXISTS cliente (
                id,
                estado
                            )

            '''           
            )
        print("TABLAN cliente CREADA")
        self.db.execute(
            '''
            CREATE TABLE IF NOT EXISTS tarjeta (
                token,
                estado
                            )

            '''           
            )
        print("TABLAN tarjeta CREADA")
        self.db.execute(
            '''
            CREATE TABLE IF NOT EXISTS suscripcion (
                id,
                estado                
                            )

            '''           
            )
        print("TABLAN suscripcion CREADA")
        
        self.conn.commit()



    # Insert a row of data
    def insertData(self):
        self.db.execute('''INSERT INTO plan VALUES (
            'a5858dbc-fd22-4d7c-87ad-a6627b2b1b5a3'
            
            )'''
        
        )
        self.conn.commit()

    def selectData(self):
        # symbol = 'RHAT'
        print("**************************************PLANES****************************")
        self.db.execute("SELECT * FROM plan")
        while True:
            row = self.db.fetchone()
            if row == None:
                break
            print(row) 
        # symbol = 'RHAT'
        print("**************************************CLIENTES****************************")
        self.db.execute("SELECT * FROM cliente")
        while True:
            row = self.db.fetchone()
            if row == None:
                break
            print(row)
        print("**************************************TARJETAS*************************")
        self.db.execute("SELECT * FROM tarjeta")
        while True:
            row = self.db.fetchone()
            if row == None:
                break
            print(row)
        print("**************************************SUSCRIPCIONES***********************")
        self.db.execute("SELECT * FROM suscripcion")
        while True:
            row = self.db.fetchone()
            if row == None:
                break
            print(row)      
    
    
    def closeConnection(self):       
        self.conn.close()
    
    def commit(self):
        self.conn.commit()

    ################### INSERCIONES

    def crearPlan(self, diccionario, planCode):
        estado='activo'
        string= '''INSERT INTO plan VALUES (
            \''''+planCode+'''\',
            \''''+str(diccionario['id'])+'''\',
            \''''+str(diccionario['trialDays'])+'''\',
            \''''+str(diccionario['interval'])+'''\',
            \''''+estado+'''\'
            )'''
        
        # print(string)
        self.db.execute(string)
        self.commit()
        self.closeConnection()
    
    def crearCliente(self, diccionario):
        estado='activo'
        string= '''INSERT INTO cliente VALUES (            
            \''''+str(diccionario['id'])+'''\',
            \''''+estado+'''\'       
            
            )'''
        self.db.execute(string)
        self.commit()
        self.closeConnection()

    def crearTarjeta(self, diccionario):
        estado='activo'
        string= '''INSERT INTO tarjeta VALUES (            
            \''''+str(diccionario['token'])+'''\',
            \''''+estado+'''\'        
            
            )'''
        self.db.execute(string)
        self.commit()
        self.closeConnection()
    def crearSuscripcion(self, diccionario):
        estado='activo'
        string= '''INSERT INTO suscripcion VALUES (            
            \''''+str(diccionario['id'])+'''\',
            \''''+estado+'''\'       
            
            )'''
        self.db.execute(string)
        self.commit()
        self.closeConnection()

    def eliminarSuscripcion(self,id):
        estado='inactivo'
        string= '''UPDATE suscripcion
                   SET estado=\''''+estado+'''\'
                   WHERE  id=\''''+id+'''\''''

        # print(string)
        self.db.execute(string)
        self.commit()
        self.closeConnection()

    def eliminarTarjeta(self, id):
        estado='inactivo'
        string= '''UPDATE tarjeta
                   SET estado=\''''+estado+'''\'
                   WHERE  token=\''''+id+'''\';'''

        # print(string)
        self.db.execute(string)
        self.commit()
        self.closeConnection()

    def eliminarCliente(self, id):
        estado='inactivo'
        string= '''UPDATE cliente
                   SET estado=\''''+estado+'''\'
                   WHERE  id=\''''+id+'''\';'''

        # print(string)
        self.db.execute(string)
        self.commit()
        self.closeConnection()

    def eliminarPlan(self, id):
        estado='inactivo'
        string= '''UPDATE plan
                   SET estado=\''''+estado+'''\'
                   WHERE  planCode=\''''+id+'''\';'''

        # print(string)
        self.db.execute(string)
        self.commit()
        self.closeConnection()
    

    

