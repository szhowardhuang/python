#! /usr/bin/env python
import os
import time
import urllib
import sys

def download(url):
    try:
        os.chdir('/home/howard/dmm')
    except:
        os.mkdir('/home/howard/dmm')
    
    firstfilename = url.split('/')[-1]   ## the last filename
    secondfilename = url.split('/')[-2]  ## the second name seperated by '/'
    rootend = url.find((secondfilename + '/' + firstfilename))
    rooturl = url[:rootend]
    value=int(firstfilename[3])*100 + int(firstfilename[4])*10 + int(firstfilename[5])
    start = value
    end = 850
    
    for i in range(start , end): ## from star to end-1
        temp = str(value//100) + str((value%100)//10) + str((value%100)%10)
        ## print temp
        secondname = secondfilename[:3] + temp 
        firstname = firstfilename[:3] + temp + firstfilename[6:]
        
        filename = rooturl + secondname + '/' + firstname
        print "downloading " + filename
        urllib.urlretrieve(filename,firstname)
        value += 1
        time.sleep(1)  # 1Sec

if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            download(sys.argv[1])
        except IOError:
            print 'Filename not found.'
    else:
        print 'usage: %s http://pics.server.com/mono/movie/abc001/abc001pl.jpg' % os.path.basename(sys.argv[0])
