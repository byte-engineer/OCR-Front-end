import PyQt5.QtWidgets as wdg



class img(wdg.QMainWindow):

    def __init__(self):
        super().__init__()

        self.UI()


    def UI(self):
        container = wdg.QWidget()
        layout = wdg.QVBoxLayout()
        container.setLayout(layout)
        
        # prograss label
        prograss_lbl = wdg.QLabel("prograss")
        layout.addWidget(prograss_lbl)

        # Input (line edit)
        input_layout = wdg.QHBoxLayout()
        layout.addLayout(input_layout)
        self.path_in = wdg.QLineEdit()
        self.path_in.setPlaceholderText("Image Path here")
        input_layout.addWidget(self.path_in)