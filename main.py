import torch, torchvision
from date_extractor import extract_date,extract_dates
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()
import time
from htmldate import find_date
import numpy as np
import random
import cv2
from dateparser.search import search_dates
import datefinder
import glob
import os
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt
import datetime
import sys
from selenium import webdriver
from google.colab.patches import cv2_imshow
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import ColorMode
from detectron2.data.catalog import DatasetCatalog
from detectron2.data.datasets import register_coco_instances
import requests
import articleDateExtractor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from GoogleNews import GoogleNews
DatasetCatalog.clear()
register_coco_instances("test", {}, "/content/_annotations.coco.json", "/content/")      #register the classes in the detectron2 Data Catalogue
MetadataCatalog.get("test").thing_classes = ["news-data", "body","headline"]          
test_metadata = MetadataCatalog.get("test")
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')              #adding path to the chromedriver
from difflib import SequenceMatcher
import re

from utils.dates import get_dates
from utils.getlinks import get_links
from utils.getpredictor import get_predictor
from utils.screenshots import get_screenshots
from utils.visualizer import visualize
from optimizations.optimizations import suppress_multiple,merge_close
def main_func(keys,links=None):
    '''
    The main driver function
    Takes inputs:
    keys: a string which is used for getting links from the Google News API.
    links: a list of links which are processed on instead if they are given.
    By default the links are set to None.
    Returns a list of tuples where each tuple is of the form [link,headline,body,date]
    Usage:
    For using keywords to get the OCR output: results = main_func('some keywords')
    For using list of links to get the OCR output: results = main_func('',l) where l is the list of links
    '''
    j=0
    dic=[]
    if links==None:
        links=get_links(keys)

    predictor=get_predictor()
    for link in links:
        print(j,link)
        j+=1
        headline=None
        body=None
        try:
            date=find_date(link)
        except:
            date=None
        images=get_screenshots(link)
        for image in images:
            '''
            visualize(image,predictor)                                 #uncomment if want to see the visualizations of the bounding boxes on the screenshots
            print('\n'*5)
            print('#################')
            '''
            temp_body=""
            temp_headline=""
            im2=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            (_, binary) = cv2.threshold(im2, 250, 255,cv2.THRESH_BINARY_INV)#|cv2.THRESH_OTSU)
            (_, binary) = cv2.threshold(binary, 250, 255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

            outputs = predictor(image)
            
            suppress_multiple(outputs)
            merge_close(outputs)
            temp=outputs['instances']
            boxes=temp.get_fields()['pred_boxes'].tensor.cpu().numpy()
            classes=temp.get_fields()['pred_classes'].cpu().numpy()

            for i in range(len(boxes)):
                tempimage=binary[int(boxes[i][1]):int(boxes[i][3]),int(boxes[i][0]):int(boxes[i][2])]
                if np.shape(tempimage)[0]==0:
                    continue
                try:
                    text = pytesseract.image_to_string(tempimage, lang = 'eng')
                except:
                    text=''
                if classes[i]==1:
                    temp_body=temp_body+text
                elif classes[i]==2:
                    temp_headline=temp_headline+text
            
            if headline==None:
                headline=temp_headline
            if body == None:
                body=temp_body
            else:
                body+=temp_body
        headline=re.sub('\s+',' ',headline)
        headline=headline.lower()
        body=re.sub('\s+',' ',body)
        body=body.lower()
        dic.append([link,headline,body,date])
    return dic


def accuracy(predicted,test):
    '''
    For checking the accuracy of strings in the OCR and the actual output via SequenceMatcher algorithm
    predicted: list of tuples where each tuple is of the form [headline,body]
    test: list of tuples where each tuple is of the form [headline,body]
    Returns a two list corresponding to the similarity scores between the headline and body.
    '''
    h_sim=[]
    b_sim=[]
    for i in range(len(test)):
        h_sim.append(SequenceMatcher(None,a=predicted[i][1],b=test[i][0]).ratio())
        b_sim.append(SequenceMatcher(None,a=predicted[i][2],b=test[i][1]).ratio())
    return h_sim,b_sim



def call(keywords):
    '''
    Call the main function with keywords and save the outputs for each link as a textfile. 
    Each link has 4 textfiles corresponding to it with the names being ID_link,ID_headline,ID_body,ID_date.
    Saves the files in the root directory.
    '''
    i=0
    results=main_func(keywords)
    for result in results:
        l=result[0]
        head=result[1]
        body=result[2]
        date=result[3]
        f=open('{}_link.txt'.format(i),'w')
        f.writelines(l)
        f.close()
        f=open('{}_headline.txt'.format(i),'w')
        f.writelines(head)
        f.close()
        f=open('{}_body.txt'.format(i),'w')
        f.writelines(body)
        f.close()
        f=open('{}_date.txt'.format(i),'w')
        f.writelines(date)
        f.close()
        i=i+1