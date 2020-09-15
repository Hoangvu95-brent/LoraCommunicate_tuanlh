import serial
ser = serial.Serial ("/dev/ttyS0", 9600)  

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


f = open('codeTestSend.py','r')
codeString = f.read()
codeName = f.name
print(codeName)
print(codeString)
codeBit = text_to_bits(codeString)
print(codeBit)
lenCodeBit = len(codeBit)
print(lenCodeBit)

try:
    for code in range(0,lenCodeBit,20):
        send = codeBit[code:code+20]
        ser.write(send.encode())
        print(send)
        ser.flush()
except KeyboardInterrupt:
    f.close()
    print("Closed file")


