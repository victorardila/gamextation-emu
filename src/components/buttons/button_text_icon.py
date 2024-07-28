from config.storagesys.storage_system import StorageSystem
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from qtawesome import icon
import pygame

class ButtonTextIcon(QPushButton):
    gradient_color_selection_dark = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(173, 216, 230, 100), stop:1 rgba(0, 255, 127, 255));"
    gradient_color_selection_light = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 135), stop:0.5 rgba(200, 200, 255, 155), stop:1 rgba(150, 150, 255, 255));"
    hover_sfx = 'src/assets/sfx/hover.wav'
    
    GRADIENT_SELECTED = None
    
    def __init__(self, parent=QWidget | None):
        super().__init__(parent)
        self.read_config_file()
        self.installEventFilter(self)
        self.setCursor(Qt.PointingHandCursor)
        self.init_sfx()
        
    def read_config_file(self):
        config_file = 'config.ini'
        storage = StorageSystem(config_file)
        settings = storage.read_config()
        if 'General' in settings:
            if 'theme' in settings['General']:
                theme = settings['General']['theme']
                self.gradient_color_selection = self.gradient_color_selection_dark if theme == 'dark' else self.gradient_color_selection_light
                self.GRADIENT_SELECTED = self.gradient_color_selection
                
    def showEvent(self, event):
        self.read_config_file()
        super().showEvent(event)

    def init_sfx(self):
        # Inicializar pygame mixer
        pygame.mixer.init()
        self.hover_sound = pygame.mixer.Sound(self.hover_sfx)
        self.hover_sound.set_volume(0.6)  # Ajusta el volumen (0.0 a 1.0)
        
    def style(self, icon_name, size, tooltip, color='white'):
        self.setIcon(QIcon(icon(icon_name, color=color)))
        self.setIconSize(size)
        self.setToolTip(tooltip)
        self.setStyleSheet(self.default_stylesheet())

    def default_stylesheet(self):
        return """
            QPushButton {
                border: none;
                border-radius: 10px;
                color: white;
                background-color: rgba(255, 255, 255, 0);
            }
            QToolTip {
                background-color: #333;
                color: #fff;
                border: 0.5px solid white;
                padding: 5px;
                border-radius: 5px;
            }
        """
    
    def hover_enter_stylesheet(self):
        return f"""
            QPushButton {{
                border: none;
                border-radius: 10px;
                color: white;
                background-color: {self.GRADIENT_SELECTED};
            }}
            QToolTip {{
                background-color: #333;
                color: #fff;
                border: 1px solid white;
                padding: 5px;
                border-radius: 5px;
            }}
        """

    def hover_leave_stylesheet(self):
        return """
            QPushButton {
                border: none;
                border-radius: 10px;
                color: white;
                background-color: rgba(255, 255, 255, 0);
            }
            QToolTip {
                background-color: #333;
                color: #fff;
                border: 0.5px solid white;
                padding: 5px;
                border-radius: 5px;
            }
        """
    
    def eventFilter(self, obj, event):
        if event.type() == event.HoverEnter:
            self.setStyleSheet(self.hover_enter_stylesheet())
            self.play_hover_sound()
        elif event.type() == event.HoverLeave:
            self.setStyleSheet(self.hover_leave_stylesheet())
        elif event.type() == event.MouseButtonPress and event.button() == Qt.LeftButton:
            pass
        return super().eventFilter(obj, event)

    def play_hover_sound(self):
        if self.hover_sound:
            self.hover_sound.play()