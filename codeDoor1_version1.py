#import library
from queue import Queue
import RPi.GPIO as GPIO
import serial
import requests
import time
import pygame
from time import sleep
from queue import Queue

form=["signature","opcode","number1","number2","doorID","time1","time2","status","from"]
SETUP_NODE = bytearray.fromhex("69 10 00 00 01 00 00 00 01")
form_resporn=["signature","opcode","status","from"]
RES_TOKEN = bytearray.fromhex("69 04 00 01")
RES_STATUS = bytearray.fromhex("69 11 01 01")
RES_STATUS_UPDATE = bytearray.fromhex("69 11 00 01")
RES_NODE_ONLINE   = bytearray.fromhex("69 02 00 01")
RES_SENSOR = bytearray.fromhex("69 00 00 00 01 00 00 00 01")
RES_FW_Update = bytearray.fromhex("69 01 00 00 01 00 00 00 01")

#status
OPEN   = 1
CLOSE  = 0
OPEN_TIMEOUT  = 2
#Size
sizeOfNotifyDoorOpen              = 8
sizeNotifyStartup                 = 5
sizeOfSetupNode                   = 8
sizeOfCheckNodeOnline             = 4
sizeOfCheckNodeOnline_Response    = 5
#NodeSatatus
NOTIFI_DOOR_OPEN = 1
NOTIFI_STARTUP   = 2
CHECK_NODE_ONLINE_RESPONSE = 3
#Opcode
Signature        = "0xAA"
CMDOpcode        = "0x10"
doorId           = "0x01"
timeOut = 10
timeOut_speaker = 3
TURN_ON = 0
TURN_OFF = 1
NumberPerson=0
########
statusDoor = CLOSE
enableAlarm = 1
speaker     = 1
start = 0
queue = []
Time=0
queue.append(SETUP_NODE)
ser = serial.Serial ("/dev/ttyS0", 9600)
#################

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Cam bien tu cua
#GPIO.setup(12, GPIO.IN) # cam bien hong ngoai1
#GPIO.setup(13, GPIO.IN) # cam bien hong ngoai2
GPIO.setup(17, GPIO.OUT) # chan trang thai cua chuong
GPIO.setup(12, GPIO.IN,pull_up_down=GPIO.PUD_UP)
##############
#def sendData():
#def sendData1():
#def initData():
def FW_Update():
    code =''
    codeName=''
    flagStartBody=False
    flagName=False
    try:
        data=ser.read()
        if(flagStartBody and data !=b'@' and data !=b'$'):
            code += data.decode()
        if (flagName and data !=b'@'):
            codeName += data.decode()
        if (data == b'&'):
            flagName = True
        if (data == b'@'):
            flagStartBody = True
            flagNAme = False
        if (data == b'$'):
            flagStartBody = False
            print(codeName)
            print(code)
            f=open(codeName,'a')
            f.write(code)
            f.close()
            exec(open(codeName).read())
            code=''
            codeName=''
    except KeyboardInterrupt:
        ser.close()
        print("close all")
def runNotifyDoor():
    global OPEN   
    global CLOSE  
    global OPEN_TIMEOUT
    global timeOut 
    global TURN_ON 
    global TURN_OFF 
########
    global statusDoor
    global enableAlarm
    global start
    global listq
    global NumberPerson
    global Time
    if (statusDoor == CLOSE):
        if (GPIO.input(4)==1):
            statusDoor = OPEN
            start = time.time()
            '''if (GPIO.input(12)==0):
                start = time.time()
                NumberPerson=NumberPerson+1
                pygame.init()
                pygame.mixer.music.load("xinchao.wav")
                pygame.mixer.music.play()'''
          
        
    if (statusDoor == OPEN):
        if (GPIO.input(12)==0):
                start = time.time()
                pygame.init()
                pygame.mixer.music.load("xinchao.wav")
                pygame.mixer.music.play()
                NumberPerson=NumberPerson+1
                time.sleep(0.03)
        if (GPIO.input(4)==1):
            '''if (GPIO.input(12)==0):
                start = time.time()
                pygame.init()
                pygame.mixer.music.load("xinchao.wav")
                pygame.mixer.music.play()
                NumberPerson=NumberPerson+1'''
                
            Time=time.time()-start
            if (int(Time)>timeOut):
                listData=[]
                
                #initData(NOTIFI_DOOR_OPEN, listData,Time )
                SETUP_NODE[6]=int(Time%256)
                SETUP_NODE[5]=int(Time/256)
                SETUP_NODE[3]=int(NumberPerson%256)
                SETUP_NODE[2]=int(NumberPerson/256)
                SETUP_NODE[7]=1
                #ser.write(SETUP_NODE)
                #ser.flush()
                print("Dong qua", Time, " ",NumberPerson)
                print("TRONG HAM",SETUP_NODE)
                queue.append(SETUP_NODE)
                NumberPerson=0
                Time=0
                if (enableAlarm == 1):
                    GPIO.output(17,TURN_ON)
                statusDoor = OPEN_TIMEOUT
                #statusDoor = CLOSE
                #time.sleep(1)
        else :
        #if (GPIO.input(4)==0):
            Time = time.time() - start
            if (int(Time)<timeOut):
                listData = []
                #initData(NOTIFI_DOOR_OPEN, listData, Time)
                
                SETUP_NODE[6]=int(Time%256)
                SETUP_NODE[5]=int(Time/256)
                SETUP_NODE[3]=int(NumberPerson%256)
                SETUP_NODE[2]=int(NumberPerson/256)
                SETUP_NODE[7]=0
                #ser.write(SETUP_NODE)
                #ser.flush()
                print("Dong qua", Time, " ",NumberPerson )
                NumberPerson=0
                Time=0
                queue.append(SETUP_NODE)
                time.sleep(1)
                statusDoor = CLOSE
               

    if (statusDoor == OPEN_TIMEOUT):
        
        if (GPIO.input(4)==0):
            statusDoor = CLOSE
            NumberPerson=0
            if (enableAlarm == 1):
                GPIO.output(17,TURN_OFF)

