import qrcode

url = "http://10.155.92.184:5000"

qr = qrcode.make(url)

qr.save("attendance_qr.png")

print("QR code successfully created!")
print("URL:", url)