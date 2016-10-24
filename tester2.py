#!/usr/bin/python2.7

import argparse

class dupa(argparse.Action):
    print 'dupa'

praser = argparse.ArgumentParser()

praser.add_argument('-n', '--nap', help='n - n', action='dupa')
praser.add_argument('-m', '--map', help='m - m')
resault = praser.parse_args()

print 'jest n'