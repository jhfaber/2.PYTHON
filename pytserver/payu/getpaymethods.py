
print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")
# importing the requests library
import requests
from pprint import pprint
import json

API_ENDPOINT = "https://sandbox.api.payulatam.com/payments-api/4.0/service.cgi "


data = {
   "test": "false",
   "language": "en",
   "command": "GET_PAYMENT_METHODS",
   "merchant": {
      "apiLogin": "xxxxxxxxxxxxx",
      "apiKey": "xxxxxxxxxxxxx"
   }


}
data = json.dumps(data)
r = requests.post(url= API_ENDPOINT,data= data)



#pprint(vars(r))
print(r.text)
