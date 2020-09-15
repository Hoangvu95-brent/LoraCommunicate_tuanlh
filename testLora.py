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


    
    

