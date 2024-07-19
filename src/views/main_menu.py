from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.uic import loadUi
from src.components.animation.animation_bg import AnimationBg
from qtawesome import icon
from PyQt5.QtGui import QFont, QFontDatabase, QMovie
from datetime import datetime

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitMainMenu()
        
    # Variable global
    bg_color_dak = "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.026178 rgba(255, 95, 1, 255), stop:0.219895 rgba(255, 96, 0, 255), stop:0.424084 rgba(219, 67, 2, 255), stop:0.715789 rgba(99, 0, 34, 255), stop:0.826316 rgba(93, 0, 33, 255), stop:1 rgba(33, 0, 19, 255));"
    bg_color_light = "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0.026178 rgba(249, 135, 11, 255), stop:0.219895 rgba(247, 134, 12, 255), stop:0.424084 rgba(241, 139, 11, 255), stop:0.715789 rgba(233, 150, 10, 255), stop:0.826316 rgba(232, 155, 13, 255), stop:1 rgba(235, 154, 11, 255));"
    
    def InitMainMenu(self):
        loadUi("src/views/main_menu.ui", self)
        self.showMaximized()
        self.setStyleSheet("background-color: " + self.bg_color_dak)
        # Aqui cargare la animacion bg al componente animation_bg que es widget 
        self.animation = AnimationBg()
        self.setCentralWidget(self.animation)
        
    #     # Cargar la fuente personalizada
    #     font_id = QFontDatabase.addApplicationFont("src/assets/font/ratchet-clank-psp.ttf")
    #     if font_id != -1:
    #         font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    #         custom_font = QFont(font_family, 24)
    #     else:
    #         custom_font = QFont("Arial", 18)  # Fuente por defecto si falla la carga

    #     # icono usuario
    #     self.button_icon_user.style(icon('fa.user', color='white'), QSize(32, 32), "Usuario")
    #     # icono modo oscuro
    #     self.button_icon_mode.style(icon('fa5s.sun', color='white'), QSize(32, 32), "Modo claro")
    #     self.button_icon_search.style(icon('fa.search', color='white'), QSize(32, 32), "Buscar")
    #     # label hora
    #     self.label_hour.style("00:00:00 AM", "white", 24, custom_font, Qt.AlignCenter)

    #     # Configurar el QTimer para actualizar la hora cada segundo
    #     self.timer = QTimer(self)
    #     self.timer.timeout.connect(self.update_time)
    #     self.timer.start(1000)  # Actualizar cada 1000 ms (1 segundo)

    #     # Actualizar la hora al iniciar
    #     self.update_time()

    # def update_time(self):
    #     current_time = datetime.now().strftime("%I:%M:%S %p")
    #     self.label_hour.setText(current_time)