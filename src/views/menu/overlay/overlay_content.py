from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.uic import loadUi
from qtawesome import icon
from PyQt5.QtGui import QFont, QFontDatabase
from datetime import datetime

class OverlayContent(QWidget):
    def __init__(self):
        super().__init__()
        self.InitMainMenu()
        
    def InitMainMenu(self):
        loadUi("src/views/menu/overlay/overlay_content.ui", self)
        self.showMaximized()
        self.setStyleSheet("background-color: transparent;")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.content_menu()
        
    def content_menu(self):
        # Cargar la fuente personalizada
        font_id = QFontDatabase.addApplicationFont("src/assets/font/ratchet-clank-psp.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            custom_font = QFont(font_family, 24)
        else:
            custom_font = QFont("Arial", 18)  # Fuente por defecto si falla la carga

        # icono usuario
        self.button_icon_user.style(icon('fa.user', color='white'), QSize(32, 32), "Usuario")
        # icono modo oscuro
        self.button_icon_mode.style(icon('fa5s.sun', color='white'), QSize(32, 32), "Modo claro")
        self.button_icon_search.style(icon('fa.search', color='white'), QSize(32, 32), "Buscar")
        # label hora
        self.label_hour.style("00:00:00 AM", "white", 24, custom_font, Qt.AlignCenter)

        # Configurar el QTimer para actualizar la hora cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Actualizar cada 1000 ms (1 segundo)

        # Actualizar la hora al iniciar
        self.update_time()

    def update_time(self):
        current_time = datetime.now().strftime("%I:%M:%S %p")
        self.label_hour.setText(current_time)
    