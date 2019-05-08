print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")

import os, sys, cgi

# the query string, which contains the raw GET data
# (For example, for http://example.com/myscript.py?a=b&c=d&e
# this is "a=b&c=d&e")


# the raw POST data
length = os.environ["CONTENT_LENGTH"] 
print(sys.stdin.read(int(length)))
# print(type(length))
# print(length)
# print(type(sys.stdin.read(int(length))))