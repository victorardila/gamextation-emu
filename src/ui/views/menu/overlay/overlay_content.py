from PyQt5.QtCore import QSize, Qt, QTimer, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from datetime import datetime
import requests

from src.utils.connection_tester_worker import ConnectionTesterWorker
from src.ui.components.toast.notification_toast import NotificationToast
from config.storagesys.storage_system import StorageSystem

class OverlayContent(QWidget):
    theme_changed = pyqtSignal()
    sound_switch_state = pyqtSignal()
    menu_button_clicked = pyqtSignal(str)
    menu_exit_clicked = pyqtSignal()

    SVG_CREDITS = "src/assets/svg/icon.svg"
    SOUND = None

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

    def __init__(self):
        super().__init__()
        self._read_config_file()
        self._init_main_menu()

        self.connection_checker = ConnectionTesterWorker("http://www.google.com")
        self.connection_checker.stateConnection.connect(self._handle_connection_state)
        self.connection_checker.start()

        self._check_initial_connection()

    def _check_initial_connection(self):
        try:
            response = requests.get("http://www.google.com", timeout=5)
            if response.status_code != 200:
                self._show_connection_lost_toast()
        except requests.RequestException:
            self._show_connection_lost_toast()

    def _read_config_file(self):
        config_file = "config.ini"
        storage = StorageSystem(config_file)
        settings = storage.read_config()
        self.SOUND = settings.get("General", {}).get("sound", None)

    def _init_main_menu(self):
        loadUi("src/ui/views/menu/overlay/overlay_content.ui", self)
        self.setStyleSheet("background-color: transparent;")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._apply_top_bar_styles()
        self._apply_content_styles()
        self._apply_credits_styles()

    def _apply_top_bar_styles(self):
        custom_font = self._load_custom_font(
            "src/assets/font/ratchet-clank-psp.ttf", 24, "Arial", 18
        )

        self.button_icon_user.style("fa.user", QSize(32, 32), "Usuario", "white")
        self.button_icon_mode.style("fa5s.sun", QSize(32, 32), "Modo claro", "white")
        self._update_sound_icon()
        self.button_connection.style("fa5s.wifi", QSize(32, 32), "Conexión", "white")
        self.button_icon_search.style("fa.search", QSize(32, 32), "Buscar", "white")
        self.label_hour.style("00:00:00 AM", "white", 30, custom_font, Qt.AlignCenter)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000)

        self._update_time()

        self.button_icon_mode.clicked.connect(self.theme_changed.emit)
        self.button_sound.clicked.connect(self._emit_sound_switch)

    def _load_custom_font(self, font_path, font_size, fallback_font, fallback_size):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            return QFont(font_family, font_size)
        return QFont(fallback_font, fallback_size)

    def _update_time(self):
        current_time = datetime.now().strftime("%I:%M:%S %p")
        self.label_hour.setText(current_time)

    def _apply_content_styles(self):
        self.frameMenuRowOne.setStyleSheet("background-color: transparent;")
        self.frameMenuRowTwo.setStyleSheet("background-color: transparent;")

        buttons = [
            self.button_load_roms,
            self.button_select_console,
            self.button_store,
            self.button_media,
            self.button_user,
            self.button_settings,
            self.button_optimize,
            self.button_update,
            self.button_creator,
            self.button_about,
            self.button_logout,
        ]

        tooltips = [
            "Juegos cargados",
            "Seleccionar consola",
            "Tienda",
            "Media",
            "Usuario",
            "Configuraciones",
            "Optimizar",
            "Actualizaciones",
            "Creador",
            "Acerca de",
            "Salir",
        ]

        for btn, image, tooltip in zip(buttons, self.IMAGES, tooltips):
            btn.style(image, QSize(250, 350), tooltip)
            btn.clicked.connect(lambda _, t=tooltip: self._emit_menu_button_clicked(t))

        self.button_logout.clicked.connect(self.menu_exit_clicked.emit)

    def _apply_credits_styles(self):
        self.logo.setPixmap(
            self._colorize_svg(self.SVG_CREDITS, QColor("white"), QSize(40, 40))
        )

    def _colorize_svg(self, svg_path, color, size):
        pixmap = QPixmap(svg_path).scaled(
            size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()

        return pixmap

    def _emit_sound_switch(self):
        self.SOUND = "on" if self.SOUND == "off" else "off"
        self._update_sound_icon()
        self.sound_switch_state.emit()

    def _update_sound_icon(self):
        icon = "fa5s.volume-up" if self.SOUND == "on" else "fa5s.volume-mute"
        tooltip = "Sonido" if self.SOUND == "on" else "Silencio"
        self.button_sound.style(icon, QSize(32, 32), tooltip, "white")

    def _emit_menu_button_clicked(self, tooltip):
        message = f"Submenu {tooltip}"
        self.menu_button_clicked.emit(message)

    @pyqtSlot(str, bool)
    def _handle_connection_state(self, url, state):
        if state:
            self._handle_connection_restored()
        else:
            self._show_connection_lost_toast()

    @pyqtSlot()
    def _show_connection_lost_toast(self):
        self.toast = NotificationToast(
            "Te has quedado sin conexión a Internet.", "mdi.wifi-remove", QSize(32, 32)
        )
        self.toast.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.toast.setAttribute(Qt.WA_TranslucentBackground)
        self.toast.show()

        QTimer.singleShot(5000, self.toast.close)

    def _handle_connection_restored(self):
        if not hasattr(self, "restored_toast_shown") or not self.restored_toast_shown:
            self.restored_toast_shown = True

            self.toast = NotificationToast(
                "Conexión restaurada. Ahora estás en línea.",
                "mdi.wifi-check",
                QSize(32, 32),
            )
            self.toast.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.toast.setAttribute(Qt.WA_TranslucentBackground)
            self.toast.show()

            QTimer.singleShot(5000, self.toast.close)
            self._show_notification_toast()

    def _show_notification_toast(self):
        if self.SOUND == "on":
            self.toast = NotificationToast(
                "Por favor, conecte los auriculares para una mejor experiencia.",
                "fa5s.headphones",
                QSize(32, 32),
            )
            self.toast.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.toast.setAttribute(Qt.WA_TranslucentBackground)
            self.toast.show()

            QTimer.singleShot(5000, self.toast.close)