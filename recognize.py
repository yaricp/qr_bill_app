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
        list_decoded = adjust_and_decode(gray)
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
#        for j in range(200, 255):
#            print(j)
        (thresh, blackAndWhiteImage) = cv2.threshold(gray, i, 255, cv2.THRESH_BINARY)
        cv2.imwrite("image_processed.png",blackAndWhiteImage)
        cv2.imwrite("image_gray.png",gray)
        #image_file = Image.open("image_processed.png")
        list_decoded = decode(blackAndWhiteImage)
    return list_decoded, blackAndWhiteImage
    

def scan(user='251241715', image=True, video=False):
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
    print('raw_text: ', raw_text.encode('utf-8'))
    
    rows = raw_text.split('\n')
    for row in rows:
        match = None
        #print('row: ', row)
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
            print('date: ', date)
            print('datetime: ', date_time)
            continue
        list_matches = [r"((|=)\d+(\.|,)(| )\d{1,2}( |$))", 
#                        r"(\d+\. \d{1,2}) ", 
#                        r"(=\d+\. \d{1,2}) ", 
#                        r"(=\d+\.\d{1,2}) ",
#                        r"(\d+(\.|,)\d{1,2})$", 
#                        r"(\d+\. \d{1,2})$", 
#                        r"(=\d+\. \d{1,2})$", 
#                        r"(=\d+\.\d{1,2})$",
                        ]
        #print('start search summ')
        for exp in list_matches:
            #print('exp: ', exp)
            match = re.search(exp, row)
            if match:
                #print(match)
                summ = match.group(1).replace(' ', '').replace('=', '').replace(',', '.')
                print('summ', summ)
                break
    return date_time,  summ
    
    
def parse_text(text):
    
    list = text.split(' ')
    if len(list) > 1:
        return list[0],  list[1]
    list = text.split('&')
    if len(list) > 1:
        temp_datetime = '%Y%m%dT%H%M'
        str_date_time = list[0].replace('t=', '')
        if len(str_date_time.split('T')[1]) == 6:
            temp_datetime = '%Y%m%dT%H%M%S'
        date_time = datetime.strptime(str_date_time, temp_datetime)
        summ = float(list[1].replace('s=', ''))
    return date_time,  summ
    
    
if __name__ == "__main__":
    scan()
    
