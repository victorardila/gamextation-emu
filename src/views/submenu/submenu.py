from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtWidgets import QWidget, QSizePolicy, QStackedWidget
from PyQt5.uic import loadUi
from src.components.animation.animation_ppsspp import AnimationPPSSPP
from src.views.submenu.overlay.overlay_content import OverlayContent
from config.storagesys.storage_system import StorageSystem

class SubMenu(QWidget):
    menu_return_clicked = pyqtSignal()
    menu_exit_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.BG_COLOR = None
        self.current_theme = None
        self.read_config_file()
        self.init_submenu()
        self.setup_signals()

    def setup_signals(self):
        self.overlay.menu_return_clicked.connect(self.emit_menu_return)
        self.overlay.menu_exit_clicked.connect(self.emit_menu_exit)

    def read_config_file(self):
        """Lee el archivo de configuración y actualiza los atributos de color de fondo y tema."""
        config_file = 'config.ini'
        storage = StorageSystem(config_file)
        settings = storage.read_config().get('General', {})
        self.BG_COLOR = settings.get('bg_color', self.BG_COLOR)
        self.current_theme = settings.get('theme', self.current_theme)

    def init_submenu(self):
        """Inicializa el menú secundario y aplica los estilos."""
        loadUi("src/views/submenu/submenu.ui", self)
        self.showMaximized()
        self.setStyleSheet(f"background-color: {self.BG_COLOR}")
        self.init_overlay_widget()
        self.init_animation_menu()
        self.adjust_widgets_size_policy()

    def adjust_widgets_size_policy(self):
        """Asegura que los widgets dentro de layout_widgets se expandan adecuadamente."""
        if isinstance(self.layout_widgets, QStackedWidget):
            for widget in self.layout_widgets.findChildren(QWidget):
                widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def showEvent(self, event):
        """Actualiza el color de fondo y el ícono de la animación cuando se muestra la ventana."""
        self.read_config_file()
        self.setStyleSheet(f"background-color: {self.BG_COLOR}")
        if hasattr(self, 'animation') and self.animation:
            self.animation.update_icon_color(self.current_theme)
        super().showEvent(event)  # Llama al método base para manejar otros eventos

    def init_animation_menu(self):
        """Inicializa el widget de animación y lo agrega al layout."""
        self.animation = AnimationPPSSPP()
        self.animation.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout_widgets.addWidget(self.animation)
        self.animation.show()

    def init_overlay_widget(self):
        """Inicializa el widget de superposición y lo agrega al layout."""
        self.overlay = OverlayContent()
        self.layout_widgets.addWidget(self.overlay)
        self.overlay.show()

    def load_module(self, message):
        """Carga el módulo en el overlay."""
        self.overlay.load_module(message)

    def change_theme_mode(self):
        """Cambia el modo del tema y actualiza la configuración y el color de fondo."""
        storage = StorageSystem('config.ini')
        settings = storage.read_config()
        new_theme = 'dark' if settings['General']['theme'] == 'light' else 'light'
        storage.update_config('General', 'theme', new_theme)
        self.read_config_file()
        if hasattr(self, 'animation') and self.animation:
            self.animation.update_icon_color(new_theme)
        self.setStyleSheet(f"background-color: {self.BG_COLOR}")

    def emit_menu_return(self):
        """Emite la señal de retorno del menú."""
        self.menu_return_clicked.emit()

    def emit_menu_exit(self):
        """Emite la señal de salida del menú."""
        self.menu_exit_clicked.emit()