from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt5.uic import loadUi
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap, QPainter, QColor
from datetime import datetime
from config.storagesys.storage_system import StorageSystem

class OverlayContent(QWidget):
    theme_changed = pyqtSignal()
    sound_switch_state = pyqtSignal()
    menu_button_clicked = pyqtSignal(str)
    menu_exit_clicked = pyqtSignal()

    SVG_CREDITS = "src/assets/svg/icon.svg"
    SOUND = None

    IMAGES = [
        "src/assets/img/load_ROMs.png", "src/assets/img/select_console.png",
        "src/assets/img/store.png", "src/assets/img/media.png",
        "src/assets/img/user.png", "src/assets/img/settings.png",
        "src/assets/img/optimize.png", "src/assets/img/update.png",
        "src/assets/img/creator.png", "src/assets/img/about.png",
        "src/assets/img/exit.png",
    ]

    def __init__(self):
        super().__init__()
        self.read_config_file()
        self.init_main_menu()

    def read_config_file(self):
        config_file = 'config.ini'
        storage = StorageSystem(config_file)
        settings = storage.read_config()
        self.SOUND = settings.get('General', {}).get('sound', None)

    def init_main_menu(self):
        loadUi("src/views/menu/overlay/overlay_content.ui", self)
        self.setStyleSheet("background-color: transparent;")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.apply_top_bar_styles()
        self.apply_content_styles()
        self.apply_credits_styles()

    def apply_top_bar_styles(self):
        custom_font = self.load_custom_font("src/assets/font/ratchet-clank-psp.ttf", 24, "Arial", 18)

        self.button_icon_user.style('fa.user', QSize(32, 32), "Usuario", 'white')
        self.button_icon_mode.style('fa5s.sun', QSize(32, 32), "Modo claro", 'white')
        self.button_sound.style('fa5s.volume-up', QSize(32, 32), "Sonido", 'white')
        self.button_icon_search.style('fa.search', QSize(32, 32), "Buscar", 'white')
        self.label_hour.style("00:00:00 AM", "white", 30, custom_font, Qt.AlignCenter)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.update_time()

        self.button_icon_mode.clicked.connect(self.theme_changed.emit)
        self.button_sound.clicked.connect(self.emit_sound_switch)

    def load_custom_font(self, font_path, font_size, fallback_font, fallback_size):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            return QFont(font_family, font_size)
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
            btn.clicked.connect(lambda _, t=tooltip: self.emit_menu_button_clicked(t))

        self.button_logout.clicked.connect(self.menu_exit_clicked.emit)

    def apply_credits_styles(self):
        self.logo.setPixmap(self.colorize_svg(self.SVG_CREDITS, QColor('white'), QSize(40, 40)))

    def colorize_svg(self, svg_path, color, size):
        pixmap = QPixmap(svg_path).scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()

        return pixmap

    def emit_sound_switch(self):
        self.SOUND = 'on' if self.SOUND == 'off' else 'off'
        icon = 'fa5s.volume-up' if self.SOUND == 'on' else 'fa5s.volume-mute'
        tooltip = "Sonido" if self.SOUND == 'on' else "Silencio"
        self.button_sound.style(icon, QSize(32, 32), tooltip, 'white')
        self.sound_switch_state.emit()

    def emit_menu_button_clicked(self, tooltip):
        message = f"Submenu {tooltip}"
        self.menu_button_clicked.emit(message)