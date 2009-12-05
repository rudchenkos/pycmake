import os
import re

class CacheEntry:       
    def __init__(self):
        self.value = ""
        self.type = ""
        self.properties = {}

    def getPoperty(self, propertyName):
        return ""

    def setProperty(self, propertyName, propertyValue):
        pass

    def appendProperty(self, propertyName, propertyValue):
        pass

class CacheManager:
    lineRegex = re.compile('([a-zA-Z_0-9]+):([a-zA-Z_0-9]+)=(.*)')

    def __init__(self):
        self.entries = {}

    def load(self, path):
        cacheFile = os.path.join(path, "CMakeCache.txt")
                
        if not os.path.exists(cacheFile):
            return False
    
        if not os.path.isfile(cacheFile):
            return False
        
        f = open(cacheFile)
        for line in f.readlines():
            match = CacheManager.lineRegex.match(line)
            if match:
                entryName = match.group(1)
                entry = CacheEntry()
                entry.type = match.group(2)
                entry.value = match.group(3)
                self.entries[entryName] = entry
                        
        f.close()
        return True

    def get(self, propName):
        return self.entries[propName];
