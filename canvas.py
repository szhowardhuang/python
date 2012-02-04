from Tkinter import *
import glob, os
from PIL import Image, ImageTk
import tkFileDialog
import subprocess

class ScrolledCanvas(Frame):
    IMG_W = 240; IMG_H = 160
    IMG_X=250; IMG_Y=210; IMG_NUM_ON_ROW=5
    
    def __init__(self, parent=None, color='brown'):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)                  
        canv = Canvas(self, bg=color, relief=SUNKEN)
        canv.config(width=1280, height=600)                
        canv.config(scrollregion=(0,0,1280, 10000))         
        canv.config(highlightthickness=0)                 

        sbar = Scrollbar(self)
        sbar.config(command=canv.yview)                   
        canv.config(yscrollcommand=sbar.set)              
        sbar.pack(side=RIGHT, fill=Y)                     
        canv.pack(side=LEFT, expand=YES, fill=BOTH)
        self.canvas = canv

    def showImage(self):
        filedir = tkFileDialog.askdirectory()
        files = os.listdir(filedir)
        self.IMG_DIR = filedir
        self.IMG_FILES = files
        for file in files[:]:
            if(file.split(".")[-1].upper() != 'JPG'):
                files.remove(file)
        self.photo = list(range(len(files)))
        for k, fname in enumerate(files):
            img = Image.open(filedir+"/"+fname)
            img.thumbnail((self.IMG_W, self.IMG_H))
            self.photo[k] = ImageTk.PhotoImage(img)
            self.canvas.create_image(self.IMG_X*(k%self.IMG_NUM_ON_ROW),k//self.IMG_NUM_ON_ROW*self.IMG_Y,image=self.photo[k], anchor="nw")
            self.canvas.create_text(self.IMG_X*(k%self.IMG_NUM_ON_ROW)+self.IMG_W/3,k//self.IMG_NUM_ON_ROW*self.IMG_Y+self.IMG_H+20, text=fname, fill='beige')

        self.canvas.create_bitmap(100, 100, bitmap="question", foreground="gold")
        self.canvas.bind('<Double-1>', self.onDoubleClick)       # set event handler
        
    def onDoubleClick(self, event):
        raw = int(self.canvas.canvasx(event.x) // self.IMG_X)
        collum = int(self.canvas.canvasy(event.y) // self.IMG_Y)
        #print raw,collum
        #print event.x, event.y
        #print self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)        
        fname=self.IMG_FILES[raw+self.IMG_NUM_ON_ROW*collum]
        img = Image.open(self.IMG_DIR+"/"+fname)
        img.show()
        p = subprocess.Popen(["gnome-mplayer" , self.IMG_DIR+"/"+fname])
        sts = os.waitpid(p.pid, 0)
        
        
app = ScrolledCanvas()
app.master.title("Sample application")
app.showImage()
app.mainloop()
#if __name__ == '__main__': ScrolledCanvas().mainloop()
