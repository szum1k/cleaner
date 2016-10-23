#!/usr/bin/python2.7

import sys
import re
import os

dirList = os.listdir('test-file')

pattern = '[\w\-\.\: ]$'

for file in dirList:

    if re.search(pattern, file):
        print file