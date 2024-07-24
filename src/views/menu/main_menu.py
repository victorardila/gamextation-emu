from PyQt5.QtWidgets import QWidget, QSizePolicy, QStackedWidget
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.uic import loadUi
from src.components.animation.animation_ppsspp import AnimationPPSSPP
from src.views.menu.overlay.overlay_content import OverlayContent

class MainMenu(QWidget):
    menu_button_clicked = pyqtSignal(str)  # Señal para indicar que un botón del menú ha sido presionado

    def __init__(self):
        super().__init__()
        self.init_main_menu()
        
    BG_COLOR_DARK = (
        "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(34, 34, 34, 255), stop:0.5 rgba(40, 40, 40, 255), "
        "stop:0.75 rgba(50, 50, 50, 255), stop:1 rgba(34, 34, 34, 255));"
    )
    BG_COLOR_LIGHT = (
        "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
        "stop:0.026178 rgba(249, 135, 11, 255), stop:0.219895 rgba(247, 134, 12, 255), "
        "stop:0.424084 rgba(241, 139, 11, 255), stop:0.715789 rgba(233, 150, 10, 255), "
        "stop:0.826316 rgba(232, 155, 13, 255), stop:1 rgba(235, 154, 11, 255));"
    )
    
    def init_main_menu(self):
        loadUi("src/views/menu/main_menu.ui", self)
        self.showMaximized()
        self.setStyleSheet(f"background-color: {self.BG_COLOR_DARK}")
        self.init_overlay_widget()
        self.init_animation_menu()
        # Asegurarse de que los widgets dentro del layout_widgets se expanden adecuadamente
        if isinstance(self.layout_widgets, QStackedWidget):
            for widget in self.layout_widgets.findChildren(QWidget):
                widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def init_animation_menu(self):
        self.animation = AnimationPPSSPP()
        self.animation.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout_widgets.addWidget(self.animation)
        self.animation.show()
        
    def init_overlay_widget(self):
        self.overlay = OverlayContent()
        self.layout_widgets.addWidget(self.overlay)
        self.overlay.show()
        # Conectar la señal theme_changed al método change_bg_color
        self.overlay.theme_changed.connect(self.change_bg_color)
        # Conectar la señal menu_button_clicked al método handle_menu_button_clicked
        self.overlay.menu_button_clicked.connect(self.handle_menu_button_clicked)
        
    def change_bg_color(self):
        if self.styleSheet() == f"background-color: {self.BG_COLOR_DARK}":
            is_dark_mode = True  # Cambiar esto según el tema actual
            self.setStyleSheet(f"background-color: {self.BG_COLOR_LIGHT}")
            self.overlay.button_icon_mode.style('fa5s.moon', QSize(32, 32), "Modo oscuro", 'gray')
            self.animation.update_icon_color(is_dark_mode)
        else:
            is_dark_mode = False  # Cambiar esto según el tema actual
            self.setStyleSheet(f"background-color: {self.BG_COLOR_DARK}")
            self.overlay.button_icon_mode.style('fa5s.sun', QSize(32, 32), "Modo claro", 'white')
            self.animation.update_icon_color(is_dark_mode)

    def handle_menu_button_clicked(self, tooltip):
        self.menu_button_clicked.emit(tooltip)