#def Reset():
GPIO.output(17,TURN_OFF)

while True:
    runNotifyDoor()
    #print(queue)
    #sleep(0.3)
    data = ser.read()
    #read serial port
    sleep(0.01)
    data_left = ser.inWaiting()             #check for remaining byte
    data += ser.read(data_left)
    print ("DATA",data)                   #print received data
    #sleep(0.5)
    #if (data[0]==0xAA):
       # if (data[1]==0x00):
            #reset()
        #elif(data[1]==0x05):'''
    if(data[0]==105 and data[1]==4 and data[2]==1  and data[3]==0 ):
        if (len(queue)!=0):
            print("da nhan duoc key")
            '''RES_TOKEN[2]=1
            ser.write(RES_TOKEN)
            ser.flush()'''
            time.sleep(0.03)
            ser.write(queue[0])
            print("TRONG KEY",queue[0])
            ser.flush()
            del queue[0]
            time.sleep(0.03)
            time.sleep(0.4)
            ser.write(RES_STATUS)
            ser.flush()
        else:
            time.sleep(0.03)
            RES_TOKEN[2]=0
            ser.write(RES_TOKEN)
            ser.flush()
    if (data[0]==105 and data[1]==4 and data[3]==0 and len(data)==7):
        time.sleep(0.03)
        RES_TOKEN[2]=0
        ser.write(RES_TOKEN)
        ser.flush()
    #update cho alarm#5
    if(data[0]==105 and data[1]==4 and data[2]==2 and data[3]==0): 
        RES_TOKEN[2]=0
        ser.write(RES_TOKEN)
        ser.flush()
    if (data[0]==105 and data[1]==1 and data[4]==1 and data[8]==0):
        FW_Update()
        
    if(data[0]==105 and data[1]==6 and data[4]==1 and data[8]==0): #update magnetic sensor
        enableAlarm = data[7]
        timeOut     = int(data[5])
        timeOut     = timeOut<<8
        timeOut    += int(data[6])
        RES_STATUS_UPDATE[2]=1
        #ser.write(RES_STATUS_UPDATE)
        #ser.flush()
    #update cho specker
    if(data[0]==105 and data[1]==8 and data[4]==1 and data[8]==0): #update radio sensor
        speaker     = data[7]
        timeOut_speaker = int(data[5])
        timeOut_speaker = timeOut_speaker<<8
        timeOut_speaker+= int(data[6])
        RES_STATUS_UPDATE[2]=1
        #ser.write(RES_STATUS_UPDATE)
        #ser.flush()
     #update cho RFID
    if(data[0]==105 and data[1]==10 and data[4]==1 and data[8]==0): #update RFID sensor
        pass
    
    if(data[0]==105 and data[1]==5  and data[4]==1 and data[2]==1 and data[8]==0):
        RES_SENSOR[1]=5
        RES_SENSOR[6]=int(timeOut%256)
        RES_SENSOR[5]=int(timeOut/256)
        RES_SENSOR[7]=enableAlarm
        ser.write(RES_SENSOR)
        ser.flush()
    if(data[0]==105 and data[1]==7  and data[4]==1 and data[2]==1 and data[8]==0):
        RES_SENSOR[1]=7
        RES_SENSOR[6]=int(timeOut_speaker%256)
        RES_SENSOR[5]=int(timeOut_speaker/256)
        RES_SENSOR[7]=speaker
        ser.write(RES_SENSOR)
        ser.flush()  

             
   

