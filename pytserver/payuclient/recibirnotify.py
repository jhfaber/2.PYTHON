print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")

import os, sys, cgi



length = os.environ["CONTENT_LENGTH"] 
print(type(sys.stdin.read(int(length)))