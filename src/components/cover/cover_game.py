from config.storagesys.storage_system import StorageSystem
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QLinearGradient, QColor
from PyQt5.QtCore import Qt
import pygame

class CoverGame(QWidget):
    ThemeSelected = None

    def __init__(self):
        super().__init__()
        self.is_hovered = False  # Variable para rastrear el estado de hover
        self.read_config_file()
        self.setupUi()
        self.init_sfx()
        
    def read_config_file(self):
        config_file = 'config.ini'
        storage = StorageSystem(config_file)
        settings = storage.read_config()
        if 'General' in settings:
            if 'theme' in settings['General']:
                theme = settings['General']['theme']
                # guardo el theme seleccionado
                self.ThemeSelected = theme

    def init_sfx(self):
        # Inicializar pygame mixer
        pygame.mixer.init()
        self.hover_sound = pygame.mixer.Sound('src/assets/sfx/hover.wav')
        self.hover_sound.set_volume(0.6)  # Ajusta el volumen (0.0 a 1.0)

    def setupUi(self):
        # Configurar estilos del widget
        self.resize(200, 200)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")

        layout = QVBoxLayout()
        label = QLabel("CoverGame")
        label.setAlignment(Qt.AlignCenter)  # Centrar el texto del label
        label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(label)
        self.setLayout(layout)

        self.show()

    def enterEvent(self, event):
        self.is_hovered = True
        self.update()  # Redibuja el widget para aplicar el borde gradiente
        self.play_hover_sound()  # Reproduce el sonido de hover
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hovered = False
        self.update()  # Redibuja el widget para remover el borde gradiente
        super().leaveEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)

        # Crear el QPainter para dibujar el borde
        painter = QPainter(self)

        if self.is_hovered:
            # Crear un gradiente lineal si el widget está en hover
            gradient_color_selection_dark = QLinearGradient(0, 0, self.width(), self.height())
            gradient_color_selection_dark.setColorAt(0, QColor(0, 255, 127, 128))  # Color verde con 50% opacidad
            gradient_color_selection_dark.setColorAt(1, QColor(173, 216, 230, 128))  # Color azul claro con 50% opacidad
            
            gradient_color_selection_light = QLinearGradient(0, 0, self.width(), self.height())
            gradient_color_selection_light.setColorAt(0, QColor(255, 255, 255, 135))
            gradient_color_selection_light.setColorAt(0.5, QColor(200, 200, 255, 155))
            gradient_color_selection_light.setColorAt(1, QColor(150, 150, 255, 255))

            gradient = gradient_color_selection_dark if self.ThemeSelected == 'dark' else gradient_color_selection_light
            
            # Configurar el pincel con el gradiente
            pen = painter.pen()
            pen.setWidth(4)  # Ajustar el ancho del borde según sea necesario
            pen.setBrush(gradient)
            painter.setPen(pen)

            # Dibujar el borde con gradiente
            painter.drawRect(1, 1, self.width() - 3, self.height() - 3)  # Ajustar el dibujo del borde para no superponer con el contenido del widget

    def play_hover_sound(self):
        if self.hover_sound:
            self.hover_sound.play()