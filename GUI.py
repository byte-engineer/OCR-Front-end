import PIL.Image
from pdf2image import convert_from_path
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QProgressBar, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QWidget, QHBoxLayout, QTabWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import pytesseract
import os
import config as con
import PIL
import msg
import threads



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.PATH = ""
        self.worker = None
        self.init_ui()

    def init_ui(self):
        """
        Initialize the main window UI.
        """
        self.setWindowTitle(f"OCR - {con.owner}")
        self.setGeometry(300, 300, 400, 200)
        self.setFixedSize(400, 200)
        self.setStyleSheet(con.QSS)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.pdf_tab()
        self.image_tap()

    def pdf_tab(self):
        # Layouts
        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.tabs.addTab(container, "PDF")

        # Progress label
        self.lbl_prog = QLabel("Pages: (0/0)")
        layout.addWidget(self.lbl_prog)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # File input
        path_layout = QHBoxLayout()
        self.path_in = QLineEdit()
        self.path_in.setPlaceholderText("Enter PDF path")
        self.path_in.textChanged.connect(self.update_path)
        path_layout.addWidget(self.path_in, 4)

        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(lambda:self.browse_path("*.pdf"))
        path_layout.addWidget(browse_button, 1)
        layout.addLayout(path_layout)

        # Start button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_ocr_pdf)
        layout.addWidget(self.start_button)


    def image_tap(self):
        container = QWidget()
        self.tabs.addTab(container, "Image")


    def update_path(self):
        """
        This function Called when the self.path_in changed
        """
        self.PATH = self.path_in.text().strip(' \'"')
        print(f"path updated: {self.PATH}\n" if con.DBG else "", end="")


    def browse_path(self, target):
        file_name, _ = QFileDialog.getOpenFileName(self, f'Select {target}', '', f'Files ({target})')
        self.path_in.setText(file_name)
        self.update_path()


    def start_ocr_pdf(self):
        """
        Start the OCR process in a separate thread.
        """
        if self.validate_path(".pdf"):

            self.progress_bar.setValue(0)
            self.lbl_prog.setText("Processing PDF...")
            self.lock_input()

            # Initialize and start the worker thread
            self.worker = threads.WorkerThread_pdf(self.PATH)
            self.worker.progress.connect(self.update_progress)
            self.worker.finished.connect(self.complete_ocr)
            self.worker.start()

        else:
            self.lbl_prog.setText("something want Wrong!")
        
    
    def validate_path(self, target):
    
        if not self.PATH:
            print("self.PATH = False" if con.DBG else "", end="")
            self.unlock_input()
            warning_box = msg.Warning("path is required")
            warning_box.set_custom_message(f"you have to browse to a valid {target} file")
            warning_box.exec()
            False

        elif not os.path.isfile(self.PATH) or not os.path.exists(self.PATH):
            print("not a file OR DNE" if con.DBG else "", end="")
            warning_box = msg.Warning("Select valid file")
            warning_box.set_custom_message("This file does NOT exist.")
            self.unlock_input()
            warning_box.exec()
            return False


        elif not self.PATH.endswith(f'{target}'):
            print("PATH does Not end with target" if con.DBG else "", end="")
            self.unlock_input()
            warning_box = msg.Warning("path is required")
            warning_box.set_custom_message(f"you have to browse to a valid {target} file")
            warning_box.exec()
            return False
        
        return True


    def update_progress(self, current, total):
        """
        Update the progress bar and label.
        """
        self.lbl_prog.setText(f"Pages: ({current}/{total})")
        self.progress_bar.setValue(current * 100 // total)

    def complete_ocr(self, message):
        """
        Handle completion of the OCR process.
        """
        self.unlock_input()
        self.progress_bar.setValue(0)
        self.path_in.setText("") 
        self.lbl_prog.setText(message)


    def unlock_input(self):
        self.start_button.setEnabled(True)
        self.path_in.setEnabled(True)
        self.path_in.selectAll()

    def lock_input(self):
        self.start_button.setEnabled(False)
        self.path_in.setEnabled(False)



if __name__ == '__main__':

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
