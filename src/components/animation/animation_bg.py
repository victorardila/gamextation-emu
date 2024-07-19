import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QPainter, QTransform, QColor
import qtawesome as qta
import random

class IconAnimationWidget(QLabel):
    def __init__(self, icon, parent=None):
        super(IconAnimationWidget, self).__init__(parent)
        self.original_pixmap = icon.pixmap(64, 64)
        self.color = QColor(255, 255, 255, 90)  # Define el color blanco con opacidad del 50%
        self.setPixmap(self.original_pixmap)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(64, 64)
        
        # Inicializa la dirección de movimiento con velocidades variables
        self.dx = random.uniform(-4, 4)
        self.dy = random.uniform(-4, 4)

        # Posiciona el ícono aleatoriamente dentro de la ventana
        self.x = random.randint(0, parent.width() - self.width())
        self.y = random.randint(0, parent.height() - self.height())
        self.move(int(self.x), int(self.y))

        # Timer para la actualización de la posición y animación
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position_and_animation)
        self.timer.start(16)  # Actualiza cada 16 ms (~60 fps)

        # Tiempo de rotación
        self.rotation_angle = 0

    def update_position_and_animation(self):
        # Actualiza la posición del ícono
        self.x += self.dx
        self.y += self.dy

        # Rebotar en los bordes de la ventana
        if self.x <= 0 or self.x >= self.parent().width() - self.width():
            self.dx = -self.dx
        if self.y <= 0 or self.y >= self.parent().height() - self.height():
            self.dy = -self.dy

        self.move(int(self.x), int(self.y))

        # Actualiza la animación de rotación
        self.rotation_angle = (self.rotation_angle + 5) % 360  # Ajusta el ángulo de rotación
        self.update_pixmap()

    def update_pixmap(self):
        # Actualiza el pixmap con rotación
        transform = QTransform().rotate(self.rotation_angle)
        rotated_pixmap = self.original_pixmap.transformed(transform, mode=Qt.SmoothTransformation)
        
        # Aplica el color blanco con transparencia al pixmap
        colored_pixmap = QPixmap(rotated_pixmap.size())
        colored_pixmap.fill(Qt.transparent)
        painter = QPainter(colored_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.drawPixmap(0, 0, rotated_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
        painter.fillRect(colored_pixmap.rect(), self.color)
        painter.end()
        
        # Actualiza el pixmap del widget
        self.setPixmap(colored_pixmap)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        super(IconAnimationWidget, self).paintEvent(event)

class AnimationBg(QWidget):
    def __init__(self):
        super(AnimationBg, self).__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Crear íconos y añadirlos al widget principal
        self.create_multiple_icons(qta.icon('mdi.circle-outline', color='white', style='outline'), count=30)
        self.create_multiple_icons(qta.icon('mdi.square-outline', color='white', style='outline'), count=30)
        self.create_multiple_icons(qta.icon('mdi.triangle-outline', color='white', style='outline'), count=30)

    def create_multiple_icons(self, icon, count):
        for _ in range(count):
            icon_widget = IconAnimationWidget(icon, self)
            icon_widget.show()