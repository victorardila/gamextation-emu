from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer, Qt, QSize, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen

class RenderLoader(QWidget):
    """Widget para mostrar un loader con animación de rotación."""
    def __init__(self, Time=None, request=None):
        super().__init__()
        self.request = request
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(200, 200)  # Tamaño fijo del loader
        self.init_loader()

    def init_loader(self):
        """Inicializa el diseño y la animación del loader."""
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        # Crear el label para el loader
        self.loader_label = QLabel(self)
        self.loader_label.setAlignment(Qt.AlignCenter)
        self.loader_label.setFixedSize(QSize(100, 100))
        self.layout.addWidget(self.loader_label)

        # Configurar el temporizador para la animación
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)  # Intervalo de actualización de la animación

        self.angle = 0
        self.reverse_angle = 0  # Ángulo para el segundo círculo

    def paintEvent(self, event):
        """Dibuja el loader con animación de rotación."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Color de fondo
        painter.fillRect(self.rect(), QColor(0, 0, 0, 150))

        # Configurar el color del primer loader (blanco)
        color = QColor(255, 255, 255)
        pen = QPen(color)
        pen.setWidth(6)  # Establece el grosor del pen

        painter.setPen(pen)
        painter.setBrush(QBrush(color))

        # Calcular el centro del widget
        center = self.rect().center()

        # Calcular el tamaño del círculo
        radius = min(self.rect().width(), self.rect().height()) // 4
        rect = QRect(center.x() - radius, center.y() - radius, 2 * radius, 2 * radius)

        # Dibujar el primer círculo giratorio (a la derecha)
        painter.drawArc(rect, self.angle * 16, 180 * 16)

        # Configurar el color del segundo loader (verde)
        color = QColor(0, 255, 0)  # Color verde llamativo
        pen.setColor(color)
        painter.setPen(pen)
        painter.setBrush(QBrush(color))

        # Dibujar el segundo círculo giratorio (a la izquierda)
        painter.drawArc(rect, self.reverse_angle * 16, -180 * 16)  # Dirección opuesta

        painter.end()

    def update_animation(self):
        """Actualiza la animación del loader."""
        self.angle = (self.angle + 30) % 360
        self.reverse_angle = (self.reverse_angle - 30) % 360  # Movimiento en dirección opuesta
        self.update()  # Actualiza el widget para redibujar

    def show_centered(self, parent):
        """Muestra el loader centrado sobre el widget padre."""
        parent_geometry = parent.geometry()
        self.move(parent_geometry.center() - self.rect().center())
        self.show()