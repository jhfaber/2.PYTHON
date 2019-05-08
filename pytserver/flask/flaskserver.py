print("HTTP/1.1 200 OK")
print("Access-Control-Allow-Origin: *")
print("Content-Type: text/json\n")



from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route("/", methods=["POST"])
def hello():
    dataDict = request.get_json()
    return jsonify(dataDict)
    # return "hi flask"

if __name__ == "__main__":
    app.run()



