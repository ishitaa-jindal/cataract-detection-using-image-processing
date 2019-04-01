import cv2
import imutils
#import numpy as np
#from math import hypot
from matplotlib import pyplot as plt
from tkinter import *
from PIL import ImageTk
import tkinter.filedialog
from PIL import Image


def select_image():

    path = tkinter.filedialog.askopenfilename()

    if len(path) > 0:
        img = cv2.imread(path)                   
        img = imutils.resize(img, width=500)          

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
        #cv2.imshow("Grayscale Conversion", gray)

        gray = cv2.GaussianBlur(gray,(5,5),0)
        #cv2.imshow("Gaussian Filter", gray)

        m=cv2.meanStdDev(gray)

        if m[0]<50:
            print('Cataract is not present')
            print('Eye is healthy')
        elif m[0]<=100:
            print('Cataract is present')
            print('Eye has mild cataract')
        else:
            print('Cataract is present')
            print('Eye has severe cataract')

        print('Mean:', m[0])
        print('SD', m[1])

        
        plt.hist(gray.ravel(),256,[0,256]);
        plt.axvline(gray.mean(), color='k', linestyle='dashed', linewidth=1)
        plt.show()

root = Tk()

btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

root.mainloop()
