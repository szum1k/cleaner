#!/usr/bin/python2.7

import sys
import re
import os
import getopt

print sys.argv

try:
    opts, args= getopt.getopt(sys.argv[1:], "a:b:c:", ["add=", "back=", "copy="])
except getopt.GetoptError:
    sys.exit(2)

print opts

for opt, arg in opts:

    print opt
    if opt in ('-a', '--add'):
        print arg
    if opt in ('-b', '--back'):
        print arg
    if opt in ('-c', '--copy'):
        print arg