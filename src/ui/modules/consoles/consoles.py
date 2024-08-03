from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

class Consoles(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
        
    def setupUi(self):
        loadUi("src/modules/consoles/consoles.ui", self)
        self.showMaximized()
        self.raise_()
        
    