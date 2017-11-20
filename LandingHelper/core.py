#!/usr/bin/env python
import time
import landingDataProvider
import landingDataProviderEmulator
import serial
import sys
import io
import pygame
import fileFinder
import os
import subprocess
import soundLibrary
import logging
import json
import threading
import queue
import importlib #use this to import dataprovider classes that are specified in the config.
logging.getLogger(__name__).addHandler(logging.NullHandler())
#use a threshold so we're not 
#measurementValueThreshold = .5
class coreApp(threading.Thread):
    def __init__(self):
       threading.Thread.__init__(self)
       self.errQ = queue.Queue()
       self.dataQ = queue.Queue()
       self.sleepDurSec = 5
       self.keepAlive = True
       self.stopRequest = threading.Event()
       self.dat = None
       self.inputStarted = False
       self.retryMax = 10
       self.dataProvider = landingDataProviderEmulator.LandingDataProviderEmulator(self.dataQ,self.errQ)
    def parse_response(input_):
        global previousReading
        response = str(input_)
        if response.endswith('ft'):
            #print('measurement: ', response)
            response = response[:-2]
            if response == '':
                measValue=0
            else:
                measValue = int(float(response))
            if measValue == previousReading:
                return
            else:
                previousReading = measValue
            #print ('meas value',measValue)
            #print(soundlib.get(str(measValue)))
            altitudeSound = soundlib.get(str(measValue))
            if altitudeSound == None:
            
                return
            pygame.mixer.fadeout(1000)
            start = time.time()
            pygame.mixer.Sound.play(soundlib.get(str(measValue)))
            while True:
                #time.sleep(.1)
                if pygame.mixer.get_busy() == False:
                    #print("sound finished")
                    break
            end = time.time()   
        else: 
            print('invalid response: ', response)
    def run(self):
        dataIn = False
        while not self.stopRequest.isSet():
            if not self.isOpen():
                self.connect()
            while self.keepAlive:
                self.dat = self.dataProvider.read()
                self.dataQ.put(dat)
                if not self.inputStarted:
                    print('reading')
                self.inputStarted = True
            #self.dataProvider.disconnect()
            self.close()
            self.stopRequest.set()
        return
   # dataprovider
    def stopdataAquisition(self):
        self.keepAlive = False
    def close(self):
        stopdataAquisition()
        self.dataProvider.disconnect()
    def connect(self):
        retryCount = 0
        if not self.dataProvider.isOpen():
            try:
                self.dataProvider.connect()
            except Exception:
                print('error connecting')
        self.dataProvider.connect()
        while self.dataProvider.read() == '' and retryCount < self.retryMax and self.keepAlive:
            retryCount += 1
            print('retrying again soon, no data.')
            time.sleep(.5)
        if retryCount >= retryMax:
            print ('max retries met or exceded.')
            self.close()
            return False
        return True
    def isOpen(self):
        return self.dataProvider.isOpen()
       # return False
if __name__ == "__main__":
    soundlib = soundLibrary.load_sounds()
    app = coreApp()
    app.start()
    print('program finishing, with no errors')
    sys.exit(0)
