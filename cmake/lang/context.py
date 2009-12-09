from error import *
from ..target import Target

class MakefileContext:
    def __init__(self, makefile):
        self.makefile = makefile

    def getVariable(self, varName):
        return self.makefile.getVariable(varName)

    # Command dispatcher
    def run_cmd(self, cmd_name, cmd_args):
        # find the appropriate "cmd_" method in the self object
        for member in self.__class__.__dict__.keys():
            if member == 'cmd_' + cmd_name:
                return self.__class__.__dict__[member](self, cmd_args)
        raise UnknownCommandError(cmd_name)

    # Commands

    def cmd_set(self, cmd_args):
        if not cmd_args:
            raise InsufficientArgumentError('set')
        name = cmd_args[0]
        value = ''
        if len(cmd_args) > 1:
            value = cmd_args[1]

        cache = False
        type = 'STRING'
        if len(cmd_args) > 2:
            if cmd_args[2] == "CACHE":
                cache = True
                if len(cmd_args) > 3:
                    type = cmd_args[3]

        if cache:
            self.makefile.getCMake().getCache().setVariable(name, value, type=type)
        else:
            self.makefile.setVariable(name, value)

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

