#!/usr/bin/env python
import sys
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import time
import landingDataProvider
import sys
import io
import os
import subprocess
import sounds
import logging.config
import yaml
import json
import threading
import queue
import importlib #use this to import dataprovider classes that are specified in the config.
with open('logging.conf','r') as stream:
    log = yaml.load(stream)
logging.config.dictConfig(log)
logger = logging.getLogger('root')
dataProviderData = 0
previousReading = None
soundlib = None
#use a threshold so we're not 
#measurementValueThreshold = .5
class coreApp():
    def __init__(self,_config):
        with open(_config,'r') as configFile:
            config = json.load(configFile)
            logger.debug('config loaded')
        self.voice = sounds.Voice(_config) 
        logger.debug('sounds loaded')
        self.errQ = queue.Queue()
        self.dataQ = queue.Queue()
        self.sleepDurSec = config['sleep_duration']
        logger.debug("Sleep Duration (sec): %s",self.sleepDurSec)
        self.keepAlive = True
        self.stopRequest = threading.Event()
        self.dat = -1
        self.inputStarted = False
        dprovider = getattr(importlib.import_module(config["dataProviderModule"]),config["dataProviderClass"])
        self.dataProvider = dprovider(self.dataQ,self.errQ);
        logging.info("DataProvider loaded: %s", config["dataProviderClass"])
    def playSound(self,input_):
        global previousReading
        input = str(input_)
        measValue = input_
        if measValue == previousReading:
            return
        else:
            previousReading = measValue
            logging.debug('playing altimeter sound for meas value: %s', measValue)
            self.voice.altitude(measValue)
            logging.debug('altimeter sound finished.')
    def run(self):
        global dataProviderData
        dataIn = False
        self.connect()
        while not self.stopRequest.isSet():
            logging.debug('Pre-connect');
            if not self.isOpen():
                logging.debug('connection not opened, attempting to connect');
                self.connect()
            while self.keepAlive:

                #self.dat = self.dataProvider.read()
                dataProviderData = self.dataProvider.read()
                time.sleep(.1)
                print(dataProviderData)
                self.playSound(str(dataProviderData))
                #dataProviderData = self.dat
            #self.dataProvider.disconnect()
            logging.info('disconnecting')
            self.close()
            self.stopRequest.set()
        return
   # dataprovider
    def stopdataAquisition(self):
        print('stopping data aquisition')
        self.keepAlive = False
    def close(self):
        stopdataAquisition()
        self.dataProvider.disconnect()
    def connect(self):
        retryCount = 0
        if not self.dataProvider.connected:
            try:
                logging.info('Connecting to data provider');
                self.dataProvider.connect()
            except Exception as ex:
                logging.exception();
        return True
    def isOpen(self):
        print('checking dataprovider is open',self.dataProvider.isOpen())
        return self.dataProvider.isOpen()
       # return False
if __name__ == "__main__":
    config = 'config.json'
    
    app = coreApp(config)
    t = threading.Thread(target=app.run)
    t.start()
    t.join()
    print('program finishing, with no errors')
    sys.exit(0)
