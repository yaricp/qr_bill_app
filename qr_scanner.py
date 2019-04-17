import os
import qrtools

from config import *

qr = qrtools.QR()
print os.path.dirname(os.path.realpath(__file__))
print os.path.join(PATH_TEMP_FILES,'qrcode.jpg')
qr.decode(os.path.join(PATH_TEMP_FILES,'qrcode.jpg'))
with open(os.path.join(PATH_TEMP_FILES,'text.data'),'a+') as file:
    file.write(qr.data)
print( qr.data)