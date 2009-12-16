"""
Utility module for command argument parsing.

Command argument parsing takes significant part of source code for almost
every command implementation. This module provides a way to deal with command
args in easy and expressive form. See the ArgumentParser class.
"""

from error import ArgumentError

class RequiredParameter:
    """
    Can be either a named parameter with value or a keyword.
    Keywords are uppercase.
    """
    def __init__(self, name = ''):
        self.name = name

    def is_keyword(self):
        return self.name.isupper()

    def matches(self, raw_args):
        """Check whether this parameter can be parsed from the raw_args"""
        return not (self.is_keyword() and self.name != raw_args[0])

    def parse(self, raw_args, result):
        """Parse this parameter from the raw_args"""
        if self.is_keyword():
            if self.name == raw_args[0]:
                result[self.name] = True
            else:
                raise ArgumentException('keyword %s was expected' % required)
        else:
            result[self.name] = raw_args[0]
        return 1

class OptionalBlock:
    """Optional block of parameters"""
    def __init__(self):
        self.children = []

    def matches(self, raw_args):
        """Check whether this parameter can be parsed from the raw_args"""
        argn = 0
        for param in self.children:
            if isinstance(param, RequiredParameter):
                if argn >= len(raw_args) - 1:
                    return False
                while not param.matches(raw_args[argn:]):
                    argn += 1
                    if argn >= len(raw_args) - 1:
                        return False
        return True

    def parse(self, raw_args, values):
        """Parse this parameter from the raw_args"""
        argn = 0
        for param in self.children:
            if param.matches(raw_args[argn:]):
                argn += param.parse(raw_args[argn:], values)
            elif isinstance(param, RequiredParameter):
                raise ArgumentError("Invalid parameters")
        return argn

class AlternativesBlock:
    """List of parameters which can be parsed in any order"""
    def __init__(self):
        self.alternatives = []

    def matches(self, raw_args):
        """Check whether this parameter can be parsed from the raw_args"""
        for alternative in self.alternatives:
            if alternative.matches(raw_args):
                return True
        return False

    def parse(self, raw_args, values):
        """Parse this parameter from the raw_args"""
        for alternative in self.alternatives:
            if alternative.matches(raw_args):
                return alternative.parse(raw_args, values)
        return 0

class ParameterLexer:
    """
    Very simple parameter specification lexer
    Example spec data:
        "name value [CACHE [type]]"
    """
    def __init__(self, spec):
        self.spec = spec
        self.spec_ptr = 0
        self.cache = []
        
    def get_token(self):
        """
        Get the next token from the spec. It can be and alphanumeric
        word, '[' or ']'. Whitespaces are skipped.
        """
        if len(self.cache) > 0:
            token = self.cache[0]
            self.cache = self.cache[1:]
            return token

        value = []
        while True:
            c = self._get_next_char()
            if len(c) == 0:
                break
            elif c.isspace():
                if len(value) > 0:
                    break
                else:
                    continue # skip spaces
            elif c.isalnum() or c == '_':
                value.append(c)  
            elif c in '[]':
                if len(value) > 0:
                    self.put_token(c)
                    break
                else:
                    return c
            else:
                raise Exception("Invalid chatacter in parameter specification")
        return ''.join(value)

    def put_token(self, param):
        """Put a token to the fifo so that it will be returned from
           a subsequent get_token call"""
        self.cache.append(param)

    def _get_next_char(self):
        if self.spec_ptr < len(self.spec):
            c = self.spec[self.spec_ptr]
            self.spec_ptr += 1
            return c
        else:
            return ''

def __parseParameters(parameterLexer):
    params = []
    while True:
        token = parameterLexer.get_token()
        if not token:
            break
        elif token.isspace():
            continue
        elif token == '[':
            optionalBlock = OptionalBlock()
            optionalBlock.children = __parseParameters(parameterLexer)
            if isinstance(params[-1], AlternativesBlock):
                params[-1].alternatives.append(optionalBlock)
            elif isinstance(params[-1], OptionalBlock): # combine optional blocks
                alt = AlternativesBlock()
                alt.alternatives.append(params[-1])
                alt.alternatives.append(optionalBlock)
                params[-1] = alt
            else:
                params.append(optionalBlock)
        elif token == ']':
            break
        else:
            params.append(RequiredParameter(token))
    return params

def parseParameterSpec(spec):
    return __parseParameters(ParameterLexer(spec))

def matchParameters(spec, raw_args):
    params = parseParameterSpec(spec)
    argn = 0
    parsed = {}

    for parameter in params:
        if isinstance(parameter, RequiredParameter):
            argn += parameter.parse(raw_args[argn:], parsed)
        else:
            while parameter.matches(raw_args[argn:]):
                argn += parameter.parse(raw_args[argn:], parsed)

    return parsed
