from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from src.views.intro import Intro
from PyQt5.uic import loadUi

class MainContainer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitGUI()

    def InitGUI(self):
        loadUi("src/windows/container/main_container.ui", self)
        # Configuración de la ventana
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showMaximized()
        self.setWindowTitle("GameXtation")
        self.setWindowIcon(QIcon("src/assets/ico/icon.png"))
        self.centralWidget = QWidget()
        self.centralLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.centralLayout)
        self.setCentralWidget(self.centralWidget)
        self.show()
        self.InitViews()
        
    def InitViews(self):
        # cargar el widget Intro en el contenedor central
        self.intro = Intro()
        self.centralLayout.addWidget(self.intro)
        self.intro.show()
        print("Vista Intro cargada")