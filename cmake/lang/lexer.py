class Token:
    def __init__(self, type, value=''):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, file, variableProvider=None):
        self.buffer = ''
        self.file = file
        self.variableProvider = variableProvider

    def getChar(self):
        if len(self.buffer) > 0:
            result = self.buffer[0]
            self.buffer = self.buffer[1:]
        else:
            result = self.file.read(1)
        return result

    def putBack(self, str):
        self.buffer = str + self.buffer

    def getToken(self):
        token = None

        while token == None:
            c = self.getChar()

            if len(c) == 0:
                token = Token('EOF')
            elif c == '#':
                self.skipComment()
            elif c.isspace():
                continue;
            elif c in '()':
                token = Token(c)
            elif c == '$' and self.variableProvider != None:
                self.substituteVariable()
            elif Lexer.isStringChar(c):
                self.putBack(c)
                token = self.getString()
            else:
                print "Invalid token: " + c
        return token

    @staticmethod
    def isStringChar(c):
        if c in '()':
            return False
        return not c.isspace()

    def skipComment(self):
        c = ''
        while c != '\n' and c != 'EOF':
            c = self.getChar()

    def getString(self):
        value = ''
        token = None
        quoted = False

        while token == None:
            c = self.getChar()

            if len(c) == 0:
                token = Token('STRING', value)
            elif c == '"':
                if len(value) == 0:
                    quoted = True
                else:
                    token = Token('STRING', value)
            elif c.isspace() and quoted:
                value = value + c
            elif c == '$' and self.variableProvider != None:
                self.substituteVariable()
            elif not Lexer.isStringChar(c):
                self.putBack(c)
                token = Token('STRING', value)
            else:
                value = value + c
        return token

    def substituteVariable(self):
        if self.getChar() != '{':
            return

        token = None
        varName = ''
        while token == None:
            c = self.getChar()

            if c == '}':
                varValue = self.variableProvider.getVariable(varName)
                self.putBack(varValue)
                break
            elif c.isalnum():
                varName = varName + c
            else:
                return

