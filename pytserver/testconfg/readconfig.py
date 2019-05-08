print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")




import json, os

CONF = '\\testconfg\\config.json'
cwd = os.getcwd() + CONF
with open(cwd, 'r') as file:
    config = json.load(file)

database_name = config['DEFAULT']['DB_NAME']
database_password = config['DEFAULT']['DB_PASSWORD']


print(database_name)