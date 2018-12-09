import landingDataProvider
from threading import Thread
import time
import serial
import queue
import os
import io
import sys
last_received =0
class X11Laser(landingDataProvider.LandingDataProvider):
    readval = None
    ser = None
    def __init__(self,dataQ,errQ):
        super(X11Laser,self).__init__(dataQ,errQ)
        self.readval = 0
        self.dataQ = dataQ
        self.errQ = errQ
        self.connected = False;
        Thread(target=self.receiving).start()
        #self.receiving()
       # self.condition = Condition()
    def connect(self):
       global readval
       ser = None
       try:
           ser = serial.Serial()
           ser.port = 'COM3'
           ser.baudrate = 11500
           ser.parity = serial.PARITY_NONE
           ser.stopbits = serial.STOPBITS_ONE
           ser.bytesize = serial.EIGHTBITS
           ser.timeout = 1
           ser.dsrdtr = False
           ser.open()
           ser.isOpen()
       except Exception as ex:
           print('Error has Occured opening port. exiting program..', ex.args)
           sys.exit(1)
           ser.flushInput()  # flush input buffer
           print('input buffer flushed.')
       while 1:
         try:
             #ser.write('Write counter: %d \n' %(counter))
             #time.sleep(.05) # sleep waiting for response
             #resp2 = ser.read('\r')
             readval = _readline(ser)
             #print('resp2=',resp2)
             #parse_response(resp2)
             ser.flushInput()
         except Exception as a:
             print('shutting down port. ',a)
             ser.close()
             break
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
        buffer = 1
        while True:
            last_received = ser.readline()
            buffer += 1
            last_received = last_received +1
            time.sleep(.5)
            print('!!!!!!!!!!!!!!!!!!!!!!!!!'+str(last_received))
        return
    def run(self):
        self.read()
        return
    def isOpen(self):
        return False
    def increment(self,i):
        i += 1
        return i
    #def __init__(self):
    #    return
    def _readline(ser):
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
    sys.exit(0)