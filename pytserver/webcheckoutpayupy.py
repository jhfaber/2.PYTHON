
print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")
# importing the requests library
import requests
from pprint import pprint

# defining the api-endpoint
API_ENDPOINT = "https://sandbox.checkout.payulatam.com/ppp-web-gateway-payu/"

# your API key here
#API_KEY = "XXXXXXXXXXXXXXXXX"

# data to be sent to api
data = {
   "merchantId":    "508029",
  "accountId"   :  "512321" ,
  "description" :  "Test PAYU",
  "referenceCode": "TestPayU" ,
  "amount"        :"20000",
  "tax"           :"3193"  ,
  "taxReturnBase" :"16806" ,
  "currency"      :"COP" ,
  "signature"     :"7ee7cf808ce6a39b17481c54f2c57acc"  ,
  "test"          :"1" ,
  "buyerEmail"    :"test@test.com" ,
  "responseUrl"    :"http://www.test.com/response" ,
  "confirmationUrl" :   "http://www.test.com/confirmation" ,

}

# sending post request and saving response as response object
r = requests.post(url = API_ENDPOINT,data = data)

# extracting response text


pprint(vars(r))
print(r.text)
