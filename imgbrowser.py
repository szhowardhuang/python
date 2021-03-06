﻿#!/usr/bin/python
#coding=utf-8 

from tkinter import *
import glob, os
from PIL import Image, ImageTk
import tkinter.filedialog
import shutil
import stat
import time
import string

class ImgBrowser(Frame):
    IMG_W = 240; IMG_H = 160
    IMG_X=250; IMG_Y=210; IMG_NUM_ON_ROW=5
    
    def __init__(self, master):
        frame=Frame.__init__(self, master)
        self.canvPanelWidth = master.winfo_screenwidth()
        self.canvPanelHeight = master.winfo_screenheight()-150 ## height will dynamic modify by content
        self.IMG_FILES=[]
        self.pack(expand=YES, fill=BOTH)
        self.makeCanvas()
        self.showAllImage()

      
      
    def makeCanvas(self):
        canv = Canvas(self, bg='brown', relief=SUNKEN)
        canv.config(width= self.canvPanelWidth, height= self.canvPanelHeight)                
        canv.config(scrollregion=( 0, 0, self.canvPanelWidth, self.canvPanelHeight ))         
        canv.config(highlightthickness=0)                 

        sbar = Scrollbar(self)
        sbar.config(command=canv.yview)                   
        canv.config(yscrollcommand=sbar.set)              
        sbar.pack(side=RIGHT, fill=Y)                     
        canv.pack(side=LEFT, expand=YES, fill=BOTH)
        self.canvas = canv
    
    
    def isPhotoFile(self,file):
        imgExtension = file.split(".")[-1].upper()
        if(imgExtension == 'PNG' or imgExtension =='JPG'):
            return True
        else:
            return False
        
    def isPngFile(self,file):
        imgExtension = file.split(".")[-1].upper()
        if(imgExtension == 'PNG'):
            return True
        else:
            return False
        
    def isJpgFile(self,file):
        imgExtension = file.split(".")[-1].upper()
        if(imgExtension == 'JPG'):
            return True
        else:
            return False
        
    def initShowAllImage(self):
        IMG_FILES=[]
        rootdir = filedialog.askdirectory()
        for root, dirs, files in os.walk(rootdir):
            for file in files:
                if(self.isPhotoFile(file)):
                    fileURL = os.path.join(root, file)
                    if (not os.path.islink(fileURL)):
                        IMG_FILES.append(fileURL)
        return IMG_FILES
    
    def convertFilename(self,src):
        isUnicode = False
        if(isinstance(src, unicode)):
            isUnicode = True
            src.encode('GBK') ## encode to GBK for chinses handler
            print("unicode")
        dest = []
        for i in range(len(src)):
            if src[i] == ' ' or src[i] == '(' or src[i] == ')' or src[i] == '-' \
                or src[i] == '&' or src[i] == '\'' or src[i] == '[' or src[i] == ']':
                dest += '\\'
            dest += src[i]
        if isUnicode:
            return ''.join(dest).encode('utf-8') ## encode to utf-8
        else:
            return ''.join(dest)    
    
    def openFileByDefaultApplication(self, file):
        if os.name == "nt":
            os.system(file)
        elif os.name == "posix":
            if os.uname()[0] == "Linux":
                os.system("/usr/bin/xdg-open " + self.convertFilename(file))
            elif os.uname()[0] == "Darwin":
                os.system("open "+file)
            print(os.uname()[0])
    
    def onDoubleClick(self, event):
        raw = int(self.canvas.canvasx(event.x) // self.IMG_X)
        collum = int(self.canvas.canvasy(event.y) // self.IMG_Y)
        imgFile=self.IMG_FILES[raw+self.IMG_NUM_ON_ROW*collum]
        if(os.path.exists(imgFile)):
            self.openFileByDefaultApplication(imgFile)  
        else: ## open folder,then user can modify image name by manual
            self.openFileByDefaultApplication(os.path.split(imgFile)[0])

    
    def showAllImage(self):
        self.IMG_FILES = self.initShowAllImage()
        self.showImage()        
        
    def showImage(self):
        dimension = [0,0]
        IMG_FILES = self.IMG_FILES         
        self.photo = list(range(len(IMG_FILES)))
        self.canvas.delete('all')
        fileNumbers = len(IMG_FILES)
        self.canvPanelHeight = (fileNumbers//self.IMG_NUM_ON_ROW + 1)*self.IMG_Y
        self.canvas.config(scrollregion=(0,0, self.canvPanelWidth, self.canvPanelHeight))
        for k, photoname in enumerate(IMG_FILES):
            if(os.path.exists(photoname)):
                ## print photoname
                if self.isPngFile(photoname):
                    dimension = self.getPngFileDimension(photoname)
                if self.isJpgFile(photoname):
                    dimension = self.getJpgFileDimension(photoname)
                try:
                    img = Image.open(photoname)
                    img.thumbnail((self.IMG_W, self.IMG_H))
                    self.photo[k] = ImageTk.PhotoImage(img)
                    self.canvas.create_image(self.IMG_X*(k%self.IMG_NUM_ON_ROW),\
                                            k//self.IMG_NUM_ON_ROW*self.IMG_Y,\
                                            image=self.photo[k], anchor="nw")
                except:
                    pass

                
            img_sname=photoname.split(os.sep)[-1]
            ## print(mov_sname)
            self.canvas.create_text(self.IMG_X*(k%self.IMG_NUM_ON_ROW)+self.IMG_W/3,\
                                    k//self.IMG_NUM_ON_ROW*self.IMG_Y+self.IMG_H+20, \
                                    text=img_sname, fill='beige', width=self.IMG_W)
            imgDimension = str(dimension[0]) + ' x ' + str(dimension[1])
            self.canvas.create_text(self.IMG_X*(k%self.IMG_NUM_ON_ROW)+self.IMG_W/3,\
                                    k//self.IMG_NUM_ON_ROW*self.IMG_Y+self.IMG_H+30, \
                                    text=imgDimension, fill='beige', width=self.IMG_W)                        
        
        self.canvas.bind('<Double-1>', self.onDoubleClick)       # set event handler
        self.canvas.bind('<Button-4>', lambda event : self.canvas.yview('scroll', -1, 'units'))
        self.canvas.bind('<Button-5>', lambda event : self.canvas.yview('scroll', 1, 'units'))
        
    def getPngFileDimension(self,filename):
        infile=open(filename,'rb')
        ## infile.seek(16) 
        ## value = infile.read(8)
        ## print repr(value)
        infile.seek(16)
        width=0 ; height=0
        for h in range(0,4):
            width=width*256+ord(infile.read(1))
        
        for h in range(0,4):
            height=height*256+ord(infile.read(1))
        ## print width , height
        infile.close() 
        return [width,height]

    def getJpgFileDimension(self,filename):
        width=0 ; height=0
        infile=open(filename,'rb')
        dataSize = len(infile.read())
        infile.seek(0)
        data = infile.read(4)
        if(data[0] == 0xFF and data[1] == 0xD8 and data[2] == 0xFF and data[3] == 0xE0):
            print('a valid SOI header')
        else:
            infile.close() 
            return [width,height]

        ## Check for valid JPEG header (null terminated JFIF)
        infile.seek(6)
        data = infile.read(5)
        if((data[0]) == 0x4A and (data[1]) == 0x46 and (data[2]) == 0x49 and (data[3]) == 0x46 and (data[4]) == 0x00):
            print('a valid JFIF string')
        else:
            infile.close() 
            return [width,height]
        
        i=4
        ## Retrieve the block length of the first block since the first block will not contain the size of file
        infile.seek(i)
        data = infile.read(2) 
        blockLength = (data[0]) * 256 + (data[1])

        while(i < dataSize):
            i = i + blockLength    ## Increase the file index to get to the next block
            if(i >= dataSize):
                break   ## Check to protect against segmentation faults
                
            infile.seek(i)
            data = infile.read(2)
            print(hex((data[0])) , hex((data[1])) )
            if((data[0]) != 0xFF):
                break   ## Check that we are truly at the start of another block
                

            ## packets with size information
            if((data[1]) == 0xC0 or (data[1]) == 0xC1 or (data[1]) == 0xC2 or \
                (data[1]) == 0xC3 or (data[1]) == 0xC5 or (data[1]) == 0xC6 or \
                (data[1]) == 0xC7 or (data[1]) == 0xC9 or (data[1]) == 0xCA or \
                (data[1]) == 0xCB or (data[1]) == 0xCD or (data[1]) == 0xCE or \
                (data[1]) == 0xCF ):
                data = infile.read(7)
                height = (data[3])*256 + (data[4])
                width = (data[5])*256 + (data[6])
                break
            else:
                data = infile.read(2)
                blockLength = (data[0]) * 256 + (data[1]) + 2 ## Go to the next block

        ## print hex(width) , hex(height)
        infile.close() 
        return [width,height]
        
if __name__ == '__main__':     
    root = Tk()
    app = ImgBrowser(root)
    root.mainloop()
