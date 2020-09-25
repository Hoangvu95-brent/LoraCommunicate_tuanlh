import serial
print("Tuan")
ser = serial.Serial ("/dev/ttyS0", 9600)    
f =open('testCode.txt','w')
try:
    while True:
        line = ser.read()
        f.write(line.decode())
        print(line, end="",flush=True)
except KeyboardInterrupt:  
    ser.close()
    f.close()
    print("Closed all")


    
    
https://5f6d590760cf97001641ab93.mockapi.io/:endpoint

url = "https://5f6d590760cf97001641ab93.mockapi.io/iot1?doorId=1&duration=1&NumberPerson=1&isOverTimeOut=true"

payload = "{\"doorId\":\"1\",\"duration\":34,\"NumberPerson\":364,\"isOverTimeOut\":false}"
headers = {
  'doorId': '1',
  'duration': '10',
  'NumberPerson': '13',
  'isOverTimeOut': 'false',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
