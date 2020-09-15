import serial
ser = serial.Serial ("/dev/ttyS0", 9600)
# de uart cao hon, 115000    
code = ''
codeName = ''
flagStartBody = False
flagName = False
try:
    while True:
        data= ser.read()
        if(flagStartBody and data != b'@' and data !=b'$'):
            code += data.decode()
        if(flagName and data != b'@'):
            codeName +=data.decode()
        if(data == b'&'): # start sending data,begin with namefile
            flagName = True
        if(data == b'@'): # start sedning code
            flagStartBody = True
            flagName = False
        if(data == b'$'): # finish sending code
            flagStartBody = False
            print(codeName)
            print(code)
            f = open(codeName,'a')
            f.write(code)
            f.close()
            code = ''
            codeName = ''
except KeyboardInterrupt:
    ser.close()
    
    print("Closed all")


    
    

