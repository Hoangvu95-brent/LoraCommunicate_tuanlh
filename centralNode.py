from flask import Flask
import os
from flask import request
from flask_cors import CORS, cross_origin
import flask
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def hello():
    return "hello"
@app.route('/api/updateFirmware',methods=['POST'])
@cross_origin()
def upload():
    if request.method == "POST":
        if request.files:
            firmWare = request.files["updateFirmwareNode"]
            target = os.path.join(APP_ROOT,'firmware')
            firmWareName = firmWare.filename
            destination = "/".join([target,firmWareName])
            firmWare.save(destination)
            print("Receive firmWare")
            return "Sucessfully"