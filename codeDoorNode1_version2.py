#import library
from queue import Queue
import RPi.GPIO as GPIO
import serial
import requests
import time
import pygame
import subprocess
import os 
from time import sleep
from queue import Queue
import command
'''f=open("PID.txt",'r')
a=f.read()    
if (a!=" "):
    subprocess.call(["kill","-9",a])
f=open("PID.txt",'w')
f.write("")
f.close()'''

form=["signature","opcode","number1","number2","doorID","time1","time2","status","from"]   #get the form from the command file
SETUP_NODE = command.NOTIFY_DOOR
RES_SENSOR = command.RES_SENSOR
RES_FW_Update = command.RES_FW_Update

form_resporn=["signature","opcode","status","from"]
RES_TOKEN = command.RES_TOKEN
RES_STATUS = command.RES_STATUS
RES_STATUS_UPDATE = command.RES_STATUS_UPDATE
RES_NODE_ONLINE   = command.RES_NODE_ONLINE
RES_UPDATE_FIRMWARE = command.RES_UPDATE_FIRMWARE
##############
RES_TOKEN[3] = command.fromnode[1]
RES_STATUS[3] = command.fromnode[1]
RES_STATUS_UPDATE[3] = command.fromnode[1]
RES_NODE_ONLINE[3] = command.fromnode[1]
TOKEN = command.TOKEN
#############
OPEN   = command.OPEN
CLOSE  = command.CLOSE
OPEN_TIMEOUT  = command.OPEN_TIMEOUT
timeOut = command.timeOut
timeOut_speaker = command.timeOut_speaker
TURN_ON = command.TURN_ON
TURN_OFF = command.TURN_OFF
NumberPerson = command.NumberPerson
########
statusDoor = command.statusDoor
enableAlarm = command.enableAlarm
speaker     = command.speaker
start = command.start
SETUP_NODE[4]=1
queue = []
Time=0
queue.append(SETUP_NODE)

#################
ser = serial.Serial ("/dev/ttyS0", 9600,timeout=0.03)
#stop=command.stop

#Open port with baud rate
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)                                            # magnetic sensor pins
GPIO.setup(17, GPIO.OUT)                                                                    # bell connection pins
GPIO.setup(12, GPIO.IN,pull_up_down=GPIO.PUD_UP)                                            # infrared sensor pins
##############
def FW_Update(length):                                                                            # read the updated data from the center
    length = int(length)
    code =''
    codeName=''
    flagStartBody=False
    flagName=False
    dem = 0
    print("ok")
    try:
        while True:
            data=ser.read()
            dem+=1
            print("do dai la ", dem)
            if(flagStartBody and data !=b'@' and data !=b'$'):
                code += data.decode()
            if (flagName and data !=b'@'):
                codeName += data.decode()
            if (data == b'&'):
                flagName = True
            if (data == b'@'):
                flagStartBody = True
                flagNAme = False
            if (dem == length ):
                flagStartBody = False
                f=open("/home/pi/Desktop/Code/new.py",'w')
                f.write(code)
                f.close()
                dem =0
                print(codeName)
                print(code)
                f= open("/home/pi/Desktop/Code/New.txt",'w')
                f.write("0")
                f.close()
                time.sleep(1)
                subprocess.call(["reboot"])

                #exec(open("new.py").read())
                sys.exit()
                code=''
                codeName=''
                #subprocess.call(["reboot"])

    except:
        pass
       
def runNotifyDoor(endtime):                                                                        #handle door states
    global OPEN   
    global CLOSE  
    global OPEN_TIMEOUT
    global timeOut 
    global TURN_ON 
    global TURN_OFF 
    global statusDoor
    global enableAlarm
    global start
    global listq
    global NumberPerson
    global Time
    global speaker
    if (statusDoor == CLOSE):                                                              
        if (GPIO.input(4)==1):                                                              
            statusDoor = OPEN
            start = time.time()
        
    if (statusDoor == OPEN):                                                                
        if (GPIO.input(12)==0):                                                          
                pygame.init()
                if (speaker==1):
                    pygame.mixer.music.load("/home/pi/Desktop/Code/xinchao.wav")
                    pygame.mixer.music.play()
                NumberPerson=NumberPerson+1
                time.sleep(0.5)
                start = time.time()
        if (GPIO.input(4)==1):
            Time=time.time()-start
            if ((Time)>=float(timeOut)):
                
                #print("stop time",time.time())
                listData=[]
                SETUP_NODE[4]=command.doorID[1]
                SETUP_NODE[6]=int(Time%256)
                SETUP_NODE[5]=int(Time/256)
                SETUP_NODE[3]=int(NumberPerson%256)
                SETUP_NODE[2]=int(NumberPerson/256)
                SETUP_NODE[7]=1
                SETUP_NODE[8]=command.fromnode[1]
                print("Dong qua", Time, " nguoi ",NumberPerson," timeout ", timeOut)
                #print("TRONG HAM",SETUP_NODE)
                queue.append(SETUP_NODE)
                NumberPerson=0
                Time=0
                if (enableAlarm == 1):
                    GPIO.output(17,TURN_ON)
                statusDoor = OPEN_TIMEOUT
        else:
            Time = int(time.time() - start)
            if ((Time)<float(timeOut)):
               
                listData = []
                print("Dong truoc", Time, " nguoi ",NumberPerson," timeout ", timeOut)

                SETUP_NODE[4]=command.doorID[1]
                SETUP_NODE[6]=int(Time%256)
                SETUP_NODE[5]=int(Time/256)
                SETUP_NODE[3]=int(NumberPerson%256)
                SETUP_NODE[2]=int(NumberPerson/256)
                SETUP_NODE[7]=0
                SETUP_NODE[8]=command.fromnode[1]
                #print("Dong qua", Time, " ",NumberPerson )
                NumberPerson=0
                Time=0
                queue.append(SETUP_NODE)
                statusDoor = CLOSE
  
    if (statusDoor == OPEN_TIMEOUT):
        
        if (GPIO.input(4)==0):                                                              #Magnetic sensors receive signals
            statusDoor = CLOSE
            NumberPerson=0
            if (enableAlarm == 1):
                GPIO.output(17,TURN_OFF)

