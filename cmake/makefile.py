
class Makefile:
    def __init__(self, cmake):
        self.cmake = cmake
        self.variables = {}
        self.targets = []

    def getCMake(self):
        return self.cmake

    def setVariable(self, varName, varValue):
        if self.cmake.getCache().hasVariable(varName):
            return;

        if not varValue:
            try:
                del self.variables[varName]
            except KeyError:
                pass
        else:
            self.variables[varName] = varValue

    def getVariable(self, varName):
        if self.cmake.getCache().hasVariable(varName):
            return self.cmake.getCache().getVariable(varName)

        try:
            return self.variables[varName]
        except KeyError:
            return ''

    def addTarget(self, target):
        self.targets.append(target)

    def lookupTarget(self, targetName):
        for t in self.targets:
            if t.getName() == targetName:
                return t
        return None
