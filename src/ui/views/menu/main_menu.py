from config.storagesys.storage_system import StorageSystem
from src.ui.components.animation.animation_ppsspp import AnimationPPSSPP
from src.ui.views.menu.overlay.overlay_content import OverlayContent
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtWidgets import QWidget, QSizePolicy, QStackedWidget
from PyQt5.uic import loadUi

class MainMenu(QWidget):
    menu_button_clicked = pyqtSignal(str)  # Señal para indicar que un botón del menú ha sido presionado
    menu_exit_clicked = pyqtSignal()
    sound_switch_state = pyqtSignal()  # Señal para indicar el cambio de estado del sonido
    bg_changed = pyqtSignal()  # Señal para indicar que el color de fondo ha cambiado
    BG_COLOR = None
    
    def __init__(self):
        super().__init__()
        self.read_config_file()
        self.init_main_menu()

    def read_config_file(self):
        """Lee el archivo de configuración y actualiza el color de fondo."""
        config_file = 'config.ini'
        storage = StorageSystem(config_file)
        settings = storage.read_config()
        if 'General' in settings and 'bg_color' in settings['General']:
            self.BG_COLOR = settings['General']['bg_color']
    
    def init_main_menu(self):
        """Inicializa el menú principal y su configuración."""
        loadUi("src/ui/views/menu/main_menu.ui", self)
        self.showMaximized()
        self.setStyleSheet(f"background-color: {self.BG_COLOR}")
        self.init_overlay_widget()
        self.init_animation_menu()

        # Asegurarse de que los widgets dentro del layout_widgets se expanden adecuadamente
        if isinstance(self.layout_widgets, QStackedWidget):
            for widget in self.layout_widgets.findChildren(QWidget):
                widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                
    def init_animation_menu(self):
        """Inicializa el menú de animación y lo agrega al layout."""
        self.animation = AnimationPPSSPP()
        self.animation.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout_widgets.addWidget(self.animation)
        self.animation.show()
        
    def init_overlay_widget(self):
        """Inicializa el widget de overlay y conecta las señales."""
        self.overlay = OverlayContent()
        self.layout_widgets.addWidget(self.overlay)
        self.overlay.show()

        # Conectar las señales a sus respectivos métodos
        self.overlay.theme_changed.connect(self.change_theme_mode)
        self.overlay.menu_button_clicked.connect(self.handle_menu_button_clicked)
        self.overlay.menu_exit_clicked.connect(self.handle_menu_exit_clicked)
        self.overlay.sound_switch_state.connect(self.handle_sound_switch_state)
        
    def change_theme_mode(self):
        """Cambia el modo del tema y actualiza la configuración y la interfaz."""
        storage = StorageSystem('config.ini')
        settings = storage.read_config()
        current_theme = settings['General']['theme']
        new_theme = 'dark' if current_theme == 'light' else 'light'
        
        # Actualiza la configuración con el nuevo tema
        storage.update_config('General', 'theme', new_theme)
        self.read_config_file()
        
        # Configuración de icono, tooltip e icon_color basada en el nuevo tema
        icon, tooltip, icon_color = (
            ('fa5s.moon', "Modo oscuro", 'gray') 
            if new_theme == 'light' 
            else ('fa5s.sun', "Modo claro", 'white')
        )
        
        # Actualiza la animación y el icono del botón de modo
        self.overlay.button_icon_mode.style(icon, QSize(32, 32), tooltip, icon_color)
        self.animation.update_icon_color(new_theme)
        self.bg_changed.emit()
        self.setStyleSheet(f"background-color: {self.BG_COLOR}")

    def handle_menu_button_clicked(self, tooltip):
        """Emite la señal cuando se hace clic en un botón del menú."""
        self.menu_button_clicked.emit(tooltip)
        
    def handle_menu_exit_clicked(self):
        """Emite la señal cuando se hace clic en el botón de salir del menú."""
        self.menu_exit_clicked.emit()
        
    def handle_sound_switch_state(self):
        """Emite la señal cuando se cambia el estado del sonido."""
        self.sound_switch_state.emit()