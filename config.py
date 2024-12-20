import os


ROOT = os.path.dirname(__file__)
LANG = 'eng+ara'
FILE = "media/PDF/report_1.pdf"


tesseract_cmd = "bin/Tesseract-OCR/tesseract.exe"
poppler_path = "bin/pdfInfo/poppler-24.08.0/Library/bin/"
owner = "encrypted-books"


QSS = \
"""
QMainWindow {
    background-color: #171717;
    border: 1px solid #000000;
}

QVBoxLayout {
    margin: 10px;
    border-color: #2c2c2c;
}

QProgressBar {
    color: #ffffff;
    border: 1px solid #000000;
    border-radius: 5px;
    text-align: center;
    background-color: #2c2c2c;
}

QLabel {
    font-size: 14px;
    color: #ffffff;
    margin-bottom: 5px;
}

QPushButton {
    background-color: #070707;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 5px;
    margin: 5px 0;
}

QPushButton:hover {
    background-color: #090909;
    border-top: 1px solid #0078D4;
    border-radius: 0px
}

QLineEdit {
    border: 1px solid #070707;
    background-color: #2c2c2c;
    color: white;
    padding: 5px;
    border-radius: 3px;
}

QLineEdit:focus {
    border-color: #070707;
}
"""