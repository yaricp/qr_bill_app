import os
import re
from datetime import datetime
from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import pytesseract

from config import *
from models.language import Language


def recognize_video():
    video_file_path = os.path.join(PATH_TEMP_FILES,'qrcode.mp4')
    vidcap = cv2.VideoCapture(video_file_path)
    success,image = vidcap.read()
    count = 0
    while success:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        list_decoded = decode(gray)
        success,image = vidcap.read()
        if list_decoded:
            date_time, summ = parse_qr_code(list_decoded)
            return date_time, summ, False
    vidcap = cv2.VideoCapture(video_file_path)
    success,image = vidcap.read()
    while success:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        list_decoded, adj_img = adjust_and_decode(gray)
        success,image = vidcap.read()
        if list_decoded:
            date_time, summ = parse_qr_code(list_decoded)
            return date_time, summ, False
    return None, None, True
        

def recognize_image(user):
    image_file_path = os.path.join(PATH_TEMP_FILES,'qrcode.jpg')
    image = cv2.imread(image_file_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    list_decoded = decode(gray)
    if list_decoded:
        date_time, summ = parse_qr_code(list_decoded)
        return date_time, summ, False
    list_decoded, adj_img = adjust_and_decode(gray)
    if list_decoded:
        date_time, summ = parse_qr_code(list_decoded)
        return date_time, summ, False
    date_time, summ = parse_raw_text(adj_img, user)
    if date_time or summ:
        return date_time, summ, True
    else:
        return None, None, True
    
    
def adjust_and_decode(gray):
    list_decoded = None
    for i in range(127, 160):
        print(i)
        (thresh, blackAndWhiteImage) = cv2.threshold(gray, i, 255, cv2.THRESH_BINARY)
        cv2.imwrite("image_processed.png",blackAndWhiteImage)
        cv2.imwrite("image_gray.png",gray)
        list_decoded = decode(blackAndWhiteImage)
        if list_decoded:
            break
    return list_decoded, blackAndWhiteImage
    

def scan(user='251241715', image=False, video=True):
    date_time = None
    summ = None
    raw = False
    if image:
        date_time, summ, raw = recognize_image(user) 
    if video:
        date_time, summ, raw = recognize_video()
    return date_time, summ, raw
        

def parse_qr_code(list_decoded):
    date_time = None
    summ = None
    for rec in list_decoded:
        print('TYPE_CODE: ', rec.type)
        type_data = rec.type
        if type_data == 'QRCODE':
            list_data = rec.data.decode("utf-8").split('&')
            temp_datetime = '%Y%m%dT%H%M'
            str_date_time = list_data[0].replace('t=', '')
            if len(str_date_time.split('T')[1]) == 6:
                temp_datetime = '%Y%m%dT%H%M%S'
            date_time = datetime.strptime(str_date_time, temp_datetime)
            summ = float(list_data[1].replace('s=', ''))
        elif type_data == 'EAN13':
            list_data = rec.data.decode("utf-8")
            print(list_data)
        print('DATA: ', rec.data)
    return date_time, summ
    

def parse_raw_text(img, user):
    date_time = ''
    summ = ''
    lang, created = Language.get_or_create(user=user)
    #print('lang: ', lang.lang)
    lang_dict = {
                'ru': 'rus', 
                'en': 'eng'
                }
    raw_text = pytesseract.image_to_string(img, lang=lang_dict[lang.lang])
    #print('raw_text: ', str(raw_text))
    
    rows = raw_text.split('\n')
    for row in rows:
        match = None
        
        list_matches = [r"(\d{2}\.\d{2}\.\d{2} \d{2}: \d{2})",
                        r"(\d{2}\.\d{2}\.\d{2} \d{2}:\d{2})",
                        r"(\d{2}\.\d{2}\. \d{2} \d{2}: \d{2})",
                        r"(\d{2}\.\d{2}\. \d{2} \d{2}:\d{2})",
                        r"(\d{4}\-\d{2}\-\d{2} \d{2}: \d{2})",
                        r"(\d{2}\-\d{2}\-\d{2} \d{2}:\d{2})",
                        r"(\d{4}\-\d{2}\-\d{2} \d{2}: \d{2})",
                        r"(\d{2}\-\d{2}\-\d{2} \d{2}:\d{2})", 
                        r"(\d{2}\.\d{2}\.\d{2} )",
                        r"(\d{2}\.\d{2}\.\d{2} )",
                        r"(\d{2}\.\d{2}\.\d{2} )",
                        r"(\d{2}\.\d{2}\.\d{2} )",
                        ]
        for exp in list_matches:
            #print('exp date time :', exp)
            match = re.search(exp, row)
            #print(match)
            if match:
                #print('break')
                break
        if match:
            date_time = match.group(1).replace(' ', '').replace('.', '-')
            date = date_time[:8]
            date_time = date_time[:8] + ' ' + date_time[8:] + ':00'
            #print('date: ', date)
            #print('datetime: ', date_time)
            continue
        list_matches = [r"((|=)\d+(\.|,)\d{1,2}$)", 

                        ]
        
        row = row.replace(' ', '')
        #print('row: ', row)
        for exp in list_matches:
            #print('exp: ', exp)
            match = re.search(exp, row)
            if match:
                #print(match)
                summ = match.group(1).replace(' ', '').replace('=', '').replace(',', '.')
                #print('summ', summ)
                break
    return date_time,  summ
    
    
def parse_text(text):
    
    list = text.split(' ')
    if len(list) > 1:
        return get_datetime_from_string(list[0]), list[1]
    list = text.split('&')
    if len(list) > 1:
        temp_datetime = '%Y%m%dT%H%M'
        str_date_time = list[0].replace('t=', '')
        if len(str_date_time.split('T')[1]) == 6:
            temp_datetime = '%Y%m%dT%H%M%S'
        date_time = datetime.strptime(str_date_time, temp_datetime)
        summ = float(list[1].replace('s=', ''))
    return date_time,  summ
    
    
def get_datetime_from_string(text_date):
    date_time = None
    dict_matches = {
                    1: '%Y-%m-%d', 
                    2: '%Y/%m/%d', 
                    3: '%Y.%m.%d', 
                    4: '%d-%m-%Y', 
                    5: '%d/%m/%Y',
                    6: '%d.%m.%Y', 
                    7: '%m-%d-%Y', 
                    8: '%m/%d/%Y',
                    9: '%m.%d.%Y',
                    10: '%y-%m-%d', 
                    11: '%y/%m/%d', 
                    12: '%y.%m.%d', 
                    13: '%d-%m-%y', 
                    14: '%d/%m/%y',
                    15: '%d.%m.%y', 
                    16: '%m-%d-%y', 
                    17: '%m/%d/%y',
                    18: '%m.%d.%y',
                    19: '%b-%d-%Y', 
                    20: '%b/%d/%Y', 
                    21: '%b.%d.%Y', 
                    22: '%d-%b-%Y', 
                    23: '%d/%b/%Y', 
                    24: '%d.%b.%Y', 
                    25: '%b-%d-%y', 
                    26: '%b/%d/%y', 
                    27: '%b.%d.%y', 
                    28: '%d-%b-%y', 
                    29: '%d/%b/%y', 
                    30: '%d.%b.%y',
                    }
    for k, v in dict_matches.items():
        match = re.search(v, text_date)
        key = k
        if match:
            break
    date_time = datetime.strptime(text_date, dict_matches[key])
    return date_time
    
    
if __name__ == "__main__":
    scan()
    
