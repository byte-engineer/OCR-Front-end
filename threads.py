import pytesseract
from PyQt5.QtCore import QThread, pyqtSignal
import config as con
from pdf2image import convert_from_path
import os.path as path
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = con.tesseract_cmd



class WorkerThread_pdf(QThread):
    progress = pyqtSignal(int, int)
    finished = pyqtSignal(str)

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        try:
            images = self.pdf_to_images(self.path)
            total_images = len(images)
            self.imgs_to_txt(images, total_images)
        except Exception as e:
            self.finished.emit(f"Error: {str(e)}")

    def pdf_to_images(self, path):
        """
        Convert the given PDF to a list of images.
        """
        images = convert_from_path(path, dpi=200, poppler_path=con.poppler_path)
        return images

    def imgs_to_txt(self, images, total_images):
        """
        Extract text from images and save to a text file.
        """
        output_path = path.splitext(self.path)[0] + ".txt"
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write('')  # Clear the file

        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang=con.LANG)
            self.progress.emit(i + 1, total_images)

            # Append the text of each page speratelly.
            with open(output_path, 'a', encoding='utf-8') as file:
                file.write(f"\n\n{'*' * 30} ( Page {i + 1} ) {'*' * 30}\n\n{text}")
                    

        self.finished.emit("OCR process completed.")



class WorkerThread_img(QThread):

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.header = "Extracted text "

    def run(self):
        
        image = self.path_to_img()
        text = self.img_to_txt(image)
        self.writetxt(text)



    def path_to_img(self):
        return Image.open(self.path)


    def img_to_txt(self, image):
        """
        Extract text from images and save to a text file.
        """

        # Create a file to write the data if not exist.
        output_path = path.splitext(self.path)[0] + ".txt"
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write('')  # Clear the file

        # Append the text of each page speratelly.
        text = pytesseract.image_to_string(image, lang= con.LANG)
        with open(output_path, 'a', encoding='utf-8') as file:
            file.write(f"\n\n{'*' * 30} ( {self.header} ) {'*' * 30}\n\n{text}")

        if con.log:
            print(text)

        self.finished.emit("OCR process completed.")
        return text