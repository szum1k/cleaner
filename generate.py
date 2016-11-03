#!/usr/bin/python2.7

import os
import random
import datetime
import time

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

def make(path):
    os.mkdir(path)

if os.path.exists('test-file'):
    os.system('rm -rf test-file')
    make('test-file')
else:
    make('test-file')

for k in range(2000,2017):
    for i in range(1, 13):
        for j in range(1, 29):
            r = random.randint(1,4)
            #r = 2
            if r == 1:
                dirPath = str(j) + '.' + str(i) + '.' + str(k) + '.txt'
                touch('test-file/' + dirPath)
            if r == 2:
                dirPath = str(j) + '.' + str(i) + '.' + str(k)
                make('test-file/' + dirPath)
            if r == 3:
                dirPath = str(j) + '.' + str(i) + '.' + str(k) + '.tar.gz'
                touch('test-file/' + dirPath)
            if r == 4:
                dirPath = str(j) + '.' + str(i) + '.' + str(k) + '.tar.bz2'
                touch('test-file/' + dirPath)
            t = datetime.datetime(k, i, j)
            ts = time.mktime(t.timetuple())
            os.utime('test-file/' + dirPath,(ts,ts))