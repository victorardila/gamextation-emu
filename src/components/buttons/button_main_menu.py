from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel
from config.storagesys.storage_system import StorageSystem
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt
import pygame

class ButtonMainMenu(QPushButton):
    gradient_color_selection_dark = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(173, 216, 230, 100), stop:1 rgba(0, 255, 127, 255));"
    gradient_color_selection_light = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 135), stop:0.5 rgba(200, 200, 255, 55), stop:1 rgba(150, 150, 255, 255));"
    hover_sfx = 'src/assets/sfx/hover.wav'
    
    GRADIENT_SELECTED = None
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.read_config_file()
        self.setup_ui()
        self.installEventFilter(self)
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
        self.hover_sound.set_volume(0.3)  # Ajusta el volumen (0.0 a 1.0)
        
    def setup_ui(self):
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(self.default_stylesheet())
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.layout.setSpacing(0)  # Remove spacing
        
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)  # Center the image
        self.layout.addWidget(self.image_label)
        
        self.text_label = QLabel(self)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.text_label)
        
        self.layout.addStretch()  # Add stretchable space to push content to the center
        
    def default_stylesheet(self):
        return """
            QPushButton {
                border: none;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.2); 
            }
        """
    
    def tooltip_stylesheet(self):
        return """
            QToolTip {
                background-color: #333;
                color: #fff;
                border: 0.5px solid white;
                padding: 5px;
                border-radius: 5px;
            }
        """

    def style(self, image, size, tooltip):
        self.setText("")  # Remove button text for design purposes
        
        pixmap = QPixmap(image)
        self.image_label.setPixmap(pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        self.setToolTip(tooltip)
        self.text_label.setText(tooltip)  # Use tooltip as text for QLabel
        
        custom_font = self.load_custom_font()
        self.text_label.setFont(custom_font)
        self.text_label.setStyleSheet("color: white;")
        
        self.setStyleSheet(self.default_stylesheet() + self.tooltip_stylesheet())

    def load_custom_font(self):
        font_id = QFontDatabase.addApplicationFont("src/assets/font/ratchet-clank-psp.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            return QFont(font_family, 20)
        else:
            return QFont("Arial", 18)

    def eventFilter(self, obj, event):
        if event.type() == event.HoverEnter:
            self.set_hover_stylesheet()
            self.play_hover_sound()
        elif event.type() == event.HoverLeave:
            self.set_default_stylesheet()
        elif event.type() == event.MouseButtonPress and event.button() == Qt.LeftButton:
            pass
        return super().eventFilter(obj, event)

    def set_hover_stylesheet(self):
        self.setStyleSheet(
            f"""
            QPushButton {{
                border: none;
                border-radius: 10px;
                background: {self.GRADIENT_SELECTED};
            }}
            {self.tooltip_stylesheet()}
            """
        )

    def set_default_stylesheet(self):
        self.setStyleSheet(self.default_stylesheet() + self.tooltip_stylesheet())

    def play_hover_sound(self):
        if self.hover_sound:
            self.hover_sound.play()