#!/usr/bin/python
import os
import sys

from cmake.lang.parser import parse,LanguageError
from cmake.lang.context import MakefileContext
from cmake.makefile import Makefile
from cmake.cache import CacheManager

if len(sys.argv) < 2:
    print "usage: pycmake <srcdir>"
    sys.exit(0)

srcdir = sys.argv[1]

mk = Makefile()
cache = CacheManager()
cache.load('.')
context = MakefileContext(makefile=mk, cache=cache)

try:
    parse(os.path.join(srcdir, 'CMakeLists.txt'), context)
except LanguageError as e:
    print e.getFile() + ':' + str(e.getLine()) + ': error:',e

