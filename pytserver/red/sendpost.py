""" Envio post a python local """


print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")


import requests
import json
import base64
from requests_toolbelt.utils import dump
import os
import sys
from flask import Flask, request



############## CONF URL ##########################
URL = 'http://127.0.0.1/py/red/api_red.py'


headers = {
    'Content-Type' : 'application/json',
    'Accept':'application/json',
    
}
cwd = os.getcwd() +'\\red\\data.json'
with open(cwd, 'r') as json_file:
    data = json_file.read()
data_json= json.loads(data)

data_basica = {
    'name': 'test send'
}

response = requests.post(URL, data= data_basica, headers= headers)

content=print(response.content)


