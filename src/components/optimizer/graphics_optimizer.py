from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QLinearGradient
import qtawesome as qta

class GraphicsOptimizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
    
    # Arreglo de iconos para el tachometer
    icons = [
        "mdi.speedometer-slow",
        "mdi.speedometer-medium",
        "mdi.speedometer",
    ]

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