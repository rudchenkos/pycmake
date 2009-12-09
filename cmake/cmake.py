import os

from lang.parser import parse,LanguageError
from lang.context import MakefileContext
from makefile import Makefile
from cache import CacheManager

class CMake:
    def __init__(self, srcdir, bindir):
        self.srcdir = os.path.abspath(srcdir)
        self.bindir = os.path.abspath(bindir)
        self.cache = CacheManager(self.bindir)
        self.rootMakefile = Makefile(self)

    def generate(self):
        parsingContext = MakefileContext(self.rootMakefile)

        try:
            parse(os.path.join(self.srcdir, 'CMakeLists.txt'), parsingContext)
        except LanguageError as e:
            errfile = os.path.relpath(e.getFile(), self.srcdir) 
            print '%s:%d: error: %s' % (errfile, e.getLine(), e)

        self.cache.save()

    def getSourceDir(self):
        return self.srcdir

    def getBinaryDir(self):
        return self.bindir

    def getCache(self):
        return self.cache

    def getRootMakefile(self):
        return self.rootMakefile
