from PyQt5.QtWidgets import QWidget, QSizePolicy, QStackedWidget
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.uic import loadUi
from src.components.animation.animation_ppsspp import AnimationPPSSPP
from src.views.submenu.overlay.overlay_content import OverlayContent
from config.storagesys.storage_system import StorageSystem

class SubMenu(QWidget):
    menu_return_clicked = pyqtSignal()
    menu_exit_clicked = pyqtSignal()
    BG_COLOR = None
    
    def __init__(self):
        super().__init__()
        self.init_submenu()
        self.overlay.menu_return_clicked.connect(self.emit_menu_return)
        self.overlay.menu_exit_clicked.connect(self.emit_menu_exit)
    
    def read_config_file(self):
        config_file = 'config.ini'
        storage = StorageSystem(config_file)
        settings = storage.read_config()
        if 'General' in settings:
            if 'bg_color' in settings['General']:
                self.BG_COLOR = settings['General']['bg_color']
                self.current_theme = settings['General']['theme']
                
    def init_submenu(self):
        self.read_config_file()
        loadUi("src/views/submenu/submenu.ui", self)
        self.showMaximized()
        self.setStyleSheet(f"background-color: {self.BG_COLOR}")
        self.init_overlay_widget()
        self.init_animation_menu()
        # Asegurarse de que los widgets dentro del layout_widgets se expanden adecuadamente
        if isinstance(self.layout_widgets, QStackedWidget):
            for widget in self.layout_widgets.findChildren(QWidget):
                widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                
    def showEvent(self, event):
        # cada vez que se muestre la ventana, se actualiza el color de fondo
        self.read_config_file()
        self.setStyleSheet(f"background-color: {self.BG_COLOR}")
        if hasattr(self, 'animation') and self.animation:  # Verifica si self.animation está inicializado
            self.animation.update_icon_color(self.current_theme)
                
    def init_animation_menu(self):
        self.animation = AnimationPPSSPP()
        self.animation.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout_widgets.addWidget(self.animation)
        self.animation.show()

    def init_overlay_widget(self):
        self.overlay = OverlayContent()
        self.layout_widgets.addWidget(self.overlay)
        self.overlay.show()
        
    def load_module(self, message):
        self.overlay.load_module(message)    
        
    def change_theme_mode(self):
        # Inicializa el sistema de almacenamiento y lee la configuración actual
        storage = StorageSystem('config.ini')
        settings = storage.read_config()
        # Determina el nuevo tema
        current_theme = settings['General']['theme']
        new_theme = 'dark' if current_theme == 'light' else 'light'
        # Actualiza la configuración con el nuevo tema
        storage.update_config('General', 'theme', new_theme)
        # Vuelve a leer la configuración para obtener el nuevo color de fondo
        self.read_config_file()
        if hasattr(self, 'animation') and self.animation:  # Verifica si self.animation está inicializado
            self.animation.update_icon_color(new_theme)
        self.setStyleSheet(f"background-color: {self.BG_COLOR}")
    
    def emit_menu_return(self):
        self.menu_return_clicked.emit()
    
    def emit_menu_exit(self):
        self.menu_exit_clicked.emit()
