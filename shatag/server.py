from shatag import *
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/host/<hostname>', methods=['POST'])
def add(host):
    print("host post {0} with data {1}\n".format(host, request.json))

def run():
    app.run()
