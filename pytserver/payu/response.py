print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")

import cgi
from pprint import pprint
args= cgi.FieldStorage()

# print(type(args))
pprint(vars(args))
# print(args)
param= args['message']

print(param)


