import sqlite3

class sqlDao:
    def __init__(self):
        
        conn = sqlite3.connect('clientpayu.db')
        self.conn = conn
        self.db = conn.cursor()


    # Create table
    def createTables(self):
                  
        self.db.execute(
            '''
            CREATE TABLE plan (
                id,               
                            )

            '''           
             )
        self.db.execute(
            '''
            CREATE TABLE plan_additionalvalues (
                name,
                value,
                currency
                            )

            '''           
            )
        # self.db.execute(
        #     '''
        #     CREATE TABLE plan_additionalvalues (
        #         name,
        #         value,
        #         currency
        #                     )

        #     '''           
        # )
        self.conn.commit()



    # Insert a row of data
    def insertData(self):
        self.db.execute('''INSERT INTO plan VALUES (
            'a5858dbc-fd22-4d7c-87ad-a6627b2b1b5a3',
            '1',
            'nnmm',
            '805394',
            '1',
            'MONTH',
            '12',
            '0',
            '1',
            '0',
            '0'
            )
            '''
        
        )
        self.conn.commit()

    def selectData(self):
        # symbol = 'RHAT'
        self.db.execute("SELECT * FROM plan")
        while True:
            row = self.db.fetchone()
            if row == None:
                break
            print(row)   
    
    
    def closeConnection(self):       
        self.conn.close()
    
    def commit(self):
        self.conn.commit()

