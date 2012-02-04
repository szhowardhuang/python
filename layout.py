from Tkinter import *
import glob, os
from PIL import Image, ImageTk
import subprocess
import shutil
import stat
 
    
       
if __name__ == '__main__':     
    root = Tk()
    get_window = Toplevel(root)
    get_window.title('Source File?')
    get_window.geometry('600x480+0+0')
    Entry(get_window, width=30,text='www').place(x=100,y=100)
    Button(get_window, text="Change").place(x=400,y=100)
    Entry(get_window, width=30,text='helo').place(x=100,y=300)
    Button(get_window, text="Change2").place(x=400,y=300)
    root.mainloop()