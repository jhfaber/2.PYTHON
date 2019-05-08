print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")

import hashlib

string= "u5tkFm3nZTk7sxL5oEgwm80z77~798450~testedental8~10000~COP"
# string.encode("utf")

encode= hashlib.md5(string.encode("utf")).hexdigest()

print(encode)