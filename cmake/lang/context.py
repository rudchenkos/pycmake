from error import *
from ..target import Target
from argparser import matchParameters

class MakefileContext:
    """CMake Makefile object builder"""
    def __init__(self, makefile):
        self.makefile = makefile

    def getVariable(self, varName):
        return self.makefile.getVariable(varName)

    def run_cmd(self, cmd_name, cmd_args):
        """
        Command dispatcher
        Find the appropriate "cmd_" method in the self object and call it
        """
        for member in self.__class__.__dict__.keys():
            if member == 'cmd_' + cmd_name:
                return self.__class__.__dict__[member](self, cmd_args)
        raise UnknownCommandError(cmd_name)

    # Commands

    def cmd_set(self, cmd_args):
        args = matchParameters('name value [CACHE type]', cmd_args)
        if 'CACHE' in args:
            try:
                type = args['type']
            except KeyError:
                type = 'STRING'
            self.makefile.getCMake().getCache().setVariable(args['name'], args['value'], type=type)
        else:
            self.makefile.setVariable(args['name'], args['value'])

    def cmd_message(self, cmd_args):
        for arg in cmd_args:
            print arg,
        print

    def cmd_add_executable(self, cmd_args):
        if not cmd_args:
            raise InsufficientArgumentError('add_executable')
        target = Target(cmd_args[0], 'EXECUTABLE')
        for src in cmd_args[1:]:
            target.addSource(src)
        self.makefile.addTarget(target)

