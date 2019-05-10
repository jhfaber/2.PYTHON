import sqlite3

class sqlDao:
    def __init__(self, db):
        self.db= db
        self.conn = sqlite3.connect('example.db')
        self.db = conn.cursor()


    # Create table
    def createTable(self):
        self.db.execute('''CREATE TABLE plan
                (date text, trans text, symbol text, qty real, price real)''')

    # Insert a row of data
    def insertData(self):
        self.db.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    def selectData(self):
        self.db.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)
        print(self.c.fetchone())
    
    def main(self):
        # c=createConnection()
        symbol = 'RHAT'
        
        c.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)
        print(c.fetchone())
    
    def closeConnection(self):        
        conn.commit()
        conn.close()

