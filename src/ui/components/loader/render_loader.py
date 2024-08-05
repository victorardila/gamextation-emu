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

        self.angle1 = 0  # Ángulo para el primer círculo
        self.angle2 = 0  # Ángulo para el segundo círculo

    def paintEvent(self, event):
        """Dibuja el loader con animación de rotación."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Color de fondo
        painter.fillRect(self.rect(), QColor(0, 0, 0, 150))

        # Configurar el color del primer loader (blanco)
        color1 = QColor(255, 255, 255)
        pen1 = QPen(color1)
        pen1.setWidth(6)  # Grosor del pen para el primer círculo
        painter.setPen(pen1)
        painter.setBrush(QBrush(color1))

        # Calcular el centro del widget
        center = self.rect().center()

        # Calcular el tamaño del primer círculo
        radius = min(self.rect().width(), self.rect().height()) // 4
        rect1 = QRect(center.x() - radius, center.y() - radius, 2 * radius, 2 * radius)

        # Dibujar el primer círculo giratorio
        painter.drawArc(rect1, self.angle1 * 16, 180 * 16)

        # Configurar el color del segundo loader (verde llamativo)
        color2 = QColor(0, 255, 0)  # Verde llamativo
        pen2 = QPen(color2)
        pen2.setWidth(6)  # Grosor del pen para el segundo círculo
        painter.setPen(pen2)
        painter.setBrush(QBrush(color2))

        # Calcular el tamaño del segundo círculo (mismo tamaño que el primero)
        rect2 = QRect(center.x() - radius + 10, center.y() - radius + 10, 2 * radius - 20, 2 * radius - 20)

        # Dibujar el segundo círculo giratorio
        painter.drawArc(rect2, -self.angle2 * 16, -180 * 16)

        painter.end()

    def update_animation(self):
        """Actualiza la animación del loader."""
        self.angle1 = (self.angle1 + 30) % 360
        self.angle2 = (self.angle2 - 30) % 360  # Mover en sentido contrario
        self.update()  # Actualiza el widget para redibujar

    def show_centered(self, parent):
        """Muestra el loader centrado sobre el widget padre."""
        parent_geometry = parent.geometry()
        self.move(parent_geometry.center() - self.rect().center())
        self.show()