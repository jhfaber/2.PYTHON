print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")

import cgi
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import json
from flask import Flask, request
# import cherrypy import request


# cgitb.enable()
# client = MongoClient('localhost',
#                       username='globalde',
#                       password='global&112008d2',      
#                      authMechanism='SCRAM-SHA-256')

# client = MongoClient('localhost', 27017)


# print(request.params['name'])

# data  = json.loads(name)

# print(GET.get('name'))

# db = client.edental
# result = db.trafico_red.insert_many(data)



# print("respuesta: \n"+name)
