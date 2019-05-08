print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")

import cgi, cgitb
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import json

client = MongoClient('localhost',27017)


form = cgi.FieldStorage() #

name = ""
name=form.getvalue('name')
data  = json.loads(str(name))
#print(data)


#print (data)
db = client.mymongo
result = db.test.insert_one(data)

#action=form.getvalue('election') #traer la variable post o get

print("respuesta:     \n" + name,result)
client.close()
