# encoding: UTF-8
import os
import shutil
import os.path
import stat
rootdir="/home/howard"
import os
MOV_FILES=[]
for root, dirs, files in os.walk(rootdir):
    for file in files:
        if(file.split(".")[-1].upper() == 'AVI'):
            path = root+os.sep+file+'\n'
            MOV_FILES.append(os.path.join(root, file))

#print MOV_FILES
for movname in MOV_FILES:
    photoname = movname.rstrip('avi')+'jpg'
    if(os.path.exists(photoname)):
        print movname,'   ',photoname
