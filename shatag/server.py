from shatag import *
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/host/<hostname>', methods=['POST'])
def add(host):
    print("host post {0} with data {1}\n".format(host, request.json))
    return jsonify(dummy=response, hello=world)

def run():
    app.run()

if __name__ == "__main__":
    app.run()
