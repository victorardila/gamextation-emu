from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from src.views.main_menu import MainMenu
from src.views.consoles import Consoles

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

        # Acceder al QStackedWidget dentro de centralWidget
        self.stackedWidget = self.centralWidget().findChild(QStackedWidget, "stackedWidget")

        # Configuración de los widgets
        self.mainMenu = MainMenu()
        self.consoles = Consoles()
        
        # Añadir los widgets al QStackedWidget
        self.stackedWidget.addWidget(self.mainMenu)
        self.stackedWidget.addWidget(self.consoles)
        
        # Mostrar el widget inicial
        self.ShowWidget(self.mainMenu)
        
        # Configurar botones para cambiar entre widgets
        self.initNavigationButtons()

    def initNavigationButtons(self):
        pass
        
    # Método para mostrar los widgets dentro del contenedor principal
    def ShowWidget(self, widget):
        self.stackedWidget.setCurrentWidget(widget)
        self.stackedWidget.raise_()
