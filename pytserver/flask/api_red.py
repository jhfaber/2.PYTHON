print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")

import cgi, cgitb
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import json

# client = MongoClient('localhost',
#                       username='globalde',
#                       password='global&112008d2',      
#                      authMechanism='SCRAM-SHA-256')

form = cgi.FieldStorage() #

name = ""
name=form.getvalue('name')

print(name)
# data  = json.loads(name)
# print(type(name))
#print (data)
# db = client.edental
# result = db.trafico_red.insert_many(data)

#action=form.getvalue('election') #traer la variable post o get 

# print("respuesta:     \n" + name)#,result)
