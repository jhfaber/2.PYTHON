print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")

# importing the requests library
import requests
from pprint import pprint
from flask import Flask, render_template, request

app= Flask(__name__)

@app.route("/")
def index():
    return render_template('test.html')

# defining the api-endpoint
API_ENDPOINT = "https://sandbox.api.payulatam.com/payments-api/4.0/service.cgi "

# your API key here
#API_KEY = "XXXXXXXXXXXXXXXXX"

# data to be sent to api
#api

app.run()


# sending post request and saving response as response object
#r = requests.post(url = API_ENDPOINT,data = data)

# extracting response text


#pprint(vars(r))
#print(r.text)
