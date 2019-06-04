print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")

import os, sys, json


if not os.environ["CONTENT_LENGTH"]:
    data= {    } 
else:
    post_length = int(os.environ['CONTENT_LENGTH'])
    post_string = sys.stdin.buffer.read(post_length).decode('utf-8')
    data = json.loads(post_string)


# values=data["additionalValues"][0]

print(json.dumps(data))





