#!/usr/bin/env python
import time
import serial
import sys
import io
import pygame
from pygame import mixer
import fileFinder
import os
import subprocess
import soundLibrary
import logging
from serialemulator import SerialEmulator
from multiprocessing import Pool, Lock

#wavFiles = fileFinder.findMatchingFiles('*.wav','./sounds/',True)
testSerPort = None
previousReading = None
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
        soundObj = soundlib.get(str(measValue))
        if soundObj == None:
            return
        mixer.fadeout(1000)
        start = time.time()
        mixer.Sound.play(soundlib.get(str(measValue)))
        while True:
            #time.sleep(.1)
            if mixer.get_busy() == False:
                #print("sound finished")
                break
        end = time.time()
        #print('time finished: ',end-start)
        ##time.sleep(3)
        
        ##pygame.mixer.Sound(soundlib.get(str(measValue)))
        ##for wavFile in wavFiles:
            ##wavfileName = os.path.splitext(wavFile)[0]
            ##print(wavfileName)
            ##if wavfileName== response:
            ##time.sleep(1)
        ##p1=subprocess.Popen(['aplay','-Dplug:pilotHeadset2','./sounds/0.wav'])
        ##p2=subprocess.Popen(['aplay','-d1','-Dplug:pilotHeadset2','piano2.wav'])
        ##p1.wait()
        ##p2.wait()
        ##time.sleep(.5)        
    else:
        print('invalid response: ', response)
    
def _readline(ser):
    eol=b'\r'
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
def main():
    try:
        ser = serial.Serial()
        ser.port='/dev/ttyAMA0'
        ser.baudrate=38400
        ser.parity=serial.PARITY_NONE
        ser.stopbits=serial.STOPBITS_ONE
        ser.bytesize=serial.EIGHTBITS
        ser.timeout=1
        ser.dsrdtr=False
        ser.open()
        ser.isOpen() 
        #ser = testSerPort      
        
	#ser.flushInput()
    except Exception as ex:
        print('Error has Occured opening port. exiting program..', ex.args )
        sys.exit(1)
    print('serialPort initialized')
    ser.flushInput()  # flush input buffer
    print('input buffer flushed.')
    #ser.write('F\r\n')  # stop the laser first.
    print('stopped the laser as a precaution.')
    time.sleep(.5)
    #ser.write(bytes(35))  # get the serial number
    print('getting laser serial number...')
    #start the textIOWrapper
    # ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser,1),
	#			newline='\n')
                #encoding='ascii')
				#line_buffering = True,
				#errors='ignore')
    #ser_io.write(u"F")
    #ser_io.write(u"#")
    #time.sleep(1)
    #id = ser_io.readline()
    #print('id=',id)
    while 1:
        try:
            #ser.write('Write counter: %d \n' %(counter))
            #time.sleep(.05)  # sleep waiting for response
            #resp2 = ser.read('\r')
            resp2 = _readline(ser)
            #print('resp2=',resp2)
            parse_response(resp2)
            ser.flushInput()
        except Exception as a:
            print('shutting down port. ',a)
            ser.close()
            break
    print('stopping program shutdown, exiting main.')
if __name__ == "__main__":
    soundlib = soundLibrary.load_sounds()
    main()
    print('program finishing, with no errors')
    sys.exit(0)
