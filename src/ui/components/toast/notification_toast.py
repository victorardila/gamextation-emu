from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QGraphicsDropShadowEffect,
)
from PyQt5.QtGui import QPainter, QColor, QLinearGradient, QPixmap
from PyQt5.QtCore import Qt, QSize
import qtawesome as qta

class NotificationToast(QWidget):
    def __init__(self, message, icon=None, icon_size=QSize(24, 24), shadow_blur_radius=2, shadow_offset=1):
        super().__init__()
        self.message = message
        self.icon = icon
        self.icon_size = icon_size
        self.shadow_blur_radius = shadow_blur_radius
        self.shadow_offset = shadow_offset
        self.init_noti()

    def init_noti(self):
        # Configurar el tamaño fijo del widget
        self.setFixedSize(500, 100)  # Ajusta el tamaño para acomodar ambos labels y la línea

        # Configurar el estilo del widget
        self.setStyleSheet("""
            background: transparent;
            border-radius: 50px;
        """)

        # Aplicar un efecto de sombra para mejorar la visibilidad de los bordes
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(self.shadow_blur_radius)  # Ajustar el grosor de la sombra
        shadow_effect.setOffset(self.shadow_offset, self.shadow_offset)  # Ajustar el desplazamiento de la sombra
        shadow_effect.setColor(QColor(0, 0, 0, 160))  # Color de la sombra
        self.setGraphicsEffect(shadow_effect)

        # Configurar el layout horizontal
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)  # Alinear el layout al centro
        self.setLayout(self.layout)

        # Agregar el ícono si se proporciona
        if self.icon:
            self.icon_label = QLabel()
            self.icon_label.setPixmap(self.load_icon(self.icon, self.icon_size))
            self.icon_label.setFixedSize(self.icon_size)  # Usar QSize directamente
            self.layout.addWidget(self.icon_label)

        # Agregar el mensaje a la notificación
        self.message_label = QLabel(self.message)
        self.message_label.setStyleSheet("color: white; font-size: 18px;")
        self.message_label.setAlignment(Qt.AlignCenter)  # Centrar el texto en el QLabel
        self.message_label.setWordWrap(True)  # Permitir que el texto se distribuya en varias líneas
        self.message_label.setFixedWidth(400)  # Ajustar el ancho máximo del QLabel si es necesario
        self.layout.addWidget(self.message_label)

    def load_icon(self, icon_name, size):
        # Utiliza qtawesome para obtener el ícono
        try:
            pixmap = qta.icon(icon_name, color='white', size=size).pixmap(size)
            return pixmap
        except Exception as e:
            print(f"Error loading icon: {e}")
            return QPixmap(size)  # Retorna un pixmap vacío en caso de error

    def paintEvent(self, event):
        """Custom paint event to draw rounded corners with gradient background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Crear un gradiente lineal
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(169, 169, 169, 150))  # 51 ≈ 20% transparencia
        gradient.setColorAt(1, QColor(105, 105, 105, 170))  # 102 ≈ 40% transparencia

        # Configurar el pincel del pintor con el gradiente
        painter.setBrush(gradient)

        # Dibujar el rectángulo redondeado con el gradiente
        painter.drawRoundedRect(self.rect(), 50, 50)