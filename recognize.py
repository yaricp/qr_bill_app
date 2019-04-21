import os
from datetime import datetime
from pyzbar.pyzbar import decode
from PIL import Image

from config import *

def scan():
    list_decoded = decode(Image.open(os.path.join(PATH_TEMP_FILES,'qrcode.jpg')))
    for rec in list_decoded:
        type_data = rec.type
        if type_data == 'QRCODE':
            list_data = rec.data.decode("utf-8").split('&')
            date_time = datetime.strptime(list_data[0].replace('t=', ''), '%Y%m%dT%H%M%S').date()
            summ = float(list_data[1].replace('s=', ''))
    return date_time, summ
