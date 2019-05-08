print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")



import requests
import json

url = 'https://sandbox.api.payulatam.com/payments-api/4.0/service.cgi'



##############BUILD JSON PING#################
data = {
                "test": "false",
                "language": "en",
                "command": "PING",
                
        }

merchant={}
merchant['apiLogin'] = 'pRRXKOl8ikMmt9u'
merchant['apiKey'] = '4Vj8eK4rloUd272L48hsrarnUA'
data['merchant'] = merchant
########################################



response = requests.post(url, json= data)


# if response.status_code== 200:
content=print(response.content)