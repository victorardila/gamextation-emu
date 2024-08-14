from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QLinearGradient, QColor, QFont
from PyQt5.QtCore import Qt, QPointF, QRectF


class JoystickInteractive(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(600, 400)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Crear un gradiente lineal para el efecto metálico oscuro
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(
            0.0, QColor(70, 70, 70, 150)
        )  # Color más oscuro en la parte superior
        gradient.setColorAt(0.5, QColor(90, 90, 90, 130))  # Color medio
        gradient.setColorAt(
            1.0, QColor(110, 120, 110, 180)
        )  # Color más claro en la parte inferior

        # Aplicar el gradiente al pincel
        brush = QBrush(gradient)
        painter.setBrush(brush)

        # Crear la silueta del mando Xbox One con escala
        path = self.createControllerPath()

        # Ajustar el path para centrarlo en el widget
        bounding_rect = path.boundingRect()
        path.translate(
            (self.width() - bounding_rect.width()) / 2 - bounding_rect.left(),
            (self.height() - bounding_rect.height()) / 2 - bounding_rect.top(),
        )

        painter.drawPath(path)
        self.drawButtonsRight(painter, path)

    def createControllerPath(self):
        path = QPainterPath()

        # Ajuste de proporciones: hacer que el mando sea un poco más ancho que alto
        width_scale = 2.4  # Factor para hacer el mando más ancho
        height_scale = 1.7  # Factor para hacer el mando más alto

        # Comienza en la parte superior del mando, en el centro
        path.moveTo(300 * width_scale, 50 * height_scale)

        # Trazar la parte superior del mando
        path.cubicTo(
            200 * width_scale,
            20 * height_scale,
            150 * width_scale,
            70 * height_scale,
            145 * width_scale,
            150 * height_scale,
        )  # Lado izquierdo superior
        path.cubicTo(
            135 * width_scale,
            180 * height_scale,
            125 * width_scale,
            190 * height_scale,
            120 * width_scale,
            260 * height_scale,
        )  # Izquierda media
        # Trazar la curva hacia abajo y alrededor del área de agarre izquierda
        path.cubicTo(
            118 * width_scale,
            300 * height_scale,
            160 * width_scale,
            322 * height_scale,
            190 * width_scale,
            300 * height_scale,
        )  # Parte inferior izquierda
        path.cubicTo(
            230 * width_scale,
            280 * height_scale,
            220 * width_scale,
            250 * height_scale,
            300 * width_scale,
            255 * height_scale,
        )  # Centro inferior

        # Parte derecha (simetría manual)
        path.moveTo(
            300 * width_scale, 50 * height_scale
        )  # Regresar al inicio para la parte derecha

        # Lado derecho superior
        path.cubicTo(
            400 * width_scale,
            20 * height_scale,
            450 * width_scale,
            70 * height_scale,
            455 * width_scale,
            150 * height_scale,
        )
        path.cubicTo(
            465 * width_scale,
            180 * height_scale,
            475 * width_scale,
            190 * height_scale,
            480 * width_scale,
            260 * height_scale,
        )
        # Parte inferior derecha
        path.cubicTo(
            482 * width_scale,
            310 * height_scale,
            440 * width_scale,
            322 * height_scale,
            400 * width_scale,
            300 * height_scale,
        )
        path.cubicTo(
            360 * width_scale,
            280 * height_scale,
            370 * width_scale,
            250 * height_scale,
            300 * width_scale,
            255 * height_scale,
        )

        return path

    def drawButtonsRight(self, painter, path):
        painter.setPen(Qt.NoPen)
        button_color = QColor(0, 0, 0, 150)  # Color de los botones por defecto
        button_radius = 30

        # Definir posiciones de los botones en la parte derecha
        button_positions = {
            "A": QPointF(850, 220),
            "B": QPointF(900, 175),
            "X": QPointF(800, 175),
            "Y": QPointF(850, 130),
        }

        # Dibujar cada botón
        painter.setBrush(QBrush(button_color))
        for label, pos in button_positions.items():
            painter.drawEllipse(pos, button_radius, button_radius)
            painter.setPen(Qt.white)
            painter.setFont(QFont("Arial", 12))
            painter.drawText(
                QRectF(
                    pos.x() - button_radius,
                    pos.y() - button_radius,
                    2 * button_radius,
                    2 * button_radius,
                ),
                Qt.AlignCenter,
                label,
            )
            painter.setPen(Qt.NoPen)
