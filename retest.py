
import re
import os

convertFiles = []

def convertFile(inputFileUrl,outputFileUrl):
    inputFile=open(inputFileUrl)
    inputLines=inputFile.readlines()
    inputFile.close()
    outFile=open(outputFileUrl,'w')
    for eachLine in inputLines:
        m=re.match('.+PROT\((.+)\)',eachLine)
        if m is not None:
            eachLine=re.sub(' PROT\(.+\)',m.group(1),eachLine)
            outFile.write(eachLine)
            continue
        
        m=re.match('.+PROT1V\((.+)\)',eachLine)
        if m is not None:
            strReplace='('+m.group(1)+', ...'+')'
            eachLine=re.sub(' PROT1V\(.+\)',strReplace,eachLine)
            outFile.write(eachLine)
            continue
        
        m=re.match('.+PROT2V\((.+)\, (.+)\)',eachLine)
        if m is not None:
            strReplace='('+m.group(1)+', '+m.group(2)+', ...'+')'
            eachLine=re.sub(' PROT2V\(.+\)',strReplace,eachLine)
            outFile.write(eachLine)
            continue
        
        m=re.match('.+P1\((.+)\, (\w+)',eachLine)
        if m is not None:
            strReplace='('+m.group(1)+' '+m.group(2)+')'
            eachLine=re.sub(' P1\(.+\)',strReplace,eachLine)
            outFile.write(eachLine)
            continue
        
        m=re.match('.+P1V\((.+)\, (\w+)',eachLine)
        if m is not None:
            strReplace='('+m.group(1)+' '+m.group(2)+', ...'+')'
            eachLine=re.sub(' P1V\(.+\)',strReplace,eachLine)
            outFile.write(eachLine)
            continue
        
        m=re.match('.+P2\((.+)\, (\w+)\, (.+)\, (\w+)',eachLine)
        if m is not None:
            strReplace='('+m.group(1)+' '+m.group(2)+', '+m.group(3)+' '+m.group(4)+')'
            eachLine=re.sub(' P2\(.+\)',strReplace,eachLine)
            outFile.write(eachLine)
            continue
        
        m=re.match('.+P2V\((.+)\, (\w+)\, (.+)\, (\w+)',eachLine)
        if m is not None:
            strReplace='('+m.group(1)+' '+m.group(2)+', '+m.group(3)+' '+m.group(4)+', ...'+')'
            eachLine=re.sub(' P2V\(.+\)',strReplace,eachLine)
            outFile.write(eachLine)
            continue
        
        m=re.match('.+P3\((.+)\, (\w+)\, (.+)\, (\w+), (.+)\, (\w+)',eachLine)
        if m is not None:
            strReplace='('+m.group(1)+' '+m.group(2)+', '+m.group(3)+' '+m.group(4)+', '+m.group(5)+' '+m.group(6)+')'
            eachLine=re.sub(' P3\(.+\)',strReplace,eachLine)
            outFile.write(eachLine)
            continue
        
        m=re.match('.+P4\((.+)\, (\w+)\, (.+)\, (\w+), (.+)\, (\w+), (.+)\, (\w+)',eachLine)
        if m is not None:
            strReplace='('+m.group(1)+' '+m.group(2)+', '+m.group(3)+' '+m.group(4)+', '+m.group(5)+' '+m.group(6)+', '+m.group(7)+' '+m.group(8)+')'
            eachLine=re.sub(' P4\(.+\)',strReplace,eachLine)
            outFile.write(eachLine)
            continue
        
        m=re.match('.+P5\((.+)\, (\w+)\, (.+)\, (\w+), (.+)\, (\w+), (.+)\, (\w+), (.+)\, (\w+)',eachLine)
        if m is not None:
            strReplace='('+m.group(1)+' '+m.group(2)+', '+m.group(3)+' '+m.group(4)+', '+m.group(5)+' '+m.group(6)+', '+m.group(7)+' '+m.group(8)+', '+m.group(9)+' '+m.group(10)+')'
            eachLine=re.sub(' P5\(.+\)',strReplace,eachLine)
            outFile.write(eachLine)
            continue
        
        m=re.match('.+P6\((.+)\, (\w+)\, (.+)\, (\w+), (.+)\, (\w+), (.+)\, (\w+), (.+)\, (\w+), (.+)\, (\w+)',eachLine)
        if m is not None:
            strReplace='('+m.group(1)+' '+m.group(2)+', '+m.group(3)+' '+m.group(4)+', '+m.group(5)+' '+m.group(6)+', '+m.group(7)+' '+m.group(8)+', '+m.group(9)+' '+m.group(10)+', '+m.group(11)+' '+m.group(12)+')'
            eachLine=re.sub(' P6\(.+\)',strReplace,eachLine)
            outFile.write(eachLine)
            continue
        
        m=re.match('.+P7\((.+)\, (\w+)\, (.+)\, (\w+), (.+)\, (\w+), (.+)\, (\w+), (.+)\, (\w+), (.+)\, (\w+), (.+)\, (\w+)',eachLine)
        if m is not None:
            strReplace='('+m.group(1)+' '+m.group(2)+', '+m.group(3)+' '+m.group(4)+', '+m.group(5)+' '+m.group(6)+', '+m.group(7)+' '+m.group(8)+', '+m.group(9)+' '+m.group(10)+', '+m.group(11)+' '+m.group(12)+', '+m.group(13)+' '+m.group(14)+')'
            eachLine=re.sub(' P7\(.+\)',strReplace,eachLine)
            outFile.write(eachLine)
            continue
        
        outFile.write(eachLine)
    outFile.close()
    

def openFolder(folderUrl):
    for root, dirs, files in os.walk(folderUrl):
        for file in files:
            extension = file.split(".")[-1].upper()
            if(extension == 'C' or extension == 'H'):
                convertFiles.append(os.path.join(root, file))



if __name__ == '__main__':
    rootDir = '/home/howard/'
    os.system('cp -r /home/howard/mudos/ /home/howard/mudos1/')
    openFolder(rootDir+'mudos')
    for filename in convertFiles:
        convertFile(filename,rootDir+'mudos1/'+os.path.split(filename)[-1])