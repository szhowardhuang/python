#!/usr/bin/env python  
  
import os,sys,math  
from glob import glob  
  
from Tkinter import *  
import Image  
from ImageTk import PhotoImage  
from tkFileDialog import askopenfilename,askdirectory  
from tkMessageBox import showerror  
  
class ViewPhotos(Frame):  
    """all photos manage"""  
    photodirs = ""  
    savephotos = ""  
  
    def __init__(self,parent=None,photo_dir=None):  
        Frame.__init__(self,parent)  
        self.pack(expand=YES,fill=BOTH)  
        self.makeWidgets()  
  
    def makeWidgets(self):  
        """ 
        init button 
        """  
        frm = Frame(self,relief=SUNKEN)  
        frm.pack(side=TOP,fill=X,padx=5)  
        Label(frm,text=':)Browse Directory:').pack(side=LEFT)  
        ent = Entry(frm,text='Type Your Directory or Press Browse Button',fg='blue')  
        ent.pack(side=LEFT,expand=YES,fill=X)  
        Button(frm,text='Browse...',command=self.onOpenDir).pack(side=LEFT)  
        Button(frm,text='Quit',command=self.quit).pack(side=RIGHT)  
  
        self.ent = ent  
  
    def makeCanvas(self):  
        """ 
        create content display area. 
        """  
        cont = Frame(self)  
        cont.pack(side=TOP,expand=YES,fill=BOTH,pady=3)  
        cont.config(relief=SUNKEN)  
        lis = Listbox(cont)  
        lis.pack(side=LEFT,fill=Y)  
        can = Canvas(cont)  
        can.config(width=300,height=200)  
        sbar = Scrollbar(cont)  
        sbar.config(command=can.yview)  
        can.config(yscrollcommand=sbar.set)  
        sbar.pack(side=RIGHT,fill=Y)  
        can.pack(side=LEFT,expand=YES,fill=BOTH)  
  
        #display photos  
        imglist = [img for img in os.listdir(self.photodirs)]  
        for img in imglist:  
            lis.insert(END,img)  
  
        lis.bind('<Double-Button-1>',self.viewOne)  
  
        self.lis = lis  
        self.can = can  
  
    def viewOne(self,event):  
        """one photo view"""  
        try:  
            index = self.lis.curselection()  
            img = self.lis.get(index)  
            imgpath = self.photodirs + '/' + img  
            imgobj = PhotoImage(file=imgpath)  
            #self.can.create_text(10,10,text=imgpath,font=('times',16,'bold'),fill='red')  
            self.can.create_image(10,20,image=imgobj,anchor=NW)  
            self.savephotos = imgobj  
        except IOError:  
            showerror('Photos',"This file isn't image.")  
            pass  
        return self.savephotos  
  
    def onOpenDir(self):  
        photodirs = askdirectory()  
        if photodirs:  
            if os.path.exists(photodirs):  
                self.photodirs = photodirs  
                #create display area.   
                self.makeCanvas()  
                self.ent.delete(0,END)  
                self.ent.insert(0,photodirs)  
            else:  
                showerror('Photos','you have not browse directory!')  
  
          
if __name__ == '__main__':  
    root = Tk()  
    root.geometry('800x600+50+50')  
    view = ViewPhotos(root)  
    root.mainloop()  