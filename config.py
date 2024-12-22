import os


ROOT = os.path.dirname(__file__)
LANG = 'eng+ara'
FILE = "media/PDF/report_1.pdf"


log = True
tesseract_cmd = "bin/Tesseract-OCR/tesseract.exe"
poppler_path = "bin/pdfInfo/poppler-24.08.0/Library/bin/"
owner = "byte-engineer"
DBG = True

QSS = open("style.qss", 'r').read()
QSS_warn = open("warn.qss", 'r').read()
