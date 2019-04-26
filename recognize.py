import os
from datetime import datetime
from pyzbar.pyzbar import decode
from PIL import Image
import pytesseract

from config import *

def scan():
    date_time = None
    summ = None
    list_decoded = decode(Image.open(os.path.join(PATH_TEMP_FILES,'qrcode.jpg')))
    print('LIST_DECODED: ', list_decoded)
    if list_decoded:
        for rec in list_decoded:
            print('TYPE_CODE: ', rec.type)
            type_data = rec.type
            if type_data == 'QRCODE':
                print('DATA: ', rec.data)
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
    else:
        raw_text = pytesseract.image_to_string(Image.open(os.path.join(PATH_TEMP_FILES,'qrcode.jpg')),
                                                lang=LANG)
        print('RAW_TEXT: ', raw_text)
    return date_time, summ
