print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")


import json
import os

cwd = os.getcwd() +'\\red\\data.json'
with open(cwd, 'r') as json_file:
    data = json_file.read()

json_data = json.loads(data)

# print(json.dumps(json_data, indent=4))