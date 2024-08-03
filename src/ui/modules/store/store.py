from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

class Store(QWidget):
    def __init__(self, parent=None):
        super(Store, self).__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        loadUi("src/modules/store/store.ui", self)
        self.showMaximized()
        self.raise_()