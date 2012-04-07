#! /usr/bin/env python
import os
import time

while True:
    result = False
    f = os.popen('ps -u howard')
    data = [ eachLine.strip() for eachLine in f ]
    f.close()
    for eachLine in data:
        if eachLine.find('driver') != -1:
            result = True
            print eachLine
            break
    
    if(not result):
        os.chdir('/home/howard/fs2')
        os.system('driver config.fs &')
    time.sleep(30)