GPIO.output(17,TURN_OFF)
while True:
    f= open("/home/pi/Desktop/Code/New.txt",'r')
    a=f.read()
    if (a=="0"):
        for i in range(0,2):
            ser.write(RES_UPDATE_FIRMWARE)
            ser.flush()
            time.sleep(1)
    f= open("/home/pi/Desktop/Code/New.txt",'w')
    f.write(" ")
    f.close()
    runNotifyDoor(time.time())
    data = ser.read()
    time.sleep(0.01)
    data_left = ser.inWaiting()                                                             #check for remaining byte
    data += ser.read(data_left)
    if (data):

        #if (data==command.signature):
    #read serial port    
        #print("-----------------------------------------------------------")
        #start =time.time()
        time.sleep(0.01)
        data_left = ser.inWaiting()                                                             #check for remaining byte
        data += ser.read(data_left)
        #endtime=time.time()
        #print(start,"         ", endtime)
        #print (data)
        '''data =[]
        s = ser.read()
        data.append(s)
        #if (data[0]==command.signature):
        for i in range(1,9):
            s = ser.read()
            data.append(s)'''
        print (data) 
        #print received data
        if(data[0]==command.signature and data[1]==command.opcode[4] and data[2]==command.number_token[1]  and data[3]==command.fromnode[0] ):  # check token
            if (len(queue)!=0):
                #print("da nhan duoc key")
                time.sleep(0.03)
                ser.write(queue[0])
                #print("TRONG KEY",queue[0])
                ser.flush()
                del queue[0]
                '''time.sleep(0.03)
                time.sleep(0.4)
                ser.write(RES_STATUS)
                ser.flush()'''
            else:
                time.sleep(0.03)
                RES_TOKEN[2]=0
                ser.write(RES_TOKEN)
                ser.flush()
        '''if (data[0]==command.signature and data[1]==command.opcode[4] and data[3]==0 and len(data)==7):
            time.sleep(0.03)
            RES_TOKEN[2]=0
            ser.write(RES_TOKEN)
            ser.flush()'''
        #update cho alarm#5
        if (data[0]==105 and data[1]==4 and data[2]==2 and data[3]==0):
            RES_TOKEN[2]=0
            ser.write(RES_TOKEN)
            ser.flush()
        if (data[0]==command.signature and data[1]==command.opcode[1] and data[4]==command.doorID[1] and data[8]==command.fromnode[0]): #FW_update Node
            print("update")
            time.sleep(1)
            data = ser.read()                                                                       #read serial port
            sleep(0.03)
            data_left = ser.inWaiting()                                                             #check for remaining byte
            data += ser.read(data_left)
            print(data)
            FW_Update(data.decode())
        if(data[0]==command.signature and data[1]==command.opcode[6] and data[4]==command.doorID[1]):  #update magnetic sensor
            #SSSSprint("xu ly")
            enableAlarm = data[7]
            timeOut     = int(data[5])
            timeOut     = timeOut<<8
            timeOut    += int(data[6])
            speaker     = data[8]
            print("nhan dc ", timeOut)
            for i in range(0,2):
                RES_TOKEN[2]=0
                ser.write(RES_TOKEN)
                ser.flush()
                time.sleep(1)

        if(data[0]==command.signature and data[1]==command.opcode[8] and data[4]==command.doorID[1] and data[8]==command.fromnode[0]): #update radio sensor
            speaker     = data[7]
            timeOut_speaker = int(data[5])
            timeOut_speaker = timeOut_speaker<<8
            timeOut_speaker+= int(data[6])
            RES_STATUS_UPDATE[2]=1
       
        if(data[0]==command.signature and data[1]==command.opcode[10] and data[4]==command.doorID[1] and data[8]==command.fromnode[0]): #update RFID sensor
            pass
        if(data[0]==command.signature and data[1]==command.opcode[5]  and data[4]==command.doorID[1] and data[8]==command.fromnode[0]): #get magnetic sensor
            RES_SENSOR[4]=command.doorID[1]
            RES_SENSOR[1]=command.opcode[5]
            RES_SENSOR[6]=int(timeOut%256)
            RES_SENSOR[5]=int(timeOut/256)
            RES_SENSOR[7]=enableAlarm
            RES_SENSOR[8]=command.fromnode[1]
            ser.write(RES_SENSOR)
            ser.flush()
        if(data[0]==command.signature and data[1]==command.opcode[7]  and data[4]==command.doorID[1] and data[8]==command.fromnode[0]): #get infrared sensor
            RES_SENSOR[4]=command.doorID[1]
            RES_SENSOR[1]=command.opcode[7]
            RES_SENSOR[7]=speaker
            RES_SENSOR[8]=command.fromnode[1]
            ser.write(RES_SENSOR)
            ser.flush()
        
            
        




