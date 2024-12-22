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

        layout = QVBoxLayout()
        container.setLayout(layout)

        # File input
        path_layout = QHBoxLayout()
        self.path_in = QLineEdit()
        self.path_in.setPlaceholderText("Enter valid Image path")
        self.path_in.textChanged.connect(self.update_path)
        path_layout.addWidget(self.path_in, 4)

        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(lambda:self.browse_path("*.png *.jpeg *jpg "))
        path_layout.addWidget(browse_button, 1)
        layout.addLayout(path_layout)



        # Start Button
        self.img_start_btn = QPushButton("start")
        layout.addWidget(self.img_start_btn)


    def update_path(self):
        """
        Update the file path from the input field.
        """
        self.PATH = self.path_in.text().strip(' \'"')

    def browse_path(self, target):
        """
        Open a file dialog to select a PDF file.
        """
        file_name, _ = QFileDialog.getOpenFileName(self, f'Select {target}', '', f'Files ({target})')
        self.path_in.setText(file_name)

    def start_ocr_pdf(self):
        """
        Start the OCR process in a separate thread.
        """
        self.progress_bar.setValue(0)
        self.lbl_prog.setText("Processing PDF...")
        self.lock_input()

        self.validate_path(".pdf")
        

        # Initialize and start the worker thread
        self.worker = threads.WorkerThread_pdf(self.PATH)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.complete_ocr)
        self.worker.start()


    def validate_path(self, target):
        if not self.PATH or not os.path.exists(self.PATH):
            warning_box = msg.Warning("Select valid file")
            warning_box.set_custom_message("This file does NOT exist.")
            warning_box.exec()
            self.unlock_input()
            return

        elif not self.PATH:
            warning_box = msg.Warning("path is required")
            warning_box.set_custom_message(f"you have to browse to a valid {target} file")
            warning_box.exec()
            self.unlock_input()

        elif not self.PATH.endswith(f'{target}'): 
            warning_box = msg.Warning("path is required")
            warning_box.set_custom_message(f"you have to browse to a valid {target} file")
            warning_box.exec()
            self.unlock_input()
            return


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
        self.lbl_prog.setText(message)

    def unlock_input(self):
        self.start_button.setEnabled(True)
        self.path_in.setEnabled(True)


    def lock_input(self):
        self.start_button.setEnabled(False)
        self.path_in.setEnabled(False)



if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
