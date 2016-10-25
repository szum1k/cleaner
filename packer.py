#!/usr/bin/python2.7

import os
import platform
import time
import datetime
import sys
import re
import argparse
import shutil

def creation_date(path_to_file):
    """
    Proba wyciagniecia daty utworzenia pliku. Brak w Linux, wyciagniecie daty ostatniej modyfikacji
    http://stackoverflow.com/a/39501288/1709587
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        return stat.st_mtime

DIR = 'test-file2/'

# pobranie aktualnej daty
now = datetime.datetime.now()

# uzyskanie listy plikow\folderow w folderze
dirList = os.listdir(DIR)

# dzialania dla kazdego pliku\folderu w liscie plikow
for file in dirList:

    dirPath = DIR + file
    # przeforamtowanie daty na bardziej ludzki
    d = datetime.datetime.strptime(time.ctime(creation_date(dirPath)), "%a %b %d %H:%M:%S %Y")

    if (int(d.strftime("%m")) == int(now.strftime("%m"))) and (int(d.strftime("%d")) < int(now.strftime("%d"))):
        os.system('tar -cvf ' + DIR + file + '.tar ' + DIR + file)
print 'Pakowanie backup\'ow zakonczone'
sys.exit(0)