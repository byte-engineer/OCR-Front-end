import PyQt5.QtWidgets as wdg
from PyQt5 import QtCore
import OCR
# from pdf2image import convert_from_path
import pytesseract
import os
import config as con



class WorkerThread(QtCore.QThread):
    progress = QtCore.pyqtSignal(int, int)  # Emit both current and total
    finished = QtCore.pyqtSignal(str)  # Emit the extracted text

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        images = OCR.pdf_to_images(self.path)
        total_images = len(images)
        self.imgs_to_text(images, total_images)




        # extracted_text = self.imgs_to_text(images, total_images)
        # # OCR.w_to_txt(extracted_text, os.path.splitext(self.path)[0]+".txt")
        # self.finished.emit(extracted_text)




    def imgs_to_text(self, images, total_images, path =None):


        if path is None:
            path = os.path.splitext(self.path)[0]+".txt"
        
        with open(path, 'w') as file:
            file.write('')                        # Clear the file.


        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang=con.LANG)

            self.progress.emit(i + 1, total_images)

            with open(path, 'ab') as file:
                file.write(bytes(f"\n\n{'*' * 30} ( Page {i + 1} ) {'*' * 30}\n\n\n {text}", 'utf-8'))


        self.finished.emit("Finished...")




    def _imgs_to_text(self, images, total_images):
        extracted_text = ""
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang=con.LANG)

            # Emit progress: current index and total images
            self.progress.emit(i + 1, total_images)

            extracted_text += f"\n\n{'*' * 30} ( Page {i + 1} ) {'*' * 30}\n\n\n" + text

        return extracted_text


class Main(wdg.QMainWindow):
    def __init__(self):
        super().__init__()
        self.PATH = ''
        self.worker = None
        self.UI()

    def UI(self):
        self.setStyleSheet(open('style.qss').read())
        self.setGeometry(300, 300, 400, 150)
        self.setWindowTitle("OCR-Ahmed")

        layout = wdg.QVBoxLayout()
        container = wdg.QWidget()
        self.setCentralWidget(container)
        container.setLayout(layout)


        self.lbl_prog = wdg.QLabel("Pages: (0/0)")
        layout.addWidget(self.lbl_prog)

        # Progress bar
        self.waiting_bar = wdg.QProgressBar()
        self.waiting_bar.setValue(0)
        layout.addWidget(self.waiting_bar)

        # File path input
        path_layout = wdg.QHBoxLayout()
        layout.addLayout(path_layout)

        self.path_in = wdg.QLineEdit()
        self.path_in.setPlaceholderText("Enter PDF path")
        self.path_in.textChanged.connect(self.path_changed)
        path_layout.addWidget(self.path_in, 4)

        brws_btn = wdg.QPushButton("Browse...")
        brws_btn.clicked.connect(self.srch_for_path)
        path_layout.addWidget(brws_btn, 1)

        # Start button
        self.strt_btn = wdg.QPushButton("Start")
        self.strt_btn.clicked.connect(self.Start)
        layout.addWidget(self.strt_btn)

    def path_changed(self):
        self.PATH = self.path_in.text().strip(' \'"')

    def srch_for_path(self):
        file_name, _ = wdg.QFileDialog.getOpenFileName(self, 'Select PDF', '', 'PDF Files (*.pdf)')
        self.path_in.setText(file_name)

    def Start(self):


        self.waiting_bar.setValue(0)
        self.lbl_prog.setText("Turning PDF to images")
        self.strt_btn.setEnabled(False)
        

        if not self.PATH:
            wdg.QMessageBox.warning(self, "Error", "Please select a valid PDF file.")
            return

        # Initialize and start the worker thread
        self.worker = WorkerThread(self.PATH)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.display_result)
        self.worker.start()

    def update_progress(self, current, total):

        self.lbl_prog.setText(f"Images: ({current}/{total})")

        self.waiting_bar.setValue(current * 100 // total)

    def display_result(self, text):
        self.strt_btn.setEnabled(True)
        self.waiting_bar.setValue(0)
        self.lbl_prog.setText("Finished...")



if __name__ == '__main__':
    app = wdg.QApplication([])
    win = Main()
    win.show()
    app.exec_()
