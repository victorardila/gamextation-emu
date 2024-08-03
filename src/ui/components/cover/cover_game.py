from config.storagesys.storage_system import StorageSystem
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QPixmap, QImage, QBrush, QPen, QCursor
from PyQt5.QtCore import Qt, pyqtSignal
import requests
from io import BytesIO
from PIL import Image
import pygame

class GradientSelectorWidget(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")
        self.is_hovered = False

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        # Establecer el pincel para el gradiente
        if self.is_hovered:
            gradient_color_selection_dark = QLinearGradient(0, 0, self.width(), self.height())
            gradient_color_selection_dark.setColorAt(0, QColor(0, 255, 127, 128))  # Color verde con 50% opacidad
            gradient_color_selection_dark.setColorAt(1, QColor(173, 216, 230, 128))  # Color azul claro con 50% opacidad
            
            gradient_color_selection_light = QLinearGradient(0, 0, self.width(), self.height())
            gradient_color_selection_light.setColorAt(0, QColor(255, 255, 255, 135))
            gradient_color_selection_light.setColorAt(0.5, QColor(200, 200, 255, 155))
            gradient_color_selection_light.setColorAt(1, QColor(150, 150, 255, 255))

            gradient = gradient_color_selection_dark if self.parent().ThemeSelected == 'dark' else gradient_color_selection_light
            
            # brush = QBrush(gradient)
            brush = QBrush(gradient_color_selection_dark)
            painter.setBrush(brush)
            painter.setPen(QPen(brush, 4))  # Ajustar el ancho del borde según sea necesario

            # Dibujar el borde con gradiente
            painter.drawRect(self.rect())  # Dibujar el borde con el tamaño completo del widget

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Redibujar el widget para aplicar el borde gradiente correctamente
        self.update()
        
class CoverGame(QWidget):
    game_hovered = pyqtSignal(str)  # Señal que emite el nombre del juego
    ThemeSelected = None
    game = None

    def __init__(self):
        super().__init__()
        self.is_hovered = False  # Variable para rastrear el estado de hover
        self.label = None  # Atributo para almacenar el QLabel
        self.gradient_border_widget = None  # Atributo para el widget de borde
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

        self.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Ajustar el tamaño del widget de borde al tamaño del CoverGame
        if self.gradient_border_widget:
            self.gradient_border_widget.setGeometry(self.rect())
        self.update()

    def load_game(self, game):
        self.game = game
        img_url = game['cover_image']
        
        # Descargar la imagen usando requests
        response = requests.get(img_url)
        
        # Verificar si la respuesta es una imagen
        if 'image' not in response.headers.get('Content-Type', ''):
            print("La URL no devuelve una imagen válida.")
            return

        # Crear un BytesIO con los datos de la imagen descargada
        image_data = BytesIO(response.content)

        try:
            # Cargar la imagen usando Pillow
            with Image.open(image_data) as img:
                # Convertir a PNG en memoria
                with BytesIO() as png_image_data:
                    img.save(png_image_data, format='PNG')
                    png_image_data.seek(0)
                    
                    # Crear un QImage y cargar los datos PNG
                    image = QImage()
                    image.loadFromData(png_image_data.read())
                    
                    # Crear un QPixmap con el QImage
                    pixmap = QPixmap.fromImage(image)
                    
                    # Redimensionar el QPixmap para llenar completamente el widget
                    pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                    
                    # Actualizar el QLabel con la imagen redimensionada
                    self.label.setPixmap(pixmap)
                    self.label.setScaledContents(True)  # Asegura que el QLabel redimensione la imagen
                    
                    # Actualizar el widget para asegurarse de que el paintEvent se llame
                    self.update()

        except Exception as e:
            print(f"Error al procesar la imagen: {e}")

    def enterEvent(self, event):
        self.is_hovered = True
        self.gradient_border_widget.is_hovered = True
        self.setCursor(QCursor(Qt.PointingHandCursor))  # Cambiar el cursor a mano cuando está en hover
        self.update()  # Redibuja el widget para aplicar el borde gradiente
        self.play_hover_sound()  # Reproduce el sonido de hover
        
        # Emitir el nombre del juego a través de la señal
        if self.parent() and isinstance(self.parent(), QWidget):
            self.game_hovered.emit(self.game['name'])
        
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hovered = False
        self.gradient_border_widget.is_hovered = False
        self.setCursor(QCursor(Qt.ArrowCursor))  # Cambiar el cursor a flecha cuando sale del hover
        self.update()  # Redibuja el widget para remover el borde gradiente
        super().leaveEvent(event)

    def play_hover_sound(self):
        if self.hover_sound:
            self.hover_sound.play()