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
        
        self.layout_views.addWidget(self.mainMenu)
        self.layout_views.addWidget(self.submenu)
        
        self.layout_views.setCurrentWidget(self.mainMenu)
        
        # Conectar la señal menu_button_clicked al método switch_to_submenu
        self.mainMenu.menu_button_clicked.connect(self.switch_to_submenu)
        self.submenu.menu_return_clicked.connect(self.switch_to_mainmenu)
        self.submenu.menu_exit_clicked.connect(self.close_aplication)

    def switch_to_submenu(self, message):
        # si message contiene la palabra Submenu cambiar a la vista submenu
        if "Submenu" in message:
            # Cambiar a la vista submenu y le pasamos el mensaje
            self.layout_views.setCurrentWidget(self.submenu)
            self.submenu.load_module(message)
        else:
            self.layout_views.setCurrentWidget(self.mainMenu)
    
    def switch_to_mainmenu(self):
        self.layout_views.setCurrentWidget(self.mainMenu)
    
    def close_aplication(self):
        self.close()