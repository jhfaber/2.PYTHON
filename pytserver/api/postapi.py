print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")



import requests
import json



if __name__ == '__main__':
    # url = 'https://sandbox.api.payulatam.com/reports-api/4.0/service.cgi'
    url= 'http://httpbin.org/post'
    headers = {
        'Conten-Type': 'application/json'
    }
    payload = {
                "test": "nonas",
                "language": "en",
                "command": "PING",
                # "merchant": {
                #     "apiLogin": "pRRXKOl8ikMmt9u",
                #     "apiKey": "4Vj8eK4rloUd272L48hserarnUA"
                }
    #json = post se encarga de serializarlo
    #data = post no lo serealiza 
    response = requests.post(url, json= payload, headers=headers)

    print(response) #devuelve el estado del recurso


    if response.status_code== 200:
        content=print(response.content)

        #LEER DICCIONARIO
        headers_response = response.headers
        print(headers_response)
    


