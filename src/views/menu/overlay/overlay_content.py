from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt5.uic import loadUi
from qtawesome import icon
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap, QPainter, QColor
from PyQt5.QtSvg import QSvgWidget
from datetime import datetime

class OverlayContent(QWidget):
    theme_changed = pyqtSignal()  # Señal para indicar el cambio de tema
    menu_button_clicked = pyqtSignal(str)  # Señal para indicar que un botón del menú ha sido presionado
    SVG_CREDITS = "src/assets/svg/icon.svg"
    
    def __init__(self):
        super().__init__()
        self.init_main_menu()
        
    IMAGES = [
        "src/assets/img/load_ROMs.png",
        "src/assets/img/select_console.png",
        "src/assets/img/store.png",
        "src/assets/img/media.png",
        "src/assets/img/user.png",
        "src/assets/img/settings.png",
        "src/assets/img/optimize.png",
        "src/assets/img/update.png",
        "src/assets/img/creator.png",
        "src/assets/img/about.png",
        "src/assets/img/exit.png",
    ]
    
    def init_main_menu(self):
        loadUi("src/views/menu/overlay/overlay_content.ui", self)
        self.setStyleSheet("background-color: transparent;")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.apply_top_bar_styles()
        self.apply_content_styles()
        
    def apply_top_bar_styles(self):
        custom_font = self.load_custom_font("src/assets/font/ratchet-clank-psp.ttf", 24, "Arial", 18)

        self.button_icon_user.style('fa.user', QSize(32, 32), "Usuario", 'white')
        self.button_icon_mode.style('fa5s.sun', QSize(32, 32), "Modo claro", 'white')
        self.button_icon_search.style('fa.search', QSize(32, 32), "Buscar", 'white')
        self.label_hour.style("00:00:00 AM", "white", 24, custom_font, Qt.AlignCenter)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Actualizar cada 1000 ms (1 segundo)

        self.update_time()

        # Conectar la señal de clic del botón de cambio de tema a la señal theme_changed
        self.button_icon_mode.clicked.connect(self.emit_theme_change)

    def load_custom_font(self, font_path, font_size, fallback_font, fallback_size):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            return QFont(font_family, font_size)
        else:
            return QFont(fallback_font, fallback_size)

    def update_time(self):
        current_time = datetime.now().strftime("%I:%M:%S %p")
        self.label_hour.setText(current_time)
        
    def apply_content_styles(self):
        self.frameMenuRowOne.setStyleSheet("background-color: transparent;")
        self.frameMenuRowTwo.setStyleSheet("background-color: transparent;")

        buttons = [
            self.button_load_roms, self.button_select_console, self.button_store, 
            self.button_media, self.button_user, self.button_settings, self.button_optimize,
            self.button_update, self.button_creator, self.button_about, self.button_logout
        ]

        tooltips = [
            "Juegos cargados", "Seleccionar consola", "Tienda", "Media", "Usuario",
            "Configuraciones", "Optimizar", "Actualizaciones", "Creador", "Acerca de", "Salir"
        ]

        for btn, image, tooltip in zip(buttons, self.IMAGES, tooltips):
            btn.style(image, QSize(250, 350), tooltip)
            btn.clicked.connect(lambda _, t=tooltip: self.emit_menu_button_clicked(t))  # Conectar clic a la señal

    def apply_credits_styles(self):
        self.logo.setPixmap(
            self.colorize_svg(self.SVG_CREDITS, QColor('white'), QSize(80, 80))
        )
        
    def colorize_svg(self, svg_path, color, size):
        """Colorize an SVG file and return it as a QPixmap."""
        pixmap = QPixmap(svg_path)
        pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Apply color using QPainter
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()

        return pixmap
    
    def emit_theme_change(self):
        self.theme_changed.emit()

    def emit_menu_button_clicked(self, tooltip):
        # Emitir la señal menu_button_clicked con el mensaje del tooltip
        message = f"Submenu {tooltip}"
        self.menu_button_clicked.emit(message)