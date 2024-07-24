from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

class SubMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.InitGUI()

    def InitGUI(self):
        loadUi("src/views/submenu/submenu.ui", self)
        