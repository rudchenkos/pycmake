from lexer import Lexer
from ..target import Target
from error import *

def cmd_set(context, cmd_args):
    if not cmd_args:
        raise InsufficientArgumentError('set')
    value = ''
    if len(cmd_args) > 1:
        value = cmd_args[1]
    context.setVariable(cmd_args[0], value)

def cmd_message(context, cmd_args):
    for arg in cmd_args:
        print arg,
    print

def cmd_add_executable(context, cmd_args):
    if not cmd_args:
        raise InsufficientArgumentError('add_executable')
    target = Target(cmd_args[0], 'EXECUTABLE')
    for src in cmd_args[1:]:
        target.addSource(src)
    context.addTarget(target)

def run_cmd(makefile, cmd_name, cmd_args):
    cmd_name = cmd_name.lower()
    if cmd_name == 'set':
        cmd_set(makefile, cmd_args)
    elif cmd_name == 'message':
        cmd_message(makefile, cmd_args)
    elif cmd_name == 'add_executable':
        cmd_add_executable(makefile, cmd_args)
    else:
        raise UnknownCommandError(cmd_name)

def parse(filename, context):
    file = open(filename, 'r')

    try:
        lexer = Lexer(file, context)
        token = lexer.getToken()

        while token.type != 'EOF':
            if token.type != 'STRING':
                raise UnexpectedTokenError(token.value, 'STRING', 'STRING', line=lexer.getLine())

            cmd_name = token.value
            token = lexer.getToken()
            if token.type != '(':
                raise UnexpectedTokenError(token.value, '(', 'STRING', line=lexer.getLine())

            cmd_args = []
            token = lexer.getToken()
            while token.type != ')':
                if token.type != 'STRING':
                    raise UnexpectedTokenError(token.value, 'STRING', line=lexer.getLine())
                cmd_args.append(token.value)
                token = lexer.getToken()

            run_cmd(context, cmd_name, cmd_args)
            token = lexer.getToken()
    except LanguageError as e:
        # set the appropriate filename and line number and re-raise
        e.setLine(lexer.getLine())
        e.setFile(filename)
        raise e
    finally:
        file.close()
