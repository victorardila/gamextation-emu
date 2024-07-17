from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitMainMenu()

    def InitMainMenu(self):
        loadUi("src/views/main_menu_dark.ui", self)
        self.showMaximized()