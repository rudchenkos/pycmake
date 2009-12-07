class MakefileContext:
    def __init__(self, makefile, cache):
        self.makefile = makefile
        self.cache = cache

    def setVariable(self, varName, varValue):
        self.makefile.setVariable(varName, varValue)

    def getVariable(self, varName):
        return self.makefile.getVariable(varName)

    def addTarget(self, target):
        self.makefile.addTarget(target)

    def lookupTarget(self, targetName):
        return self.makefile.lookupTarget(targetName)
