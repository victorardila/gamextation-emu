import os
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

class Intro(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        loadUi("src/views/intro.ui", self)
        # Cambiar color de fondo de la ventana
        self.setStyleSheet("background-color: #000;")
