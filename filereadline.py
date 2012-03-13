#!/usr/bin/env python

import os

filename=raw_input('input file name: ')
filename=os.getcwd()+os.sep+filename
f=open(filename,'r')
print f.name, f.encoding
print os.path.splitext(filename)
print os.path.dirname(filename)
for line in f:
    print line,
f.close()

