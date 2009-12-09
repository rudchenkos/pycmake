import os
import sys
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

    def __str__(self):
        return self.value

class CacheManager:
    lineRegex = re.compile('([a-zA-Z_0-9]+):([a-zA-Z_0-9]+)=(.*)')

    def __init__(self, dir):
        self.entries = {}
        self.file = os.path.join(dir, "CMakeCache.txt")
        self.reload()

    def hasVariable(self, varName):
        return varName in self.entries

    def setVariable(self, varName, varValue, type='STRING', force=False):
        if not force and not self.hasVariable(varName):
            if not varValue:
                try:
                    del self.entries
                except KeyError:
                    pass
            else:
                entry = CacheEntry()
                entry.value = varValue
                entry.type = type
                self.entries[varName] = entry

    def getVariable(self, varName):
        try:
            return self.entries[varName].value;
        except KeyError:
            return ''

    def reload(self):
        self.entries.clear()
                
        if not os.path.exists(self.file):
            return
    
        if not os.path.isfile(self.file):
            return
        
        f = open(self.file)
        try:
            for line in f.readlines():
                match = CacheManager.lineRegex.match(line)
                if match:
                    entryName = match.group(1)
                    entry = CacheEntry()
                    entry.type = match.group(2)
                    entry.value = match.group(3)
                    self.entries[entryName] = entry
        finally:
            f.close()

    def save(self):
        # Do not write an empty file
        if len(self.entries) == 0:
            if os.path.exists(self.file) and os.path.isfile(self.file):
                sys.unlink(self.file)
            return

        f = open(self.file, 'w')
        try:
            for (k,v) in self.entries.items():
                f.write(k + ":" + v.type + "=" + v.value)
        finally:
            f.close()
        pass
