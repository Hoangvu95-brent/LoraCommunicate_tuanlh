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
