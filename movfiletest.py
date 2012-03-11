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



def isMovFile(file):
    movExtension = file.split(".")[-1].upper()
    ## if(movExtension =='DAT' or movExtension =='ASF' or movExtension =='MP4' or movExtension =='DIVX' \
        ## or movExtension =='DIV' or movExtension =='MOV' or movExtension =='MPEG' \
        ## or movExtension =='MPE' or movExtension =='FLV' or movExtension =='TS' ):
    if(movExtension =='DAT'):
        return True
    else:
        return False

def checkFiles(movDirectory):
    for root, dirs, files in os.walk(movDirectory):
        for file in files:
            if(isMovFile(file)):
                path = root+os.sep+file+'\n'
                print path
                    

checkFiles('/media/d385e1f4-6d63-415c-b6a2-a7263d0cd06f/')
