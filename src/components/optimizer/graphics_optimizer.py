from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt5.QtGui import QPainter, QColor, QLinearGradient, QPen, QPainterPath
from time import time
import pygame
import psutil
import math
import os

class GraphicsOptimizer(QWidget):
    load_sfx = 'src/assets/sfx/optimize.wav'
    
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.initAnimation()
        self.init_sfx()  # Inicializar el sonido antes de la animación
        optimize_system_resources(os.getpid())
        
    def init_sfx(self):
        # Inicializar pygame mixer
        pygame.mixer.init()
        # Cargar el sonido
        self.sound = pygame.mixer.Sound(self.load_sfx)
        # Reproducir el sonido
        self.sound.set_volume(0.3)  # Ajusta el volumen (0.0 a 1.0)

    def setupUi(self):
        # Configurar el tamaño fijo del widget
        self.setFixedSize(500, 80)

        # Configurar el estilo del widget
        self.setStyleSheet(
            f"""
            background: transparent;
            border-radius: 50px;
        """
        )

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
        center_y = (
            value_center_y * 1.3
        )  # Ajusta este valor para mover el tacómetro hacia arriba
        radius = min(self.width(), self.height()) / 2 * 0.8

        # Dibujar el arco del tacómetro
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        arc_rect = QRectF(center_x - radius, center_y - radius, 2 * radius, radius * 2)
        painter.drawArc(arc_rect, 0 * 16, 180 * 16)  # Dibuja solo la mitad superior

        # Crear un gradiente lineal para la franja más interna
        gradient = QLinearGradient(
            center_x - radius, center_y - radius, center_x + radius, center_y - radius
        )
        gradient.setColorAt(0.0, QColor(255, 0, 0))  # Rojo fuerte en el inicio
        gradient.setColorAt(0.5, QColor(255, 255, 0))  # Amarillo en el medio
        gradient.setColorAt(1.0, QColor(0, 255, 0))  # Verde fuerte al final

        # Crear un QPainterPath para dibujar el arco con el gradiente
        path = QPainterPath()
        path.arcMoveTo(arc_rect, 0)  # Mueve el camino al inicio del arco
        path.arcTo(arc_rect, 0, 180)  # Dibuja el arco

        # Crear una máscara para la franja más interna
        mask = QPainterPath()
        inner_radius = radius * 0.6
        inner_arc_rect = QRectF(
            center_x - inner_radius,
            center_y - inner_radius,
            2 * inner_radius,
            inner_radius * 2,
        )
        mask.arcMoveTo(inner_arc_rect, 0)
        mask.arcTo(inner_arc_rect, 0, 180)

        # Resta el camino de la máscara del arco principal
        path -= mask

        # Configurar el pincel del pintor con el gradiente y dibujar la franja con gradiente
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawPath(path)

        # Dibujar la franja blanca más interna y más gruesa
        inner_most_radius = (
            radius * 0.6
        )  # Ajusta este valor para la franja más interna hacerla gruesa o delgada
        painter.setPen(
            QPen(QColor(255, 255, 255), 6)
        )  # Grosor de línea mayor para la franja más gruesa
        inner_most_arc_rect = QRectF(
            center_x - inner_most_radius,
            center_y - inner_most_radius,
            2 * inner_most_radius,
            inner_most_radius * 2,
        )
        painter.drawArc(
            inner_most_arc_rect, 0 * 16, 180 * 16
        )  # Dibuja solo la mitad superior

        # Dibujar la aguja del tacómetro
        needle_length = radius * 0.8
        needle_width = 5  # Ancho de la aguja en la parte superior

        # Ajustar la aguja para que tenga un ancho mayor en la base
        base_width = 15  # Ancho de la base de la aguja

        # Crear un QPainterPath para la aguja con base más ancha
        path = QPainterPath()
        angle_rad = math.radians(180 - self.angle)
        base_start = QPointF(center_x - base_width / 2, center_y)
        base_end = QPointF(center_x + base_width / 2, center_y)
        tip = QPointF(
            center_x + needle_length * math.cos(angle_rad),
            center_y - needle_length * math.sin(angle_rad),
        )

        path.moveTo(base_start)
        path.lineTo(base_end)
        path.lineTo(tip)
        path.lineTo(base_start)

        # Configurar el pincel del pintor para la aguja
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 0, 0))
        painter.drawPath(path)
    
    def showEvent(self, event):
        """Overrides the showEvent to play the sound when the widget is shown."""
        super().showEvent(event)
        self.play_load_sound()
        
    def play_load_sound(self):
        if self.sound:
            self.sound.play()


# Funcionalidad para optimizar los recursos del sistema
def optimize_system_resources(exclude_pid=None):
    """
    Optimize system resources by terminating processes consuming too much memory.

    :param exclude_pid: PID of the process to exclude from termination.
    """
    memory_threshold = 500  # Memory threshold in MB

    for proc in psutil.process_iter(["pid", "name", "memory_info"]):
        try:
            # Exclude the process with the given PID
            if exclude_pid and proc.info["pid"] == exclude_pid:
                continue

            # Check if process memory usage exceeds the threshold
            if proc.info["memory_info"].rss > memory_threshold * 1024 * 1024:
                print(
                    f"Terminating process {proc.info['name']} (PID: {proc.info['pid']}) using {proc.info['memory_info'].rss / (1024 * 1024):.2f} MB"
                )
                proc.terminate()

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
