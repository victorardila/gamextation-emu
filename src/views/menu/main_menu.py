from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize
from PyQt5.uic import loadUi
from src.components.animation.animation_ppsspp import AnimationPPSSPP
from src.views.menu.overlay.overlay_content import OverlayContent
from qtawesome import icon

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.InitMainMenu()
        
    # Variables globales para los colores de fondo
    bg_color_dak = "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.026178 rgba(255, 95, 1, 255), stop:0.219895 rgba(255, 96, 0, 255), stop:0.424084 rgba(219, 67, 2, 255), stop:0.715789 rgba(99, 0, 34, 255), stop:0.826316 rgba(93, 0, 33, 255), stop:1 rgba(33, 0, 19, 255));"
    bg_color_light = "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.026178 rgba(249, 135, 11, 255), stop:0.219895 rgba(247, 134, 12, 255), stop:0.424084 rgba(241, 139, 11, 255), stop:0.715789 rgba(233, 150, 10, 255), stop:0.826316 rgba(232, 155, 13, 255), stop:1 rgba(235, 154, 11, 255));"
    
    def InitMainMenu(self):
        loadUi("src/views/menu/main_menu.ui", self)
        self.showMaximized()
        self.setStyleSheet(f"background-color: {self.bg_color_dak}")
        self.animation_menu()
        self.overlay_widget()
        
    def animation_menu(self):
        # Crear la animación de PPSSPP
        self.animation = AnimationPPSSPP()
        # Añadir la animación al QStackedWidget
        self.layout_widgets.addWidget(self.animation)
        # Mostrar la animación
        self.animation.show()
        
    def overlay_widget(self):
        # Añado el widget superpuesto
        self.overlay = OverlayContent()
        # Añadir el widget superpuesto al QStackedWidget
        self.layout_widgets.addWidget(self.overlay)
        # Mostrar el widget superpuesto
        self.overlay.show()
        
    def change_bg_color(self):
        if self.styleSheet() == f"background-color: {self.bg_color_dak}":
            self.setStyleSheet(f"background-color: {self.bg_color_light}")
            self.button_icon_mode.style(icon('fa5s.moon', color='black'), QSize(32, 32), "Modo oscuro")
        else:
            self.setStyleSheet(f"background-color: {self.bg_color_dak}")
            self.button_icon_mode.style(icon('fa5s.sun', color='white'), QSize(32, 32), "Modo claro")