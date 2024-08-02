from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtGui import QPainter, QColor, QPixmap, QFont
from PyQt5.Qt import Qt

class RenderLoader(QWidget):
    def __init__(self):
        super().__init__()
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

    def paintEvent(self, event):
        """Dibuja el loader con animación de rotación."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Color de fondo
        painter.fillRect(self.rect(), QColor(0, 0, 0, 150))

        # Configurar el color del loader
        color = QColor(255, 255, 255)
        painter.setPen(color)
        painter.setBrush(color)

        # Dibujar el círculo giratorio
        painter.drawArc(self.loader_label.rect().adjusted(10, 10, -10, -10), 
                        self.angle * 16, 180 * 16)
        painter.end()

    def update_animation(self):
        """Actualiza la animación del loader."""
        self.angle = (self.angle + 10) % 360
        self.update()  # Redibuja el widget

    def show_centered(self, parent_widget):
        """Muestra el widget de loader centrado en el widget padre."""
        parent_rect = parent_widget.rect()
        self.move((parent_rect.width() - self.width()) // 2,
                  (parent_rect.height() - self.height()) // 2)
        self.show()
