from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QPushButton, QLabel
import config as con




class Warning(QMessageBox):
    def __init__(self, msg):
        super().__init__()

        self.setIcon(QMessageBox.Icon.Warning)
        self.setWindowTitle("Error")
        self.setStyleSheet(con.QSS_warn)

        layout = QVBoxLayout()

        label = QLabel(msg)


        layout.addWidget(label)

        button = QPushButton("OK")
        button.clicked.connect(self.accept)
        layout.addWidget(button)

        self.setLayout(layout)

    def set_custom_message(self, message):
        self.findChild(QLabel).setText(message)

