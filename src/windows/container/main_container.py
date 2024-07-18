from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi

class MainContainer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitGUI()

    def InitGUI(self):
        loadUi("src/windows/container/main_container.ui", self)
        # Configuración de la ventana
        self.showMaximized()
        self.setWindowTitle("GameXtation")
        self.setWindowIcon(QIcon("src/assets/ico/icon.png"))
        