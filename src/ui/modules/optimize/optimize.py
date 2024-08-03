from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

class Optimize(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
        
    def setupUi(self):
        loadUi("src/modules/optimize/optimize.ui", self)
        self.showMaximized()