#!/usr/bin/env python
import sys
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import time
#import landingDataProvider

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
import sounds
import logging
import json
import threading
import queue
import importlib #use this to import dataprovider classes that are specified in the config.
logging.getLogger(__name__).addHandler(logging.NullHandler())
dataProviderData = 0
previousReading = None
soundlib = None
#use a threshold so we're not 
#measurementValueThreshold = .5
class coreApp():
    def __init__(self,_config):
        with open(_config,'r') as configFile:
            config = json.load(configFile)
        global soundlib
        soundlib = soundLibrary.load_sounds()
        self.errQ = queue.Queue()
        self.dataQ = queue.Queue()
        self.sleepDurSec = config['data_providers']['sleep_duration']
        self.keepAlive = True
        self.stopRequest = threading.Event()
        self.dat = None
        self.inputStarted = False
        self.retryMax = 10
        self.dataProvider = landingDataProviderEmulator.LandingDataProviderEmulator(self.dataQ,self.errQ)

    def playSound(self,input_):
        global soundlib
        global previousReading
        input = str(input_)
        measValue = int(float(input))
        if measValue == previousReading:
            return
        else:
            previousReading = measValue
            altitudeSound = soundlib.get(str(measValue))
            if altitudeSound == None:
                print("sound not found, meas value:",measValue)
                return
            pygame.mixer.fadeout(1000)
            start = time.time()
            pygame.mixer.Sound.play(soundlib.get(str(measValue)))
            while True:
                #time.sleep(.1)
                if pygame.mixer.get_busy() == False:
                    print("sound finished")
                    break
                    end = time.time()   
                else: 
                    print('invalid response: ', input)
    def run(self):
        global dataProviderData
        dataIn = False
        while not self.stopRequest.isSet():
            if not self.isOpen():
                self.connect()
            while self.keepAlive:
                self.dat = self.dataProvider.read()
                #self.dataQ.put(dat)
                #time.sleep(1)
                print(self.dat)
                self.playSound(str(dataProviderData)+'ft')
                dataProviderData = self.dat
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
        if not self.dataProvider.connected:
            try:
                self.dataProvider.connect()
            except Exception:
                print('error connecting')
        return True
    def isOpen(self):
        return self.dataProvider.isOpen()
       # return False
if __name__ == "__main__":
    config = 'C:/Users/Aaron/Source/Repos/LandingHelper/LandingHelper/config.json'
    voice = sounds.Voice(config) 
    soundlib = soundLibrary.load_sounds()
    app = coreApp(config)
    t = threading.Thread(target=app.run)
    t.start()
    t.join()
    print('program finishing, with no errors')
    sys.exit(0)
