from lexer import Lexer
from ..makefile import Makefile

class ParserError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class LanguageError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

def cmd_set(context, cmd_args):
    if not cmd_args:
        raise LanguageError('The "set" command needs at least one argument')
    value = ''
    if len(cmd_args) > 1:
        value = cmd_args[1]
    context.setVariable(cmd_args[0], value)

def cmd_message(makefile, cmd_args):
    for arg in cmd_args:
        print arg,
    print

def run_cmd(makefile, cmd_name, cmd_args):
    cmd_name = cmd_name.lower()
    if cmd_name == 'set':
        cmd_set(makefile, cmd_args)
    elif cmd_name == 'message':
        cmd_message(makefile, cmd_args)
    else:
        raise LanguageError('Unknown command: ' + cmd_name)

def parse(filename, context):
    file = open(filename, 'r')

    lexer = Lexer(file, context)
    token = lexer.getToken()

    try:
        while token.type != 'EOF':
            if token.type != 'STRING':
                raise ParserError('command name was expected')
            cmd_name = token.value
            token = lexer.getToken()
            if token.type != '(':
                raise ParserError('\'(\' was expected')

            cmd_args = []
            token = lexer.getToken()
            while token.type != ')':
                if token.type != 'STRING':
                    raise ParserError('string was expected')
                cmd_args.append(token.value)
                token = lexer.getToken()

            run_cmd(context, cmd_name, cmd_args)
            token = lexer.getToken()
    finally:
        file.close()
