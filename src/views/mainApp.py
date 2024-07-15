from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from . import *

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("src/views/MainApp.ui",self)
        self.showMaximized()