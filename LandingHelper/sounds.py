import json
import pygame
import os
import time
import fnmatch
from pathlib import Path

class SoundDAO():
    def __init__(self):
        id = None
        active = False
        checkgear = False
        file = None
        pygameObj = None

class Voice():
    def __init__(self,_config):
        self.config = None
        with open(_config,'r') as configFile:
            self.config = json.load(configFile)
        self.sound_library = {}
        #self.soundFiles = self.findMatchingFiles('*.wav',self.config['sounds']['path'],True)                
        pygame.mixer.init()
        #print(self.soundFiles)
        for soundcfg in self.config['sounds']['sound']:
            if soundcfg['active'] == True:
                soundfile=os.path.join(self.config['sounds']['path'],soundcfg['file'])
                soundfilePath = Path(soundfile)
                if soundfilePath.exists():
                    #sound = pygame.mixer.Sound(soundfile)
                    #soundfileName = os.path.splitext(os.path.basename(soundcfg['file']))[0]
                    #load json config and sound object into a dao
                    sounddao = SoundDAO()
                    sounddao.id = soundcfg['id']
                    sounddao.active = soundcfg['active']
                    sounddao.checkgear = soundcfg['checkgear']
                    sounddao.file = soundcfg['file']
                    sounddao.soundobject = pygame.mixer.Sound(soundfile)
                    self.sound_library[sounddao.id] = sounddao
                else:
                    print('file does not exist',soundfilePath)
            else:
                print('sound file not active',soundcfg['file'])
        return

    def findMatchingFiles(self,pattern, path, includeRoot):
        result = []
        for root, dirs, files in os.walk(path):
          for file in files:
             if fnmatch.fnmatch(file, pattern):
                    #fi = open(os.path.join(root,file), mode='r')
                   if includeRoot:
                        #result.append(fi)
                        #fi.close()
                        result.append(os.path.join(root,file))
                   else:
                      result.append(file)
        return result
    def findMatchingFilesWithoutExtension(pattern, path):
        result = []
        filesWithExtension = findMatchingFiles(pattern,path)
        for file in filesWithExtension:
            result.append(os.path.splitext(file)[0])
        return result
    def altitude(self,measurement):
        #measval = str(measurement).replace(" ","")
        altitudeSound = self.sound_library.get(str(measurement))
        if altitudeSound == None:
            print("sound not found, meas value:",measurement)
            return
        pygame.mixer.fadeout(1000)
        start = time.time()
        sounddao = None
        
        if self.config['sounds']['check_gear'] == measurement:
            sounddao = self.sound_library.get(self.config['sounds']['check_gear_sound_id'])
        else:
            sounddao = self.sound_library.get(str(measurement))
        pygame.mixer.Sound.play(sounddao.soundobject)
        while True:
            if pygame.mixer.get_busy() == False:
                print("sound finished")
                break
                end = time.time()   
            #else: 
                #
               # print('cannot play sound for %s, player is busy', measurement)
        return
if __name__ == "__main__":
    config = 'config.json'
    sound = Voice(config) 


