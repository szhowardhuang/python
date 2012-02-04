from Tkinter import *
import glob, os
from PIL import Image, ImageTk
import tkFileDialog
 
root = Tk()
root.title("BIEC Picture Viewer")
filedir = tkFileDialog.askdirectory()
       # for infile in glob.glob("/home/howard/*.jpg"):
files = os.listdir(filedir)
for file in files[:]:
    if(file.split(".")[-1].upper() != 'JPG'):
        files.remove(file)
label = list(range(len(files)))
for k, fname in enumerate(files):
    image = Image.open(filedir+"/"+fname)
    ##((width, height))
    image.thumbnail((160, 240))
    photo = ImageTk.PhotoImage(image)
    label[k] = Label(root, image=photo)
    label[k].image = photo # keep a reference!
    label[k].pack()  # pack when you want to display it

# im = Image.open("/home/howard/faceTemplate.jpg")

#img = root.PhotoImage(Image.open(path))


root.mainloop()
