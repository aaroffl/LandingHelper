import os
import fileFinder
import pygame

sound_library = {}
wavFiles = fileFinder.findMatchingFiles('*.wav','./sounds/',True)
def load_sounds():
    pygame.mixer.init()
    global sound_library
    for wavFile in wavFiles:
        sound = sound_library.get(wavFile)
        if sound == None:
            #canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            sound = pygame.mixer.Sound(wavFile)
            wavFileNameOnly = os.path.splitext(os.path.basename(wavFile))[0]
            print('wavename: ',wavFileNameOnly)
            sound_library[wavFileNameOnly] = sound
    #print('soundlibraryContents: ',sound_library)
    return sound_library
    #pygame.mixer.quit()
def get_sound_by_name(name):
    global sound_library
    return sound_library.get(str(name))
    
            