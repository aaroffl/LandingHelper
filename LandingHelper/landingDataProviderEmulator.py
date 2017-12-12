import landingDataProvider
from threading import Thread
import time
last_received =0
class LandingDataProviderEmulator(landingDataProvider.LandingDataProvider):
    def __init__(self,dataQ,errQ):
        super(LandingDataProviderEmulator,self).__init__(dataQ,errQ)
        self.readval = 0
        self.dataQ = dataQ
        self.errQ = errQ
        self.connected = False;
        Thread(target=self.receiving).start()
        #self.receiving()
       # self.condition = Condition()
    def connect(self):
        time.sleep(2)
        connected = True
        return
    def disconnect(self):
        return "disconnected"
    def reset(self):
        return "reset"
    def send(self, data):
		#log data
        return True
    def read(self):
        global last_received
        #while True:
        #    self.readval +=1
        #    time.sleep(0.01)
        #    if self.readval is 10:
        #        self.readval = 0
        return last_received
    def receiving(self):
        global last_received
        buffer = 1
        while True:
            # last_received = ser.readline()
            buffer += 1
            last_received = last_received +1
            time.sleep(.5)
            print('!!!!!!!!!!!!!!!!!!!!!!!!!'+str(last_received))
            if buffer is 10:
                last_received=1
                buffer = 1
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
