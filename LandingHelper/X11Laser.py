import landingDataProvider
from threading import Thread
import time
import serial
import queue
import os
import io
import sys
import re
last_received =0
class X11Laser(landingDataProvider.LandingDataProvider):
    readval = None
    ser = None
    regex = None
    def __init__(self,dataQ,errQ):
        super(X11Laser,self).__init__(dataQ,errQ)
        self.readval = 0
        self.dataQ = dataQ
        self.errQ = errQ
        self.connected = False;
        self.ser = serial.Serial('/dev/ttyUSB0',115200)
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.timeout = 1
        self.ser.dsrdtr = False
        self.regex = re.compile(r'[0-9]{1,3}[.][0-9]{1,3}[\s]{1}[m]{1}')
        Thread(target=self.receiving).start()
    def connect(self):
        #global last_received
        print('X11: connecting')
        try:
           #self.ser.Open()
           self.connected = self.ser.isOpen()
           print('X11: connected',self.connected)
        except Exception as ex:
           print('Error has Occured opening port. exiting program..', ex.args)
           sys.exit(1)
          
           self.ser.flushInput()  # flush input buffer
           print('input buffer flushed.')
        # while True:
           # last_received = self.ser.readline()
           # print(last_received)
           # s = self.ser.readline().split(b" ")
           # #print (str(s))
           # a = (s[3:4])
           # meas = float(a[0].decode('utf-8')) * 3.28084
           # #print(meas)
           # last_received = meas
        #self.receiving()
    def disconnect(self):
        return "disconnected"
    def reset(self):
        return "reset"
    def send(self, data):
        #log data
        return True
    def read(self):
        global last_received
        return last_received
    def receiving(self):
        global last_received
        while True:
            measInMeter = re.search(r'[0-9]{1,3}[.][0-9]{1,3}[\s]{1}[m]{1}',self.ser.readline().decode('utf-8'))
            meas = 0.0
            if a != None:
                meas = measInMeter.group(0).replace('m','')
            measRounded = (float(meas) * 3.28084)
            #print(c)
            last_received = int(measRounded)
            #s = self.ser.readline().split(b" ")
           # print(self.ser.readline().decode('utf-8'))
            #print(self.regex.match(self.ser.readline().decode('utf-8')))
            #print(s)
            self.ser.flushInput()
            # if len(s) > 4:
              # a = (s[3:4])
              # meas = float(a[0].decode('utf-8')) * 3.28084
              # #print(meas)
              # time.sleep(.5)
              # last_received = int(meas)
              #print(last_received)
        return
    def run(self):
        self.read()
        return
    def isOpen(self):
        return self.ser.isOpen()
    def increment(self,i):
        i += 1
        return i
    #def __init__(self):
    #    return
    def _readline(self,ser):
        eol = b'\r'
        leneol = len(eol)
        line = bytearray()
        # prev = None
        while True:
            c = ser.read(1)
            if c:
                line += c
                #prev = c
                if line[-leneol:] == eol:
                    break
            else:
                break
        #print(line)
        return bytes(line[:-1])
if __name__ == "__main__":
    errQ = queue.Queue()
    dataQ = queue.Queue()
    laser = X11Laser(dataQ,errQ)
    laser.connect()
    laser.receiving()
    sys.exit(0)