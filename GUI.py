from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
import config as con
import pdf_tab



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
        self.setGeometry(300, 300, con.WIDTH, con.HEIGHT)
        self.setFixedSize(con.WIDTH, con.HEIGHT)
        self.setStyleSheet(con.QSS)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.addTab(pdf_tab.PDF_tab(), "PDF")


if __name__ == '__main__':

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
