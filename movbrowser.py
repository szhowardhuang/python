#!/usr/bin/python
#coding=utf-8 

from Tkinter import *
import glob, os
from PIL import Image, ImageTk
import tkFileDialog
import subprocess
import shutil
import stat
import threading
import time
import pickle
import tkMessageBox
## import re

class MovBrowser(Frame):
    IMG_W = 240; IMG_H = 160
    IMG_X=250; IMG_Y=210; IMG_NUM_ON_ROW=5
    
    def __init__(self, master):
        frame=Frame.__init__(self, master)
        self.canvPanelWidth = master.winfo_screenwidth()
        self.canvPanelHeight = master.winfo_screenheight()-150 ## height will dynamic modify by content
        self.MOV_FILES=[]
        self.movPlayer='default player'
        self.var  = IntVar()
        self.var.set(1)
        self.pack(expand=YES, fill=BOTH)
        self.makeMenu()
        self.makeProgressString()
        self.makeCanvas()

        
    def makeMenu(self):
        self.menubar = Menu(self)
        
        Filemenu = Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=Filemenu)
        Filemenu.add_command(label="Load File", command=self.loadMovDBFile)
        Filemenu.add_command(label="Save File As", command=self.saveMovDBFileAs)
        Filemenu.add_command(label="Exit", command=self.quit)
        
        Operatemenu = Menu(self.menubar)
        Sorttypemenu = Menu(Operatemenu)
        self.menubar.add_cascade(label="Operate", menu=Operatemenu)
        Operatemenu.add_command(label="Show All Image", command=self.startShowAllImage)
        Operatemenu.add_command(label="Show Favorite Image", command=self.startShowFavImage)
        Operatemenu.add_command(label="Update movie DB", command=self.updateMovDB)
        Operatemenu.add_cascade(label="Sort movie DB", menu=Sorttypemenu)
        
        Sorttypemenu.add_command(label = "By Movie Name",command=self.sortMovDBByName)
        Sorttypemenu.add_command(label = "By Movie File Size",command=self.sortMovDBByFileSize)
        Sorttypemenu.add_command(label = "By Movie Folder",command=self.sortMovDBByFolder)
        Sorttypemenu.add_command(label = "By Playback Frequency",command=self.sortMovDBByPlayback)

        
        configmenu = Menu(self.menubar)
        selectPlayeremnu=Menu(configmenu)
        self.menubar.add_cascade(label="Config", menu=configmenu)
        configmenu.add_command(label="Set movie folder", command=self.setMovFolder)
        configmenu.add_cascade(label="Select movie player", menu=selectPlayeremnu)
        selectPlayeremnu.add_radiobutton(label='default player',value=1,\
                                         variable=self.var, command=self.setMovPlayer)
        selectPlayeremnu.add_radiobutton(label='ubuntu gnome-mplayer',value=2,\
                                         variable=self.var, command=self.setMovPlayer)
        selectPlayeremnu.add_radiobutton(label='ubuntu smplayer',value=3,\
                                         variable=self.var, command=self.setMovPlayer)
        selectPlayeremnu.add_radiobutton(label='ubuntu totem',value=4,\
                                         variable=self.var, command=self.setMovPlayer)
        selectPlayeremnu.add_radiobutton(label='vlc',value=5,\
                                         variable=self.var, command=self.setMovPlayer)
        selectPlayeremnu.add_radiobutton(label='realplay',value=6,\
                                         variable=self.var, command=self.setMovPlayer)

        self.master.config(menu=self.menubar)
        
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
    
    def getMovBrowserIniFileName(self):
        return os.getenv('HOME')+os.sep+'movlist.ini'
    
    def getHistoryMovFileName(self):
        return os.getenv('HOME')+os.sep+'movlist.dat'
    
    def getFavoriteFileName(self):
        return os.getenv('HOME')+os.sep+'favlist.dat'
    
    def setMovPlayer(self):
        if(self.var.get() == 1):
            self.movPlayer = 'default player'
        if(self.var.get() == 2):
            self.movPlayer = 'gnome-mplayer'
        if(self.var.get() == 3):
            self.movPlayer = 'smplayer'    
        if(self.var.get() == 4):
            self.movPlayer = 'totem'
        if(self.var.get() == 5):
            self.movPlayer = 'vlc'
        if(self.var.get() == 6):
            self.movPlayer = 'realplay'

    
    def isMovFile(self,file):
        movExtension = file.split(".")[-1].upper()
        if(movExtension == 'AVI' or movExtension =='MKV' or movExtension =='WMV' \
           or movExtension == 'MPG' or movExtension == 'ISO' or movExtension =='RM' \
           or movExtension =='RMVB' or movExtension =='MDF' or movExtension =='DAT' \
           or movExtension =='ASF' or movExtension =='MP4' or movExtension =='DIVX' \
           or movExtension =='DIV' or movExtension =='MOV' or movExtension =='MPEG' \
           or movExtension =='MPE' or movExtension =='FLV' or movExtension =='TS' ):
            return True
        else:
            return False
        
    def getPhotoFile(self,file):
        pos = file.rfind('.')
        photoFilename = file[0:pos]+'.UNK'
        for i in range(1,4): ## remove the latest letter of file
            jpgFilename = file[0:pos]+'.jpg'
            pngFilename = file[0:pos]+'.png'
            bmpFilename = file[0:pos]+'.bmp'
            jpgFilename1 = file[0:pos]+'.JPG'
            pngFilename1 = file[0:pos]+'.PNG'
            bmpFilename1 = file[0:pos]+'.BMP'
            pos = pos - 1
            if(os.path.exists(jpgFilename)):
                photoFilename=jpgFilename
                break
            if(os.path.exists(bmpFilename)):
                photoFilename=bmpFilename
                break
            if(os.path.exists(pngFilename)):
                photoFilename=pngFilename
                break
            if(os.path.exists(jpgFilename1)):
                photoFilename=jpgFilename1
                break
            if(os.path.exists(bmpFilename1)):
                photoFilename=bmpFilename1
                break
            if(os.path.exists(pngFilename1)):
                photoFilename=pngFilename1
                break
        return photoFilename # if not photo,then return error filename


    def makeProgressString(self):
        self.progressString = StringVar()
        frm = Frame(self,relief=SUNKEN)  
        frm.pack(side=TOP,fill=X,padx=5)  
        Label(frm, textvariable=self.progressString).pack(side=LEFT)

    def updateProgressString(self,value):
        self.progressString.set("Progress: %d" % (value+1))

    def setMovFolder(self):
        get_window = Toplevel(self)
        get_window.title('Source File?')
        get_window.geometry('600x480+0+0')
        ## Entry(get_window, width=60,textvariable=self.source).place(x=10,y=10)
        Button(get_window, text="Del", command=self.delFolder).place(x=500,y=50)
        Button(get_window, text="Add", command=self.addFolder).place(x=500,y=100)
        lis = Listbox(get_window,width=50)
        filename=self.getMovBrowserIniFileName()
        if(os.path.exists(filename)):
            infile = open(filename, 'r')
            movDirectory = pickle.load(infile)
            infile.close()
            for str in movDirectory:
                lis.insert(0,str)  
        lis.pack(side=LEFT,fill=Y)  
        self.lis = lis
        self.get_window = get_window
 
        
    def addFolder(self):
        rootdir = tkFileDialog.askdirectory(parent=self.get_window)
        self.lis.insert(END,rootdir)
        movDirectory = self.lis.get(0,END)
        ## print movDirectory
        filename=self.getMovBrowserIniFileName()
        outfile = open(filename,"w")
        pickle.dump(movDirectory, outfile,0)
        outfile.close()
     
    def delFolder(self):
        try:
            index = self.lis.curselection()[0]
            self.lis.delete(index)
            movDirectory = self.lis.get(0,END)
            ## print movDirectory
            filename=self.getMovBrowserIniFileName()
            outfile = open(filename,"w")
            pickle.dump(movDirectory, outfile,0)
            outfile.close()
        except IndexError:
            pass
        
 
    def startShowFavImage(self):
        tShowFavImage = threading.Thread(target=self.showFavImage)
        tShowFavImage.start()
 
    def showFavImage(self):
        finalFiles = []
        favoriteFiles = []
        favoriteFileName = self.getFavoriteFileName()
        if(os.path.exists(favoriteFileName)):
            infile = open(favoriteFileName,"rb")
            favoriteFiles = pickle.load(infile)
            infile.close()       
        favoriteLen = len(favoriteFiles)
        if favoriteLen == 0:
            return
        else:
            for i in range(favoriteLen):
                finalFiles.append(favoriteFiles[i][1])
        self.MOV_FILES = finalFiles
        self.showImage()   
 
    def startShowAllImage(self):
        t2 = threading.Thread(target=self.showAllImage)
        t2.start()
    
    def initShowAllImage(self):
        MOV_FILES=[]
        historyMovFile = self.getHistoryMovFileName()
        if(os.path.exists(historyMovFile)):
            infile = open(historyMovFile, 'rb')
            MOV_FILES = pickle.load(infile)
            infile.close()
        else:
            rootdir = tkFileDialog.askdirectory()
            for root, dirs, files in os.walk(rootdir):
                for file in files:
                    if(self.isMovFile()):
                        fileURL = os.path.join(root, file)
                        if (not os.path.islink(fileURL)):
                            MOV_FILES.append(fileURL)
            outfile = open(historyMovFile,"wb")
            pickle.dump(MOV_FILES, outfile,2)
            outfile.close()
        return MOV_FILES
    
    def showAllImage(self):
        self.MOV_FILES = self.initShowAllImage()
        self.showImage()        
        
    def showImage(self):
        MOV_FILES = self.MOV_FILES         
        self.photo = list(range(len(MOV_FILES)))
        self.canvas.delete('all')
        fileNumbers = len(MOV_FILES)
        self.canvPanelHeight = (fileNumbers//self.IMG_NUM_ON_ROW + 1)*self.IMG_Y
        self.canvas.config(scrollregion=(0,0, self.canvPanelWidth, self.canvPanelHeight))
        for k, movname in enumerate(MOV_FILES):
            self.updateProgressString(k)
            time.sleep(0.01)
            photoname = self.getPhotoFile(movname)
            ## print photoname
            if(os.path.exists(photoname)):
                ## print movname,'   ',photoname
                try:
                    img = Image.open(photoname)
                    img.thumbnail((self.IMG_W, self.IMG_H))
                    self.photo[k] = ImageTk.PhotoImage(img)
                    self.canvas.create_image(self.IMG_X*(k%self.IMG_NUM_ON_ROW),\
                                            k//self.IMG_NUM_ON_ROW*self.IMG_Y,\
                                            image=self.photo[k], anchor="nw")
                except:
                    pass
            else:
                self.canvas.create_bitmap(self.IMG_X*(k%self.IMG_NUM_ON_ROW)+self.IMG_X/3,\
                                          k//self.IMG_NUM_ON_ROW*self.IMG_Y+self.IMG_H/2, \
                                          bitmap="question", foreground="gold", anchor="nw")
                
            mov_sname=movname.split(os.sep)[-1]
            ## print(mov_sname)
            self.canvas.create_text(self.IMG_X*(k%self.IMG_NUM_ON_ROW)+self.IMG_W/3,\
                                    k//self.IMG_NUM_ON_ROW*self.IMG_Y+self.IMG_H+20, \
                                    text=mov_sname, fill='beige', width=self.IMG_W)

        self.canvas.bind('<Double-1>', self.onDoubleClick)       # set event handler
        self.canvas.bind('<Button-4>', lambda event : self.canvas.yview('scroll', -1, 'units'))
        self.canvas.bind('<Button-5>', lambda event : self.canvas.yview('scroll', 1, 'units'))
        
    def convertFilename(self,src):
        print repr(src) 
        isUnicode = False
        if(isinstance(src, unicode)):
            isUnicode = True
            src.encode('GBK') ## encode to GBK for chinses handler
        dest = []
        for i in range(len(src)):
            if src[i] == ' ' or src[i] == '(' or src[i] == ')' or src[i] == '-':
                dest += '\\'
            dest += src[i]
        if isUnicode:
            return ''.join(dest).encode('utf-8') ## encode to utf-8
        else:
            return ''.join(dest)
        
    
    def openFileByDefaultApplication(self, file):
        if os.name == "nt":
            os.filestart(file)
        elif os.name == "posix":
            if os.uname()[0] == "Linux":
                os.system("/usr/bin/xdg-open " + self.convertFilename(file))
            elif os.uname()[0] == "Darwin":
                os.system("open "+file)
        print os.uname()[0]

    def saveFavoriteFile(self,filename):
        originalFiles = []
        newFavorite = True
        favoriteFileName = self.getFavoriteFileName()
        if(os.path.exists(favoriteFileName)):
            infile = open(favoriteFileName,"rb")
            originalFiles = pickle.load(infile)
            infile.close()       
        favoriteLen = len(originalFiles)
        if favoriteLen == 0:
            originalFiles.append([1,filename])
        else:
            for i in range(favoriteLen):
                if filename in originalFiles[i]:
                    newFavorite=False
                    originalFiles[i][0] = originalFiles[i][0] + 1
            if newFavorite:
                originalFiles.append([1,filename])

        originalFiles.sort()
        originalFiles.reverse()
        ## print originalFiles
        
        outfile = open(favoriteFileName,"wb")
        pickle.dump(originalFiles, outfile,2)
        outfile.close()
        
    def onDoubleClick(self, event):
        raw = int(self.canvas.canvasx(event.x) // self.IMG_X)
        collum = int(self.canvas.canvasy(event.y) // self.IMG_Y)
        fname=self.MOV_FILES[raw+self.IMG_NUM_ON_ROW*collum]
        imgFile=self.getPhotoFile(fname)
        if(os.path.exists(imgFile)):
            self.openFileByDefaultApplication(imgFile)  
        else: ## open folder,then user can modify image name by manual
            self.openFileByDefaultApplication(os.path.split(imgFile)[0])
        if(os.path.exists(fname)):
            self.saveFavoriteFile(fname)
            if(self.movPlayer == 'default player'):
                self.openFileByDefaultApplication(fname)
            else:
                p = subprocess.Popen([self.movPlayer , fname])
            ## sts = os.waitpid(p.pid, 0)

    def sortMovDBByPlayback(self):
        tSort = threading.Thread(target=self.sortFilesByPlayback)
        tSort.start()
        
    def sortFilesByPlayback(self):
        originalFiles=[]
        historyMovFile = self.getHistoryMovFileName()
        if(os.path.exists(historyMovFile)):
            infile = open(historyMovFile,"rb")
            originalFiles = pickle.load(infile)
            infile.close()

        finalFiles = []
        favoriteFiles = []
        favoriteFileName = self.getFavoriteFileName()
        if(os.path.exists(favoriteFileName)):
            infile = open(favoriteFileName,"rb")
            favoriteFiles = pickle.load(infile)
            infile.close()       
        favoriteLen = len(favoriteFiles)
        originalLen = len(originalFiles)
        if favoriteLen == 0 or originalLen == 0:
            return
        else:
            for i in range(favoriteLen):
                try:
                    finalFiles.append(favoriteFiles[i][1])
                    originalFiles.remove(favoriteFiles[i][1])
                except:
                    pass
                    

        finalFiles = finalFiles + originalFiles
        ## print finalFiles
     
        outfile = open(historyMovFile,"wb")
        pickle.dump(finalFiles, outfile,2)
        outfile.close()
        self.showAllImage()

    def sortMovDBByFolder(self):
        tSort = threading.Thread(target=self.sortFilesByFolder)
        tSort.start()
        
    def sortFilesByFolder(self):
        originalFiles=[]
        historyMovFile = self.getHistoryMovFileName()
        if(os.path.exists(historyMovFile)):
            infile = open(historyMovFile,"rb")
            originalFiles = pickle.load(infile)
            infile.close()

        originalFiles.sort()
        originalFiles.reverse()
        ## print originalFiles
     
        outfile = open(historyMovFile,"wb")
        pickle.dump(originalFiles, outfile,2)
        outfile.close()
        self.showAllImage()
        
    def sortMovDBByFileSize(self):
        tSort = threading.Thread(target=self.sortFilesByFileSize)
        tSort.start()
        
    def sortFilesByFileSize(self):
        originalFiles=[]
        historyMovFile = self.getHistoryMovFileName()
        if(os.path.exists(historyMovFile)):
            infile = open(historyMovFile,"rb")
            originalFiles = pickle.load(infile)
            infile.close()
        sortFiles = []
        finalFiles = []
        for file in originalFiles:
            if(self.isMovFile(file)):
                sortFiles.append(os.path.getsize(file))
        ## print sortFiles
        
        originalSize = len(originalFiles)
        for i in range(originalSize):
            maxValue=max(sortFiles)
            k=sortFiles.index(maxValue)
            finalFiles.append(originalFiles[k])
            sortFiles.remove(maxValue)
            originalFiles.remove(originalFiles[k])
        ## print finalFiles
        
        outfile = open(historyMovFile,"wb")
        pickle.dump(finalFiles, outfile,2)
        outfile.close()
        self.showAllImage()
        
    def sortMovDBByName(self):
        tSort = threading.Thread(target=self.sortFilesByName)
        tSort.start()
        
    def sortFilesByName(self):
        originalFiles=[]
        historyMovFile = self.getHistoryMovFileName()
        if(os.path.exists(historyMovFile)):
            infile = open(historyMovFile,"rb")
            originalFiles = pickle.load(infile)
            infile.close()
        sortFiles = []
        finalFiles = []
        for file in originalFiles:
            if(self.isMovFile(file)):
                sortFiles.append(os.path.split(file)[-1])
        sortFiles=list(set(sortFiles))
        sortFiles.sort()
        ## print sortFiles

        for file in sortFiles:
            for oriFile in originalFiles:
                if oriFile.find(file) != -1:
                    finalFiles.append(oriFile)
        ## print finalFiles
        
        outfile = open(historyMovFile,"wb")
        pickle.dump(finalFiles, outfile,2)
        outfile.close()
        self.showAllImage()

    def updateMovDB(self):
        movConfigFile = self.getMovBrowserIniFileName()
        if(os.path.exists(movConfigFile)):
            infile = open(movConfigFile, 'r')
            movDirectory = pickle.load(infile)
            infile.close()
        else:
            movDirectory = tkFileDialog.askdirectory()
            infile = open(movConfigFile, 'w')
            pickle.dump(movDirectory, outfile,0)
            infile.close()
        self.movDirectory = movDirectory
        t1 = threading.Thread(target=self.checkFiles)
        t1.start()
        
    def checkFiles(self):
        check_files=[]
        i=0
        for movfolder in self.movDirectory:
            print movfolder
            for root, dirs, files in os.walk(movfolder):
                for file in files:
                    i=i+1
                    self.updateProgressString(i)
                    if(self.isMovFile(file)):
                        fileURL = os.path.join(root, file)
                        if (not os.path.islink(fileURL)):
                            check_files.append(fileURL)
        historyMovFile = self.getHistoryMovFileName()
        if(check_files==self.MOV_FILES):
            checkResult = "correct"
        else:
            checkResult = "incorrect"
            outfile = open(historyMovFile,"wb")
            pickle.dump(check_files, outfile,2)
            outfile.close()
        tkMessageBox.showinfo( "Movie DB Verify", checkResult+' , Movie DB Verify Finish.')
            
    def saveMovDBFileAs(self):
        originalFiles = []
        historyMovFile = self.getHistoryMovFileName()
        if(os.path.exists(historyMovFile)):
            infile = open(historyMovFile,"rb")
            originalFiles = pickle.load(infile)
            infile.close()
        
        filename=tkFileDialog.asksaveasfilename(defaultextension='.dat',initialdir=os.getenv('HOME'),\
                                                filetypes=[('mov list files', '.dat')])
        if filename:
            outfile = open(filename, 'wb')
            pickle.dump(originalFiles, outfile,2)
            outfile.close()
            
    def loadMovDBFile(self):
        MOV_FILES=[]
        filename=tkFileDialog.askopenfilename(defaultextension='.dat',initialdir=os.getenv('HOME'),\
                                                filetypes=[('mov list files', '.dat')])
        if filename:
            infile = open(filename, 'rb')
            MOV_FILES=pickle.load(infile)
            infile.close()
        
        historyMovFile = self.getHistoryMovFileName()
        outfile = open(historyMovFile,"wb")
        pickle.dump(MOV_FILES, outfile,2)
        outfile.close()

        
if __name__ == '__main__':     
    root = Tk()
    app = MovBrowser(root)
    app.master.title("Movie Browser application")
    root.mainloop()
