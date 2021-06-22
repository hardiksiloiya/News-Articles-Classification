import cv2
import numpy as np 
import matplotlib.pyplot as plt 
import pytesseract
import glob
import os
from pythonRLSA import rlsa
import math

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\hardi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

for file in glob.glob('C:/Users/hardi/Downloads/news_dataset/*.jpg'):
    im=cv2.imread(file)
    im2=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    (thresh, binary) = cv2.threshold(im2, 150, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    

    mask = np.ones(im.shape[:2], dtype="uint8") * 255 



    contours,h = cv2.findContours(binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours] 
    avgArea = sum(areas)/len(areas) 
    for c in contours:
        if cv2.contourArea(c)>60*avgArea:
            cv2.drawContours(mask, [c], -1, 0, -1)
    binary = cv2.bitwise_and(binary, binary, mask=mask) 

    contours, h= cv2.findContours(binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 




    #cv2.drawContours(im, contours, -1, (0,0,0), 3)
    '''for contour in contours:
    [x,y,w,h] = cv2.boundingRect(contour)
    cv2.rectangle(im, (x,y), (x+w,y+h), (0, 255, 0), 1)
    cv2.imwrite('contours.png', image)'''

    heights = [cv2.boundingRect(contour)[3] for contour in contours] 
    mask = np.ones(im.shape[:2], dtype="uint8") * 255 
    avgheight = sum(heights)/len(heights) 
    for c in contours:
        [x,y,w,h] = cv2.boundingRect(c)
        if h > 1.4*avgheight:
            cv2.drawContours(mask, [c], -1, 0, -1)
    #cv2.imshow('mask',mask)
    headline = pytesseract.image_to_string(mask, lang = 'eng')
    cv2.imwrite('C:/Users/hardi/Downloads/binary/'+os.path.basename(file).split('.')[0]+'.jpg',mask)

    f=open('C:/Users/hardi/Downloads/headlines/'+os.path.basename(file).split('.')[0]+'.txt','w')
    f.writelines(headline)
    f.close()
    x, y = mask.shape
    value = max(math.ceil(x/100),math.ceil(y/100))+20 
    mask = rlsa.rlsa(mask, True, False, value)
    (t, mask) = cv2.threshold(mask, 155, 255, cv2.THRESH_BINARY_INV)

    contours,h = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    #mask2 = np.ones(im.shape, dtype="uint8") * 255 
    for contour in contours:
        [x, y, w, h] = cv2.boundingRect(contour)
        if w > 0.30*im.shape[1]: 
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
            '''
            title = im[y: y+h, x: x+w] 
            mask2[y: y+h, x: x+w] = title 
            im[y: y+h, x: x+w] = 255 '''
    #cv2.imshow('title', mask2)
    cv2.imwrite('C:/Users/hardi/Downloads/smooth/'+os.path.basename(file).split('.')[0]+'.jpg',mask)
    cv2.imwrite('C:/Users/hardi/Downloads/final/'+os.path.basename(file).split('.')[0]+'.jpg',im)
    print(file,'  done')
    

    