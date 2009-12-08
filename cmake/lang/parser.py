from lexer import Lexer
from error import LanguageError, UnexpectedTokenError

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

            context.run_cmd(cmd_name, cmd_args)
            token = lexer.getToken()
    except LanguageError as e:
        # fixup filename and line number if needed and re-raise
        if not e.getLine(): e.setLine(lexer.getLine())
        if not e.getFile(): e.setFile(filename)
        raise e
    finally:
        file.close()
