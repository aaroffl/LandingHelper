import serial
import sys
import logging
import logging.config
import landingDataProvider
from threading import Thread
import time
class MDLLaser(landingDataProvider.LandingDataProvider):
    readval = None
    def __init__(self,dataQ,errQ):
        super(MDLLaser,self).__init__(dataQ,errQ)
        logging.config.fileConfig('logging.conf')
        logger = logging.getLogger('dataProvider');
        #global readval
        #self.readval = 0
        self.dataQ = dataQ
        self.errQ = errQ
        #readval = None
        Thread(target=self.receiving).start()
        self.connected = False;
        # self.ser = serial.Serial(
           # port = '/dev/ttyAMA0',
           # baudrate = 38400,
           # parity = serial.PARITY_NONE,
           # stopbits = serial.STOPBITS_ONE,
           # bytesize = serial.EIGHTBITS,
           # timeout = 1,
           # dsrdtr = False
           # #open()
           # #isOpen()
		# )

        self.connect()
   
    def disconnect(self):
        return True
    def reset(self):
        return True
    def send(self, data):
        return True
    def read(self):
        return readval
    def isOpen(self):
        return True
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
        print(c)
        return bytes(line[:-1])
    def receiving(self):
        global last_received
        global ser
        buffer = 1
        while True:
            last_received = ser.readline()
            buffer += 1
            last_received = last_received + bytes(1)
            time.sleep(.5)
            print('!!!!!!!!!!!!!!!!!!!!!!!!!'+str(last_received))
        return
    def connect(self):
       global ser
       try:
           ser = serial.Serial()
           ser.port = '/dev/ttyAMA0'
           ser.baudrate = 38400
           ser.parity = serial.PARITY_NONE
           ser.stopbits = serial.STOPBITS_ONE
           ser.bytesize = serial.EIGHTBITS
           ser.timeout = 1
           ser.dsrdtr = False
           ser.open()
           ser.isOpen()
           connected = True
           self.receiving()
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
             readval = self._readline(ser)
             print(readval)
             #print('resp2=',resp2)
             #parse_response(resp2)
             ser.flushInput()
         except Exception as a:
             print('shutting down port. ',a)
             ser.close()
             break