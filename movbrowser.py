# encoding: UTF-8

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

class MovBrowser(Frame):
    IMG_W = 240; IMG_H = 160
    IMG_X=250; IMG_Y=210; IMG_NUM_ON_ROW=5
    canvPanelWidth=1280; canvPanelHeight=600;# will dynamic modify by content
    
    def __init__(self, master):
        frame=Frame.__init__(self, master)
        self.MOV_FILES=[]
        self.movPlayer='gnome-mplayer'
        self.var  = IntVar()
        self.var.set(1)
        self.pack(expand=YES, fill=BOTH)
        self.makeMenu()
        self.makeProgressString()
        self.makeCanvas()
        
    def makeMenu(self):
        self.menubar = Menu(self)
        Operatemenu = Menu(self.menubar)
        self.menubar.add_cascade(label="Operate", menu=Operatemenu)
        Operatemenu.add_command(label="Show Image", command=self.startShowImage)
        Operatemenu.add_command(label="Update movie DB", command=self.updateMovDB)
        Operatemenu.add_separator()
        Operatemenu.add_command(label="Exit", command=self.quit)
        
        configmenu = Menu(self.menubar)
        selectPlayeremnu=Menu(configmenu)
        self.menubar.add_cascade(label="Config", menu=configmenu)
        configmenu.add_command(label="Set movie folder", command=self.setMovFolder)
        configmenu.add_cascade(label="Select movie player", menu=selectPlayeremnu)
        selectPlayeremnu.add_radiobutton(label='gnome-mplayer',value=1,\
                                         variable=self.var, command=self.setMovPlayer)
        selectPlayeremnu.add_radiobutton(label='smplayer',value=2,\
                                         variable=self.var, command=self.setMovPlayer)
        selectPlayeremnu.add_radiobutton(label='totem',value=3,\
                                         variable=self.var, command=self.setMovPlayer)
        selectPlayeremnu.add_radiobutton(label='vlc',value=4,\
                                         variable=self.var, command=self.setMovPlayer)
        selectPlayeremnu.add_radiobutton(label='realplay',value=5,\
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
    
    def setMovPlayer(self):
        print self.var.get()
        if(self.var.get() == 1):
            self.movPlayer = 'gnome-mplayer'
        if(self.var.get() == 2):
            self.movPlayer = 'smplayer'    
        if(self.var.get() == 3):
            self.movPlayer = 'totem'
        if(self.var.get() == 4):
            self.movPlayer = 'vlc'
        if(self.var.get() == 5):
            self.movPlayer = 'realplay'

    
    def isMovFile(self,file):
        movExtension = file.split(".")[-1].upper()
        if(movExtension == 'AVI' or movExtension =='MKV' or movExtension =='WMV' \
           or movExtension == 'MPG' or movExtension == 'ISO' or movExtension =='RM' \
           or movExtension =='RMVB'):
            return True
        else:
            return False
        
    def getPhotoFile(self,file):
        pos = file.rfind('.')
        photoFilename = file[0:pos]+'.UNK'
        jpgFilename = file[0:pos]+'.jpg'
        pngFilename = file[0:pos]+'.png'
        bmpFilename = file[0:pos]+'.bmp'
        
        if(os.path.exists(jpgFilename)):
            photoFilename=jpgFilename
        if(os.path.exists(bmpFilename)):
            photoFilename=bmpFilename
        if(os.path.exists(pngFilename)):
            photoFilename=pngFilename
        return photoFilename # if not photo,then return error filename


    def makeProgressString(self):
        self.progressString = StringVar()
        frm = Frame(self,relief=SUNKEN)  
        frm.pack(side=TOP,fill=X,padx=5)  
        Label(frm, textvariable=self.progressString).pack(side=LEFT)

    def updateProgressString(self,value):
        self.progressString.set("Progress: %d" % (value))

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
        
 
    def startShowImage(self):
        t2 = threading.Thread(target=self.showImage)
        t2.start()
        
        
    def showImage(self):
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
                        path = root+os.sep+file+'\n'
                        MOV_FILES.append(os.path.join(root, file))
            outfile = open(historyMovFile,"wb")
            pickle.dump(MOV_FILES, outfile,2)
            outfile.close()
        
        self.MOV_FILES = MOV_FILES            
        self.photo = list(range(len(MOV_FILES)))
        self.canvas.delete('all')
        fileNumbers = len(MOV_FILES)
        self.canvPanelHeight = (fileNumbers//self.IMG_NUM_ON_ROW + 1)*self.IMG_Y
        self.canvas.config(scrollregion=(0,0, self.canvPanelWidth, self.canvPanelHeight))
        for k, movname in enumerate(MOV_FILES):
            self.updateProgressString(k)
            time.sleep(0.05)
            photoname = self.getPhotoFile(movname)
            ## print photoname
            if(os.path.exists(photoname)):
                ## print movname,'   ',photoname
                img = Image.open(photoname)
                img.thumbnail((self.IMG_W, self.IMG_H))
                self.photo[k] = ImageTk.PhotoImage(img)
                self.canvas.create_image(self.IMG_X*(k%self.IMG_NUM_ON_ROW),\
                                         k//self.IMG_NUM_ON_ROW*self.IMG_Y,\
                                         image=self.photo[k], anchor="nw")
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
        
    def onDoubleClick(self, event):
        raw = int(self.canvas.canvasx(event.x) // self.IMG_X)
        collum = int(self.canvas.canvasy(event.y) // self.IMG_Y)
        fname=self.MOV_FILES[raw+self.IMG_NUM_ON_ROW*collum]
        imgFile=self.getPhotoFile(fname)
        if(os.path.exists(imgFile)):
            p1 = subprocess.Popen(["eog" , imgFile])
            ## sts1 = os.waitpid(p1.pid, 0)
        else: ## user can modify image name by manual
            p1 = subprocess.Popen(["caja" , os.path.split(imgFile)[0]])
        if(os.path.exists(fname)):
            p = subprocess.Popen([self.movPlayer , fname])
            ## sts = os.waitpid(p.pid, 0)

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
                        path = root+os.sep+file+'\n'
                        check_files.append(os.path.join(root, file))
        historyMovFile = self.getHistoryMovFileName()
        if(check_files==self.MOV_FILES):
            checkResult = "correct"
        else:
            checkResult = "incorrect"
            outfile = open(historyMovFile,"wb")
            pickle.dump(check_files, outfile,2)
            outfile.close()
        tkMessageBox.showinfo( "Movie DB Verify", checkResult+' , Movie DB Verify Finish.')
            
     
        
if __name__ == '__main__':     
    root = Tk()
    app = MovBrowser(root)
    app.master.title("Movie Browser application")
    root.mainloop()
