import sqlDao



if __name__ == "__main__":
    DB = sqlDao.sqlDao()
    DB.selectData()




################# INSERT DE MUESTRA #########3
# print(storage['id'])



            
""" string= '''INSERT INTO plan VALUES (
            \''''+str(storage['id'])+'''\',
            \''''+str(storage['planCode'])+'''\',
            \''''+str(storage['description'])+'''\',
            \''''+str(storage['accountId'])+'''\',
            \''''+str(storage['intervalCount'])+'''\',
            \''''+str(storage['interval'])+'''\',
            \''''+str(storage['maxPaymentsAllowed'])+'''\',
            \''''+str(storage['maxPaymentAttempts'])+'''\',
            \''''+str(storage['paymentAttemptsDelay'])+'''\',
            \''''+str(storage['maxPendingPayments'])+'''\',
            \''''+str(storage['trialDays'])+'''\'
            )
            '''

# print(string)
settings.DB.db.execute(string)
settings.DB.commit()
# settings.DB.selectData()
settings.DB.closeConnection() """
