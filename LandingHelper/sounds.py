import json
import pygame
import os
import fnmatch
from pathlib import Path
class Voice():
    def __init__(self,_config):
        self.config = None
        with open(_config,'r') as configFile:
            self.config = json.load(configFile)
        self.sound_library = {}
        self.soundFiles = self.findMatchingFiles('*.wav',self.config['sounds']['path'],True)                
        pygame.mixer.init()
        for soundcfg in self.config['sounds']['sound']:
            if soundcfg['active'] == True:
                soundfile=os.path.join(self.config['sounds']['path'],soundcfg['file'])
                var = Path(soundfile)
                if var.exists():
                    sound = pygame.mixer.Sound(soundfile)
                    soundfileName = os.path.splitext(os.path.basename(soundcfg['file']))[0]
                    self.sound_library[soundfileName] = sound
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
if __name__ == "__main__":
    config = 'C:/Users/Aaron/Source/Repos/LandingHelper/LandingHelper/config.json'
    sound = Voice(config) 


