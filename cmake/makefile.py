
class Makefile:
    def __init__(self):
        self.variables = {}

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

