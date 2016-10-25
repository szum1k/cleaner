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

# pobranie aktualnej daty
now = datetime.datetime.now()

# wprowadzone parametry i ustawianie wartosci domyslnych gdy ich brak
praser = argparse.ArgumentParser()

praser.add_argument('-e', '--extension', help='Poddaj rozszerzenie do ktorego chcesz ograniczyc dzialanie CLENER\'a.',default='')
praser.add_argument('-s', '--separator', help='Podaj po ilu miesiacach backup ma byc bardziej ograniczony.',default=5)
praser.add_argument('-o', '--old', help='Podaj dzien miesiaca, ktory bedzie przechowywany po roku czasu', default=5)
praser.add_argument('-a', '--after', help='Podaj dni miesiaca (rodzielajac je przecinkami), z ktorych backup ma zostac w wersji bardziej ograniczonej.', default='5,15,25')
praser.add_argument('-b', '--before', help='Podaj dni miesiaca (rodzielajac je przecinkami), z ktorych backup ma zostac w wersji mniej ograniczonej.', default='5,10,15,20,25,30')
praser.add_argument('-x', '--excluded', help='Podaj pliki/foldery (oddzielajac je przecinkami), ktore maja zostac pominiete.', default='')
praser.add_argument('-r', '--regexp', help='Wyrazenie regularne, ktorego pozytywne wyniki beda pomijane.', default='\Zx\A')
praser.add_argument('-d', '--dir', help='Ograniczenie pracy CLEANER\'a do jednego podfolderu (bez / (slash) na koncu).', default='test-file')

argResult = praser.parse_args()

# przypisanie wartosci argumentow do zmiennych
EXT = '[\w\-\.\:\ \,]*' + argResult.extension + '$'
if argResult.excluded == '':
    EXC = ['old']
else:
    tmp = 'old,' + argResult.excluded
    EXC = tmp.split(',')
SEP = int(argResult.separator)
AFT = map(int, argResult.after.split(','))
BEF = map(int, argResult.before.split(','))
RGX = argResult.regexp
DIR = argResult.dir + '/'
OLD = argResult.old

print EXT
print EXC
print SEP
print AFT
print BEF
print RGX
print DIR
print OLD

#sys.exit(1)

# tworzenie struktury folderow na starsze backupy
if not os.path.exists('test-file/old'):
    os.mkdir('test-file/old')

# foldery roczne
for i in range(1992,int(now.strftime("%Y"))):
    if not os.path.exists(DIR + 'old/' + str(i)):
        os.mkdir(DIR + 'old/' + str(i))
        print 'Utworzono ' + DIR + 'old/' + str(i)
    else:
        print 'Folder ' + DIR + 'old/' + str(i) + ' istnieje'

# uzyskanie listy plikow\folderow w folderze
dirList = os.listdir('test-file')

# dzialania dla kazdego pliku\folderu w liscie plikow
for file in dirList:

    # pominiecie plikow\folderow z excluded lub regexp
    if (file in EXC) or re.search(RGX, file):
        print 'Pomijam plik\\folder - ' + DIR + str(file)
    else:

        # sprawdzenie rozszerzenia
        if re.search(EXT, file):

            dirPath = DIR + file
            # przeforamtowanie daty na bardziej ludzki
            d = datetime.datetime.strptime(time.ctime(creation_date(dirPath)), "%a %b %d %H:%M:%S %Y")

            #starsze niz rok zostawiany tylko z 5 i przenoszony do folderu old
            if int(d.strftime("%Y")) < int(now.strftime("%Y")):
                if int(d.strftime("%d")) == OLD:
                    #shutil.move(file, DIR + '/old/' + d.strftime("%Y") + '/')
                    os.system('mv ' + DIR + file + ' ' + DIR + '/old/' + d.strftime("%Y") + '/')
                    print 'Przenosze \'' + file + '\' do ' + DIR + '/old/' + d.strftime("%Y")
                if int(d.strftime("%d")) != OLD:
                    #shutil.rmtree(DIR + file)
                    print 'Usuwam \'' + file + '\''
                    os.system('rm -rf ' + DIR + file)

            #do roku czasu
            if int(d.strftime("%Y")) == int(now.strftime("%Y")):

                #starsze niz 5 miechow (5, 15, 25)
                if int(d.strftime("%m")) < (int(now.strftime("%m")) - SEP + 1):
                    if int(d.strftime("%d")) in AFT:
                        print 'Backup starszy niz 5 miesiecy - ' + DIR + file + ' - zostawiam'
                    else:
                        print 'Backup starszy niz 5 miesiecy - ' + DIR + file + ' - usuwam'
                        #shutil.rmtree(DIR + file)
                        os.system('rm -rf ' + DIR + file)
                else:

                    #starsze niz 1 miech (5, 10, 15, 20, 25, 30)
                    if int(d.strftime("%m")) < int(now.strftime("%m")):
                        if int(d.strftime("%d")) in BEF:
                            print 'Backup starszy niz 1 miesiac: ' + DIR + file + ' - zostawiam'
                        else:
                            print 'Backup starszy niz 1 miesiac: ' + DIR + file + ' - usuwam'
                            #shutil.rmtree(DIR + file)
                            os.system('rm -rf ' + DIR + file)
                    if int(d.strftime("%m")) == int(now.strftime("%m")):
                        print 'Backup z tego miesiaca: ' + DIR + file + ' - zostawiam'
                #usuniecie bledow generowanie pliki po dacie
                if int((d.strftime("%m")) > int(now.strftime("%m"))) and ((d.strftime("%Y")) == int(now.strftime("%Y"))):
                    os.system('rm -rf test-file/' + file)

        else:
            print 'Plik\Folder nie pasuje do kryteriow - ' + file

print 'Czyszczenie backup\'ow zakonczone'
sys.exit(0)