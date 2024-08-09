from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QBrush, QPen, QCursor, QMovie
from config.storagesys.storage_system import StorageSystem
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QSize
import random

class GradientSelectorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        # Crear el gradiente con las configuraciones dadas
        gradient_color_selection_dark = QLinearGradient(0, 0, self.width(), self.height())
        gradient_color_selection_dark.setColorAt(0, QColor(173, 216, 230, 15))  # Color azul claro con 39% opacidad
        gradient_color_selection_dark.setColorAt(1, QColor(0, 255, 127, 90))  # Color verde con 100% opacidad    

        brush = QBrush(gradient_color_selection_dark)
        painter.setBrush(brush)
        painter.setPen(QPen(brush, 4))  # Ajustar el ancho del borde según sea necesario

        # Dibujar el borde con gradiente y esquinas redondeadas
        rect = self.rect().adjusted(2, 2, -2, -2)  # Ajustar un poco para evitar que el borde se corte
        painter.drawRoundedRect(rect, 20, 20)  # Esquinas redondeadas con un radio de 20px

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Redibujar el widget para aplicar el borde gradiente correctamente
        self.update()
        
class CoverConsole(QWidget):
    ThemeSelected = None
    
    def __init__(self, gifs, parent=None):
        super().__init__()
        self.gifs = gifs
        self.read_config_file()
        self.setupUi()
    
    def read_config_file(self):
        config_file = 'config.ini'
        storage = StorageSystem(config_file)
        settings = storage.read_config()
        if 'General' in settings:
            if 'theme' in settings['General']:
                theme = settings['General']['theme']
                self.ThemeSelected = theme
    
    def setupUi(self):
        # Hacer que el widget ocupe todo el espacio disponible
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: transparent;")
        self.setAutoFillBackground(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Elimina los márgenes del layout
        layout.setSpacing(0)  # Elimina el espacio entre widgets

        self.label = QLabel(self)  # Crear el QLabel y asignarlo al atributo
        self.label.setAlignment(Qt.AlignCenter)  # Centrar el texto del label
        self.label.setStyleSheet("background: transparent;")  # Hacer el fondo del QLabel transparente
        layout.addWidget(self.label)  # Añadir el QLabel al layout

        self.gradient_border_widget = GradientSelectorWidget(self)
        self.gradient_border_widget.setGeometry(self.rect())
        self.gradient_border_widget.ThemeSelected = self.ThemeSelected
        self.gradient_border_widget.show()

        self.setLayout(layout)
        self.load_gif()
        self.show()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Ajustar el tamaño del widget de borde al tamaño del CoverGame
        if self.gradient_border_widget:
            self.gradient_border_widget.setGeometry(self.rect())
        self.resize_gif()
        
    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.PointingHandCursor))  # Cambiar el cursor a mano cuando está en hover
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
        
    def load_gif(self):
        """Carga el GIF en el QLabel."""
        random_index = random.randint(0, len(self.gifs) - 1)
        self.movie = QMovie(self.gifs[random_index])
        self.label.setMovie(self.movie)
        self.movie.start()

    def resize_gif(self):
        """Ajusta el tamaño del GIF al ancho del QLabel manteniendo la proporción y centrado."""
        if self.movie:
            movie_width = self.movie.currentImage().width()
            movie_height = self.movie.currentImage().height()

            # Calcular la nueva altura manteniendo la proporción
            new_width = self.label.width()
            new_height = int((new_width / movie_width) * movie_height)

            # Ajustar el tamaño de la película al QLabel
            self.movie.setScaledSize(QSize(new_width, new_height))

            # Centrar verticalmente el GIF dentro del QLabel
            self.label.setAlignment(Qt.AlignCenter)

        self.update()