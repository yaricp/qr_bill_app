import os
import cv2
from pyzbar.pyzbar import decode

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


def recognize_image(image_file_path: str) -> str | None:
    logger.info(f"image_file_path: {image_file_path}")
    image = cv2.imread(image_file_path)
    logger.info(f"image: {image}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    list_decoded = decode(gray)
    if list_decoded:
        return parse_qr_code(list_decoded)
    list_decoded, adj_img = adjust_and_decode(gray)
    if list_decoded:
        return parse_qr_code(list_decoded)
    return None


def adjust_and_decode(gray):
    list_decoded = None
    for i in range(127, 160):
        logger.info(f"i: {i}")
        (thresh, blackAndWhiteImage) = cv2.threshold(gray, i, 255, cv2.THRESH_BINARY)
        cv2.imwrite("image_processed.png", blackAndWhiteImage)
        cv2.imwrite("image_gray.png", gray)
        list_decoded = decode(blackAndWhiteImage)
        if list_decoded:
            logger.info(f"list_decoded: {list_decoded}")
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
    url = None
    for rec in list_decoded:
        logger.info(f"TYPE_CODE: {rec.type}")
        type_data = rec.type
        if type_data == 'QRCODE':
            url = rec.data.decode("utf-8")
            logger.info(f"url: {url}")
    return url
