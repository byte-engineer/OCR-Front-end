from PyQt5.QtWidgets import  QVBoxLayout, QProgressBar, QLabel, QLineEdit, QPushButton, QFileDialog, QWidget, QHBoxLayout, QCheckBox
import os
import config as con
import msg
import threads
from PyQt5.QtCore import Qt


class PDF_tab(QWidget):
    def __init__(self):
        super().__init__()
        self.PATH = ""
        self.LANG = "ara+eng"
        self.worker = None
        self.UI()
        # self.init_settings()


    def UI(self):
        # Layouts
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Lang ckeck boxs
        container = QWidget()
        container.setObjectName("Container")
        container.setStyleSheet("#Container { border: 1px solid black; padding: 5px; border-radius: 10%; }")
        ckeck_boxs = QVBoxLayout()
        container.setLayout(ckeck_boxs)

        self.eng_ckeck = QCheckBox()
        self.ara_ckeck = QCheckBox()

        self.eng_ckeck.setText("english")
        self.ara_ckeck.setText("arabic")        

        self.eng_ckeck.setObjectName("eng")
        self.ara_ckeck.setObjectName("ara")
        
        self.boxs_list = [self.ara_ckeck, self.eng_ckeck]

        for box in self.boxs_list:
            box.stateChanged.connect(self.setLang)
            box.setCheckState(Qt.CheckState.Checked)
            ckeck_boxs.addWidget(box)
        self.setLang()

        # Progress label
        lbl_layout = QHBoxLayout()
        self.lbl_prog = QLabel("Pages: (0/0)")
        lbl_layout.addWidget(self.lbl_prog, 2)
        lbl_layout.addWidget(container, 1)
        layout.addLayout(lbl_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # File input
        path_layout = QHBoxLayout()
        self.path_in = QLineEdit()
        self.path_in.setPlaceholderText("Enter PDF path")
        self.path_in.textChanged.connect(self.update_path)
        self.path_in.setFocus(True)
        path_layout.addWidget(self.path_in, 4)

        # Browse Button
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(lambda: self.browse_path("*.pdf"))
        path_layout.addWidget(browse_button, 1)
        layout.addLayout(path_layout)

        # Start button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_ocr_pdf)
        layout.addWidget(self.start_button)


    def setLang(self):
        lang = "+".join([box.objectName() for box in self.boxs_list if box.isChecked()])

        # Chech if there is no box cheched.
        if lang:
            self.LANG = lang
            print(f"LANG: {self.LANG}\n" if con.DBG else "", end="")


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
        if self.validate_path(".pdf"):

            self.progress_bar.setValue(0)
            self.lbl_prog.setText("Processing PDF...")
            self.lock_input()

            # Initialize and start the worker thread
            self.worker = threads.WorkerThread_pdf(self.PATH, self.LANG)
            self.worker.progress.connect(self.update_progress)
            self.worker.finished.connect(self.complete_ocr)
            self.worker.start()

        else:
            self.lbl_prog.setText("something want Wrong!")
        
    
    def validate_path(self, target):

        if not self.PATH:
            print("self.PATH = False\n" if con.DBG else "", end="")
            self.unlock_input()
            warning_box = msg.Error("path is required")
            warning_box.exec()
            False

        elif not os.path.isfile(self.PATH) or not os.path.exists(self.PATH):
            print("not a file OR DNE\n" if con.DBG else "", end="")
            warning_box = msg.Error("This file does NOT exist.")
            self.unlock_input()
            warning_box.exec()
            return False


        elif not self.PATH.endswith(f'{target}'):
            print("PATH does Not end with target\n" if con.DBG else "", end="")
            self.unlock_input()
            warning_box = msg.Error("path is required")
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
