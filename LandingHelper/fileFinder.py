import time
import serial
import io
import sys
import re
import os.path
import fnmatch

def main(argv):
	#see if value is a decimal
    non_decimal = re.compile(r'[^\d]+')
    numberToFind = non_decimal.sub('', argv)
    if numberToFind == 0:
        findSoundFile(0)

def findMatchingFiles(pattern, path, includeRoot):
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
	main(sys.argv)