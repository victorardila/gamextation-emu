from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from src.views.menu.main_menu import MainMenu
from src.views.submenu.submenu import SubMenu

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
        self.layout_views = self.centralWidget().findChild(QStackedWidget, "layout_views")

        # Configuración de los widgets
        self.mainMenu = MainMenu()
        self.submenu = SubMenu()
        
        # Añadir los widgets al QStackedWidget
        self.layout_views.addWidget(self.mainMenu)
        self.layout_views.addWidget(self.submenu)
        
        # Mostrar el widget inicial
        self.ShowWidget(self.mainMenu)
        
        # Configurar botones para cambiar entre widgets
        self.initNavigationButtons()

    def initNavigationButtons(self):
        pass
        
    # Método para mostrar los widgets dentro del contenedor principal
    def ShowWidget(self, widget):
        self.layout_views.setCurrentWidget(widget)
        self.layout_views.raise_()
