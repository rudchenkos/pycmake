
class Makefile:
    def __init__(self):
        self.variables = {}
        self.targets = []

    def setVariable(self, varName, varValue):
        if not varValue:
            try:
                del self.variables[varName]
            except KeyError:
                pass
        else:
            self.variables[varName] = varValue

    def getVariable(self, varName):
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
