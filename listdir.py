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
for filename in MOV_FILES:
    print filename
