from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt5.QtGui import QPainter, QColor, QLinearGradient, QPen, QPainterPath
from time import time
import math

class GraphicsOptimizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.initAnimation()
    
    def setupUi(self):
        # Configurar el tamaño fijo del widget
        self.setFixedSize(500, 80)
        
        # Configurar el estilo del widget
        self.setStyleSheet(f"""
            background: transparent;
            border-radius: 50px;
        """)

        # Aplicar un efecto de sombra para mejorar la visibilidad de los bordes
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)
        shadow_effect.setOffset(0, 0)
        shadow_effect.setColor(QColor(0, 0, 0, 160))  # Color de la sombra
        self.setGraphicsEffect(shadow_effect)

        # Configurar el layout
        layout = QVBoxLayout()
        label = QLabel("CoverGame")
        label.setAlignment(Qt.AlignCenter)  # Centrar el texto del label
        label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(label)
        self.setLayout(layout)

    def initAnimation(self):
        """Initializes the animation for the tachometer needle."""
        self.animation_time = 8000  # 8 seconds in milliseconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateNeedle)
        self.timer.start(50)  # Update every 50ms
        self.start_time = self.currentTime()

    def currentTime(self):
        """Returns the current time in milliseconds."""
        return int(time() * 1000)

    def updateNeedle(self):
        """Updates the angle of the tachometer needle."""
        current_time = self.currentTime()
        elapsed_time = current_time - self.start_time
        progress = (elapsed_time % self.animation_time) / self.animation_time
        self.angle = 180 * progress

        self.update()  # Trigger a repaint
    
    def paintEvent(self, event):
        """Custom paint event to draw rounded corners with gradient background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Crear un gradiente lineal
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(169, 169, 169, 51))  # 51 ≈ 20% transparencia
        gradient.setColorAt(1, QColor(105, 105, 105, 102))  # 102 ≈ 40% transparencia
        
        # Configurar el pincel del pintor con el gradiente
        painter.setBrush(gradient)
        
        # Dibujar el rectángulo redondeado con el gradiente
        painter.drawRoundedRect(self.rect(), 50, 50)

        # Configurar el estilo del tacómetro la mitad de la circunferencia hacia arriba para el tacómetro
        center_x = 100  # Ajusta este valor para mover el tacómetro a la izquierda
        value_center_y = self.height() / 2
        center_y = value_center_y * 1.3  # Ajusta este valor para mover el tacómetro hacia arriba
        radius = min(self.width(), self.height()) / 2 * 0.8
        
        # Dibujar el arco del tacómetro
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        arc_rect = QRectF(center_x - radius, center_y - radius, 2 * radius, radius * 2)
        painter.drawArc(arc_rect, 0 * 16, 180 * 16)  # Dibuja solo la mitad superior

        # Dibujar la franja blanca interna
        inner_radius = radius * 0.9  # Ajusta este valor para la franja blanca interna
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        inner_arc_rect = QRectF(center_x - inner_radius, center_y - inner_radius, 2 * inner_radius, inner_radius * 2)
        painter.drawArc(inner_arc_rect, 0 * 16, 180 * 16)  # Dibuja solo la mitad superior

        # Crear un gradiente lineal para la franja más interna
        gradient = QLinearGradient(center_x - inner_radius, center_y - radius, center_x + inner_radius, center_y - radius)
        gradient.setColorAt(0.0, QColor(255, 0, 0))  # Rojo fuerte en el inicio
        gradient.setColorAt(0.5, QColor(255, 255, 0))  # Amarillo en el medio
        gradient.setColorAt(1.0, QColor(0, 255, 0))  # Verde fuerte al final
        
        # Dibujar la franja más interna con el gradiente
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawArc(QRectF(center_x - inner_radius, center_y - inner_radius, 2 * inner_radius, inner_radius * 2), 0 * 16, 180 * 16)  # Dibuja solo la mitad superior

        # Dibujar la franja blanca más interna y más gruesa
        inner_most_radius = radius * 0.7  # Ajusta este valor para la franja más interna
        painter.setPen(QPen(QColor(255, 255, 255), 8))  # Grosor de línea mayor para la franja más gruesa
        inner_most_arc_rect = QRectF(center_x - inner_most_radius, center_y - inner_most_radius, 2 * inner_most_radius, inner_most_radius * 2)
        painter.drawArc(inner_most_arc_rect, 0 * 16, 180 * 16)  # Dibuja solo la mitad superior

        # Dibujar la aguja del tacómetro
        needle_length = radius * 0.8
        # Cambiar el ángulo para que la aguja empiece desde la izquierda y vaya hacia la derecha
        angle_rad = math.radians(180 - self.angle)  # Ajuste para que la aguja comience desde la izquierda
        needle_end = QPointF(center_x + needle_length * math.cos(angle_rad),
                            center_y - needle_length * math.sin(angle_rad))
        painter.setPen(QPen(QColor(255, 0, 0), 5))
        painter.drawLine(QPointF(center_x, center_y), needle_end)