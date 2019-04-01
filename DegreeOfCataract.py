import cv2
import imutils
import numpy as np
from math import hypot
from tkinter import *
from PIL import ImageTk
import tkinter.filedialog
from PIL import Image

pupil_area = 0          
cat_area = 0                       

def select_image():
    
    global panelA, panelB,panelC, panelD,panelE, panelF,panelG, panelH,panelI
 
    path = tkinter.filedialog.askopenfilename()

    if len(path) > 0:
        img = cv2.imread(path)
        
        img = imutils.resize(img, width=500)            
        #cv2.imshow("Original Image of Eye", img)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #cv2.imshow("1 - Grayscale Conversion", gray)
        
        kernel = np.ones((5,5),np.float32)/25           
        imgfiltered = cv2.filter2D(gray,-1,kernel)      
        #cv2.imshow("2 - 2D Filtered", imgfiltered)      

        kernelOp = np.ones((10, 10), np.uint8)          
        kernelCl = np.ones((15, 15), np.uint8)          

        ret,thresh_image = cv2.threshold(imgfiltered,50,255,cv2.THRESH_BINARY_INV)      
        #cv2.imshow("3 - Thresholding",thresh_image)
        
        morpho = cv2.morphologyEx(thresh_image, cv2.MORPH_OPEN, kernelOp)               
        #cv2.imshow("4 - Morpholigical Opening", morpho)                                                      

        circles = cv2.HoughCircles(morpho, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

        cimg_morpho=img.copy()
        img_morpho_copy = morpho.copy()                                 

        circle_values_list = np.uint16(np.around(circles))              
        x, y, r = circle_values_list[0,:][0]
        
        rows, cols = img_morpho_copy.shape

        for i in range(cols):                                           
            for j in range(rows):                                       
                if hypot(i-x, j-y) > r:                                 
                    img_morpho_copy[j,i] = 0                            

        imgg_inv = cv2.bitwise_not(img_morpho_copy)                     
        #cv2.imshow("6 - Iris Contour Separation", img_morpho_copy)
        
        #cv2.imshow("7 - Image Inversion", imgg_inv)                     

        contours0, hierarchy = cv2.findContours(img_morpho_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)   
        cimg_pupil = img.copy()                                                                                 

        for cnt in contours0:                                                   
                #cv2.drawContours(cimg_pupil, cnt, -1, (0, 255, 0), 3, 8)        
                pupil_area = cv2.contourArea(cnt)                             
                label6 = Label(root, text= "Pupil area: %d" % pupil_area)
                           

        contours0, hierarchy = cv2.findContours(imgg_inv, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)      
        cimg_cat = img.copy()                                                                           

        for cnt in contours0:                                                  
                if cv2.contourArea(cnt) < pupil_area:
                    
                    cv2.drawContours(cimg_cat, cnt, -1, (0, 255, 0), 3, 8)      
                    cat_area = cv2.contourArea(cnt)                           

                    cataract_percentage = (cat_area / (pupil_area + cat_area)) * 100        
                    
                    label1 = Label(root, text= "Cataract area: %d" % (cat_area))
                    label4 = Label(root, text= "You have %.2f percent cataract" % (cataract_percentage))
    
                    label6.pack()
                    label1.pack()
                    label4.pack()

        cv2.waitKey(0)

        img = Image.fromarray(img)
        gray = Image.fromarray(gray)
        imgfiltered = Image.fromarray(imgfiltered)
        thresh_image = Image.fromarray(thresh_image)
        morpho = Image.fromarray(morpho)
        cimg_morpho = Image.fromarray(cimg_morpho)
        img_morpho_copy = Image.fromarray(img_morpho_copy)
        imgg_inv = Image.fromarray(imgg_inv)
        cimg_cat = Image.fromarray(cimg_cat)

        width = 100
        height = 100
        img = img.resize((width,height), Image.ANTIALIAS)
        gray = gray.resize((width,height), Image.ANTIALIAS)
        imgfiltered = imgfiltered.resize((width,height), Image.ANTIALIAS)
        thresh_image = thresh_image.resize((width,height), Image.ANTIALIAS)
        morpho = morpho.resize((width,height), Image.ANTIALIAS)
        cimg_morpho = cimg_morpho.resize((width,height), Image.ANTIALIAS)
        img_morpho_copy = img_morpho_copy.resize((width,height), Image.ANTIALIAS)
        imgg_inv = imgg_inv.resize((width,height), Image.ANTIALIAS)
        cimg_cat = cimg_cat.resize((width,height), Image.ANTIALIAS)
        
        img = ImageTk.PhotoImage(img)
        gray = ImageTk.PhotoImage(gray)
        imgfiltered = ImageTk.PhotoImage(imgfiltered)
        thresh_image = ImageTk.PhotoImage(thresh_image)
        morpho = ImageTk.PhotoImage(morpho)
        cimg_morpho = ImageTk.PhotoImage(cimg_morpho)
        img_morpho_copy = ImageTk.PhotoImage(img_morpho_copy)
        imgg_inv = ImageTk.PhotoImage(imgg_inv)
        cimg_cat = ImageTk.PhotoImage(cimg_cat)

        if panelA is None or panelB is None or panelC is None or panelD is None or panelE is None or panelF is None or panelG is None or panelH is None or panelI is None:

            panelA = Label(image=img)
            panelA.image = img
            panelA.pack(side="left", padx=10, pady=10)

            #panelB = Label(image=gray)
            #panelB.image = gray
            #panelB.pack(side="left", padx=10, pady=10)

            panelC = Label(image=imgfiltered)
            panelC.image = imgfiltered
            panelC.pack(side="left", padx=10, pady=10)

            panelD = Label(image=thresh_image)
            panelD.image = thresh_image
            panelD.pack(side="left", padx=10, pady=10)

            #panelE = Label(image=morpho)
            #panelE.image = morpho
            #panelE.pack(side="left", padx=10, pady=10)

            #panelF = Label(image=cimg_morpho)
            #panelF.image = cimg_morpho
            #panelF.pack(side="left", padx=10, pady=10)

            panelG = Label(image=img_morpho_copy)
            panelG.image = img_morpho_copy
            panelG.pack(side="left", padx=10, pady=10)

            panelH = Label(image=imgg_inv)
            panelH.image = imgg_inv
            panelH.pack(side="left", padx=10, pady=10)

            panelI = Label(image=cimg_cat)
            panelI.image = cimg_cat
            panelI.pack(side="left", padx=10, pady=10)

        else:
            panelA.configure(image=img)
            #panelB.configure(image=gray)
            panelC.configure(image=imgfiltered)
            panelD.configure(image=thresh_image)
            #panelE.configure(image=morpho)
            #panelF.configure(image=cimg_morpho)
            panelG.configure(image=img_morpho_copy)
            panelH.configure(image=imgg_inv)
            panelI.configure(image=cimg_cat)

            panelA.image = img
            #panelB.image = gray
            panelC.image = imgfiltered
            panelD.image = thresh_image
            #panelE.image = morpho
            #panelF.image = cimg_morpho
            panelG.image = img_morpho_copy
            panelH.image = imgg_inv
            panelI.image = cimg_cat

root = Tk()
panelA = None
#panelB = None
panelC = None
panelD = None
#panelE = None
#panelF = None
panelG = None
panelH = None
panelI = None

btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

root.mainloop()
        






