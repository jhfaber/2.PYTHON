print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")



import requests
if __name__ == '__main__':
    # url = 'https://sandbox.api.payulatam.com/reports-api/4.0/service.cgi'
    url= 'http://httpbin.org/get'
    data = {
                # "test": "false",
                # "language": "en",
                # "command": "PING",
                # "merchant": {
                #     "apiLogin": "pRRXKOl8ikMmt9u",
                #     "apiKey": "4Vj8eK4rloUd272L48hsrarnUA"
                }
    response = requests.get(url=url)#, params= data)

    print(response) #devuelve el estado del recurso


    if response.status_code== 200:
        content=print(response.content)
    
