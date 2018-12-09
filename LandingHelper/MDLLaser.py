import serial
import sys
import landingDataProvider
class MDLLaser(landingDataProvider.LandingDataProvider):
    readval = None
    ser = None
    def connect(self):
       global redval
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
        return True
    def reset(self):
        return True
    def send(self, data):
        return True
    def read(self):
        return readval
    def isOpen(self):
        return False
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

        