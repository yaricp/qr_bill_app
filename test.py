import qrtools
qr = qrtools.QR()
qr.decode("test.png")
print qr.data