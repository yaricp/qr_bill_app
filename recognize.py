import os
import re
from datetime import datetime
from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import pytesseract

from config import *
from store.models.language import Language


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
        if DEVEL: print(i)
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
        if DEVEL: print('TYPE_CODE: ', rec.type)
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
            if DEVEL: print(list_data)
        if DEVEL: print('DATA: ', rec.data)
    return date_time, summ
    

def parse_raw_text(img, user):
    date_time = ''
    summ = ''
    lang, created = Language.get_or_create(user=user)
    if DEVEL: print('lang: ', lang.lang)
    lang_dict = {
                'ru': 'rus', 
                'en': 'eng'
                }
    raw_text = pytesseract.image_to_string(img, lang=lang_dict[lang.lang])
    #raw_text = pytesseract.image_to_string(img, lang='eng')
    if DEVEL: print('raw_text: ', str(raw_text).encode('utf-8').strip())
    
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
            #if DEVEL: print('exp date time :', exp)
            match = re.search(exp, row)
            #if DEVEL: print(match)
            if match:
                #if DEVEL: print('break')
                break
        if match:
            date_time = match.group(1).replace(' ', '').replace('.', '-')
            date = date_time[:8]
            date_time = date_time[:8] + ' ' + date_time[8:] + ':00'
            #if DEVEL: print('date: ', date)
            #if DEVEL: print('datetime: ', date_time)
            continue
        list_matches = [r"((|=)\d+(\.|,)\d{1,2}$)", 

                        ]
        
        row = row.replace(' ', '')
        #if DEVEL: print('row: ', row)
        for exp in list_matches:
            #if DEVEL: print('exp: ', exp)
            match = re.search(exp, row)
            if match:
                #if DEVEL: print(match)
                summ = match.group(1).replace(' ', '').replace('=', '').replace(',', '.')
                #if DEVEL: print('summ', summ)
                break
    return date_time,  summ
    
    
def parse_text(text):
    
    list = text.split(' ')
    if DEVEL: print('LIST: ', list)
    if DEVEL: print(len(list))
    if len(list) == 1:
        date_time = datetime.now()
        summ = list[0]
        return date_time,  summ
    if len(list) > 1:
        return get_datetime_from_string(list[0]), get_decimal_or_none(list[1])
    list = text.split('&')
    if len(list) > 1:
        temp_datetime = '%Y%m%dT%H%M'
        str_date_time = list[0].replace('t=', '')
        if len(str_date_time.split('T')[1]) == 6:
            temp_datetime = '%Y%m%dT%H%M%S'
        date_time = datetime.strptime(str_date_time, temp_datetime)
        #summ = float(list[1].replace('s=', ''))
        summ = get_decimal_or_none(list[1].replace('s=', ''))
    return date_time,  summ
    
    
def get_datetime_from_string(text_date):
    date_time = None
    matches = [
                '%d.%m.%Y',
                '%d-%m-%Y', 
                '%d/%m/%Y',
                '%Y-%m-%d', 
                '%Y/%m/%d', 
                '%Y.%m.%d', 
                '%m-%d-%Y', 
                '%m/%d/%Y',
                '%m.%d.%Y',
                '%y-%m-%d', 
                '%y/%m/%d', 
                '%y.%m.%d', 
                '%d-%m-%y', 
                '%d/%m/%y',
                '%d.%m.%y', 
                '%m-%d-%y', 
                '%m/%d/%y',
                '%m.%d.%y'
                    ]
    for v in matches:
        try:
            date_time = datetime.strptime(text_date, v)
            break
        except:
            if DEVEL: print('error type: ', v)
    return date_time
    
    
def get_decimal_or_none(text):
    result = None
    from decimal import Decimal
    try:
        result = Decimal(text)
    except: if DEVEL: print('error Decimal in '+ text)
    return result
    
    
if __name__ == "__main__":
    scan()
    
