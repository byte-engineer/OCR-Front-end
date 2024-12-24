from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QPushButton, QLabel, QWidget
import config as con




class Error(QMessageBox):
    def __init__(self, msg):
        super().__init__()
        self.setFixedHeight(60)

        self.setIcon(QMessageBox.Icon.Warning)
        self.setWindowTitle("Error")
        self.setStyleSheet(con.QSS_warn)

        layout = QVBoxLayout()

        cotainer = QWidget()
        cotainer.setLayout(layout)

        self.setText(msg)
