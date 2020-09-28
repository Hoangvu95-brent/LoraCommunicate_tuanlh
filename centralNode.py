import time
from flask import Flask, jsonify
from multiprocessing import Process, Value
import os
from flask import request
from flask_cors import CORS, cross_origin
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
cors = CORS(app)


@app.route('/',methods=['GET'])
@cross_origin()
def hello():
     return "Test server flask sucessfully"


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
def record_loop():
    while True:
        print("dndfasfm")
        time.sleep(1)

if __name__ == "__main__":
    p = Process(target=record_loop)
    p.start()  
    app.run(debug=True, use_reloader=False)
    p.join()