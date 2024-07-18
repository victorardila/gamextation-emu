from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

class Consoles(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitViewsContainer()
        
    def InitViewsContainer(self):
        loadUi("src/views/consoles.ui", self)
        self.showMaximized()
        self.raise_()
        
    