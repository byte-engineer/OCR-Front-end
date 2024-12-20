from pdf2image import convert_from_path
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QProgressBar, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import pytesseract
import os
import config as con


class WorkerThread(QThread):
    progress = pyqtSignal(int, int)  # Emits current progress and total pages
    finished = pyqtSignal(str)      # Emits completion message

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        try:
            images = self.pdf_to_images(self.path)
            total_images = len(images)
            self.extract_text_from_images(images, total_images)
        except Exception as e:
            self.finished.emit(f"Error: {str(e)}")

    def pdf_to_images(self, path):
        """
        Convert the given PDF to a list of images.
        """
        pytesseract.pytesseract.tesseract_cmd = con.tesseract_cmd
        images = convert_from_path(path, dpi=200, poppler_path=con.poppler_path)
        return images

    def extract_text_from_images(self, images, total_images):
        """
        Extract text from images and save to a text file.
        """
        output_path = os.path.splitext(self.path)[0] + ".txt"
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write('')  # Clear the file

        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang=con.LANG)
            self.progress.emit(i + 1, total_images)
            with open(output_path, 'a', encoding='utf-8') as file:
                file.write(f"\n\n{'*' * 30} ( Page {i + 1} ) {'*' * 30}\n\n{text}")

        self.finished.emit("OCR process completed.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.PATH = ''
        self.worker = None
        self.init_ui()

    def init_ui(self):
        """
        Initialize the main window UI.
        """
        self.setWindowTitle(f"OCR - {con.owner}")
        self.setGeometry(300, 300, 400, 180)
        self.setFixedSize(400, 180)
        self.setStyleSheet(con.QSS)

        # Layouts
        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

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
        browse_button.clicked.connect(self.browse_path)
        path_layout.addWidget(browse_button, 1)
        layout.addLayout(path_layout)

        # Start button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_ocr)
        layout.addWidget(self.start_button)

    def update_path(self):
        """
        Update the file path from the input field.
        """
        self.PATH = self.path_in.text().strip(' \'"')

    def browse_path(self):
        """
        Open a file dialog to select a PDF file.
        """
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select PDF', '', 'PDF Files (*.pdf)')
        self.path_in.setText(file_name)

    def start_ocr(self):
        """
        Start the OCR process in a separate thread.
        """
        self.progress_bar.setValue(0)
        self.lbl_prog.setText("Processing PDF...")
        self.start_button.setEnabled(False)

        if not self.PATH or not os.path.exists(self.PATH):
            QMessageBox.warning(self, "Error", "Please select a valid PDF file.")
            self.start_button.setEnabled(True)
            return

        # Initialize and start the worker thread
        self.worker = WorkerThread(self.PATH)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.complete_ocr)
        self.worker.start()

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
        self.start_button.setEnabled(True)
        self.progress_bar.setValue(0)
        self.lbl_prog.setText(message)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
