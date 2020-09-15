import serial
import time
ser = serial.Serial ("/dev/ttyS0", 9600)  


f = open('openFile.py','r')
codeString = f.read()
codeName = f.name
print(codeName)
print(codeString)

try:
    ser.write(b'&')
    ser.write(codeName.encode())
    ser.flush()
    ser.write(b'@')
    ser.flush()
    for c in codeString:
        ser.write(c.encode())
        ser.flush
    ser.write(b'$')
except KeyboardInterrupt:
    ser.close()
    f.close()
    print("Closed file")


