from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSize
from PyQt5.uic import loadUi
from src.components.buttons.button_icon import ButtonIcon
from qtawesome import icon

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitMainMenu()

    # Colores de fondo para el modo dark y light
    # Color de fondo dark: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.026178 rgba(255, 95, 1, 255), stop:0.219895 rgba(255, 96, 0, 255), stop:0.424084 rgba(219, 67, 2, 255), stop:0.715789 rgba(99, 0, 34, 255), stop:0.826316 rgba(93, 0, 33, 255), stop:1 rgba(33, 0, 19, 255));
    # Color de fondo light: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.026178 rgba(249, 135, 11, 255), stop:0.219895 rgba(247, 134, 12, 255), stop:0.424084 rgba(241, 139, 11, 255), stop:0.715789 rgba(233, 150, 10, 255), stop:0.826316 rgba(232, 155, 13, 255), stop:1 rgba(235, 154, 11, 255));
    
    def InitMainMenu(self):
        loadUi("src/views/main_menu.ui", self)
        self.showMaximized()
        # Le doy color de fondo gradiente a la ventana con el estilo dark por defecto
        self.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.026178 rgba(255, 95, 1, 255), stop:0.219895 rgba(255, 96, 0, 255), stop:0.424084 rgba(219, 67, 2, 255), stop:0.715789 rgba(99, 0, 34, 255), stop:0.826316 rgba(93, 0, 33, 255), stop:1 rgba(33, 0, 19, 255));")
        self.button_icon_user = ButtonIcon()
        self.button_icon_mode = ButtonIcon()
        # icono usuario
        self.button_icon_user.setIcon(icon('fa.user', color='white'))
        self.button_icon_user.setIconSize(QSize(32, 32))
        self.button_icon_user.setToolTip("Usuario")
        # icono modo oscuro
        self.button_icon_mode.setIcon(icon('fa5s.moon', color='white'))
        self.button_icon_mode.setIconSize(QSize(32, 32))
        self.button_icon_mode.setToolTip("Modo oscuro")
        
        # Añadir el botón al layout horizontalLayout_buttons_topbar
        self.horizontalLayout_buttons_topbar.addWidget(self.button_icon_mode)
        self.horizontalLayout_buttons_topbar.addWidget(self.button_icon_user)
        
        