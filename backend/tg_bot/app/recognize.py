import os
import cv2
from datetime import datetime
from pyzbar.pyzbar import decode

from config import tg_bot_config
from utils import get_logger


logger = get_logger(__name__)


def recognize_video():
    video_file_path = os.path.join("temp_files", "qrcode.mp4")
    vidcap = cv2.VideoCapture(video_file_path)
    success, image = vidcap.read()
    while success:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        list_decoded = decode(gray)
        success, image = vidcap.read()
        if list_decoded:
            date_time, summ = parse_qr_code(list_decoded)
            return date_time, summ, False
    vidcap = cv2.VideoCapture(video_file_path)
    success, image = vidcap.read()
    while success:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        list_decoded, adj_img = adjust_and_decode(gray)
        success, image = vidcap.read()
        if list_decoded:
            date_time, summ = parse_qr_code(list_decoded)
            return date_time, summ, False
    return None, None, True


def recognize_image(image_file_path: str) -> tuple:
    # image_file_path = os.path.join("temp_files", "qrcode.mp4")
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
        cv2.imwrite("image_processed.png", blackAndWhiteImage)
        cv2.imwrite("image_gray.png", gray)
        list_decoded = decode(blackAndWhiteImage)
        if list_decoded:
            break
    return list_decoded, blackAndWhiteImage
    

# def scan(user='251241715', image=False, video=True):
#     date_time = None
#     summ = None
#     raw = False
#     if image:
#         date_time, summ, raw = recognize_image(user) 
#     if video:
#         date_time, summ, raw = recognize_video()
#     return date_time, summ, raw
        

def parse_qr_code(list_decoded):
    date_time = None
    summ = None
    for rec in list_decoded:
        logger.info(f"TYPE_CODE: {rec.type}")
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
