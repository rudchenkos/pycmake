#!/usr/bin/python
import os
import sys
from cmake import CMake

if len(sys.argv) < 2:
    print "usage: pycmake <srcdir>"
    sys.exit(0)

cmake = CMake(sys.argv[1], '.')
cmake.generate()
