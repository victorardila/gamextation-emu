from config.storagesys.storage_system import StorageSystem
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QPixmap, QImage, QBrush, QPen, QCursor, QMovie
from PyQt5.QtCore import Qt, pyqtSignal

class CoverConsole(QWidget):
        
        # arreglo de imagenes gif de consolas
        GIF_CONSOLE = [
            "src/assets/gif/console.gif",
            "src/assets/gif/console2.gif",
            "src/assets/gif/console3.gif",
        ]
        
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setStyleSheet("background: transparent; border-radius: 10px;")
            
        def load_gif(self):
            """Carga el GIF en el QLabel y ajusta su tamaño."""
            self.movie = QMovie(self.GIF_CONSOLE)
            self.label_gif.setMovie(self.movie)
            self.movie.frameChanged.connect(self.resize_gif)
            self.movie.start()
            
        def resize_gif(self):
            """Ajusta el tamaño del GIF al ancho del QLabel manteniendo la proporción."""
            frame = self.movie.currentPixmap()
            if not frame.isNull():
                label_width = self.label_gif.width()
                frame = frame.scaledToWidth(label_width, Qt.SmoothTransformation)
                self.label_gif.setPixmap(frame)
    
        def paintEvent(self, event):
            super().paintEvent(event)
            painter = QPainter(self)
            gradient_color_selection_dark = QLinearGradient(0, 0, self.width(), self.height())
            gradient_color_selection_dark.setColorAt(0, QColor(0, 255, 127, 128))  # Color verde con 50% opacidad
            gradient_color_selection_dark.setColorAt(1, QColor(173, 216, 230, 128))  # Color azul claro con 50% opacidad
                
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