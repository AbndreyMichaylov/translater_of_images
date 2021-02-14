



tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

print(pytesseract.image_to_string(Image.open('kek.jpg'), lang='eng'))