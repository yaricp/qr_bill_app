import qrtools
qr = qrtools.QR()
qr.decode("QRCode1.png")
#qr.decode("test.jpg")
print( qr.data)