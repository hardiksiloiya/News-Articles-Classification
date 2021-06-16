from dateparser.search import search_dates
import datefinder
import glob
import os
from PIL import Image
import pytesseract
tes_path='C:/"Program Files (x86)"/Tesseract-OCR'
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\hardi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
files=glob.glob('C:/Users/hardi/Downloads/news_dataset/*.jpg')
for file in files:
    try:
        print('name - ',file)
        im=Image.open(file)
        text = pytesseract.image_to_string(im, lang = 'eng')
        #print(text)
        dates=datefinder.find_dates(text,source=True)
        for date in dates:
            try:
                if (search_dates(date[1])) != None:
                    print(search_dates(date[1])[0][0])
            except:
                pass
    except:
        pass


