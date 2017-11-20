import landingDataProvider
import time
from threading import Thread, Condition
class LandingDataProviderEmulator(landingDataProvider.LandingDataProvider, Thread):
    def __init__(self,dataQ,errQ):
        super(LandingDataProviderEmulator,self).__init__(dataQ,errQ)
        self.readval = 0
        self.dataQ = dataQ
        self.errQ = errQ
        self.condition = Condition()
    def connect(self):
        num = range(5)
        while True:
            self.condition.acquire()
            if len(self.dataQ) == 10:
                print ("queue full")
        return "connected"
    def disconnect(self):
        return "disconnected"
    def reset(self):
        return "reset"
    def send(self, data):
		#log data
        return True
    def read(self):
        while True:
            self.readval +=1
            time.sleep(0.01)
            if self.readval is 10:
                self.readval = 0
        return
    def isOpen(self):
        return True
    def increment(self,i):
        i += 1
        return i
    #def __init__(self):
    #    return
