
class LanguageError(Exception):
    def __init__(self, *args, **kwargs):
        try:
            self.line = kwargs['line']
        except KeyError:
            self.line = 0

        try:
            self.file = kwargs['file']
        except KeyError:
            self.file= 0

        self.args = args

    def setLine(self, line):
        self.line = line

    def getLine(self):
        return self.line

    def setFile(self, file):
        self.file = file

    def getFile(self):
        return self.file

    def __str__(self):
        return self.args[0]

class UnexpectedTokenError(LanguageError):
    def __str__(self):
        return "Unexpected token: '%s' ('%s' was expected)" % (self.args[0], self.args[1])

class InvalidCharacterError(LanguageError):
    def __str__(self):
        return "Invalid character: '%s'" % self.args[0]

class UnknownCommandError(LanguageError):
    def __str__(self):
        return "Unknown command: '%s'" % self.args[0]

class ArgumentError(LanguageError):
    def __str__(self):
        return "Incorrect arguments for '%s'" % self.args[0]

class InsufficientArgumentError(ArgumentError):
    def __str__(self):
        return "Insufficient arguments for '%s'" % self.args[0]

