import os
path="/home/howard/python"  # insert the path to the directory of interest here
dirList=os.listdir(path)
    
for filename in dirList:
    basename, extension = filename.split('.')
    if extension == 'py':
        print basename+'.py'
