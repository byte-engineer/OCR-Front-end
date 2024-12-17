from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
import time

class WorkerThread(QThread):
    progress_updated = pyqtSignal(int)  # Signal to update the progress bar
    
    def run(self):
        """Simulate a long-running task."""
        for i in range(1, 101):  # Simulate progress from 1 to 100
            time.sleep(0.1)  # Simulate work
            self.progress_updated.emit(i)  # Emit progress value

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Progress Bar with Thread")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        
        self.start_button = QPushButton("Start Long Task")
        self.start_button.clicked.connect(self.start_long_task)
        
        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.start_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.worker = WorkerThread()
        self.worker.progress_updated.connect(self.update_progress)
    
    def start_long_task(self):
        self.start_button.setEnabled(False)  # Disable button during task
        self.worker.start()  # Start the worker thread
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
        if value == 100:
            self.start_button.setEnabled(True)  # Re-enable button when task is done

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
