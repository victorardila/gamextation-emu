from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QLinearGradient, QColor, QFont
from PyQt5.QtCore import Qt, QPointF, QRectF


class GamepadInteractive(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(600, 400)
        self.button_positions = {
            "A": QPointF(850, 220),
            "B": QPointF(900, 175),
            "X": QPointF(800, 175),
            "Y": QPointF(850, 130),
        }
        self.button_radius = 30
        self.setMouseTracking(True)

    def paintEvent(self, event):
        # ?: Dibujar la silueta del mando de juego
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(70, 70, 70, 150))
        gradient.setColorAt(0.5, QColor(90, 90, 90, 130))
        gradient.setColorAt(1.0, QColor(110, 120, 110, 180))

        brush = QBrush(gradient)
        painter.setBrush(brush)

        path = self.createControllerPath()

        bounding_rect = path.boundingRect()
        path.translate(
            (self.width() - bounding_rect.width()) / 2 - bounding_rect.left(),
            (self.height() - bounding_rect.height()) / 2 - bounding_rect.top(),
        )

        painter.drawPath(path)
        # Todo: partes del joystick
        self.draweIconJoystick(painter, path)
        self.drawButtonsActions(painter, path)
        self.drawButtonOptions(painter, path)
        self.drawDPad(painter, path)
        self.drawJoysticks(painter, path)
        self.drawBumpers(painter, path)
        self.drawTriggers(painter, path)

    def createControllerPath(self):
        # ? :
        path = QPainterPath()
        width_scale = 2.4
        height_scale = 1.7

        path.moveTo(300 * width_scale, 50 * height_scale)
        path.cubicTo(
            200 * width_scale,
            20 * height_scale,
            150 * width_scale,
            70 * height_scale,
            145 * width_scale,
            150 * height_scale,
        )
        path.cubicTo(
            135 * width_scale,
            180 * height_scale,
            125 * width_scale,
            190 * height_scale,
            120 * width_scale,
            260 * height_scale,
        )
        path.cubicTo(
            118 * width_scale,
            300 * height_scale,
            160 * width_scale,
            322 * height_scale,
            190 * width_scale,
            300 * height_scale,
        )
        path.cubicTo(
            230 * width_scale,
            280 * height_scale,
            220 * width_scale,
            250 * height_scale,
            300 * width_scale,
            255 * height_scale,
        )

        path.moveTo(300 * width_scale, 50 * height_scale)

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

    def draweIconJoystick(self, painter, path):
        # ?: Dibujar el icono del joystick en el centro superior del mando (icono importado)
        pass

    def drawDPad(self, painter, path):
        # ?: Dibujar el D-Pad en la parte izquierda del mando (arriba, abajo, izquierda, derecha)
        pass

    def drawJoysticks(self, painter, path):
        # ?: Dibujar los joysticks uno en la parte izquierda superior y otro en la parte derecha inferior
        pass

    def drawBumpers(self, painter, path):
        # ?: Dibujar los bumpers en la parte superior del mando LB, RB
        pass

    def drawTriggers(self, painter, path):
        # ?: Dibujar los triggers en la parte inferior del mando LT, RT
        pass

    def drawButtonOptions(self, painter, path):
        # ?: Dibujar los botones de opciones en la parte centro superior del mando debajo del Icono del joystick
        pass

    def drawButtonsActions(self, painter, path):
        # ?: Dibujar los botones de acción en la parte derecha del mando A, B, X, Y
        painter.setPen(Qt.NoPen)
        button_color = QColor(0, 0, 0, 150)
        painter.setBrush(QBrush(button_color))

        for label, pos in self.button_positions.items():
            painter.drawEllipse(pos, self.button_radius, self.button_radius)
            painter.setPen(Qt.white)
            painter.setFont(QFont("Arial", 12))
            painter.drawText(
                QRectF(
                    pos.x() - self.button_radius,
                    pos.y() - self.button_radius,
                    2 * self.button_radius,
                    2 * self.button_radius,
                ),
                Qt.AlignCenter,
                label,
            )
            painter.setPen(Qt.NoPen)

    def mouseMoveEvent(self, event):
        cursor_hover = False

        for pos in self.button_positions.values():
            if (event.pos() - pos).manhattanLength() <= self.button_radius:
                cursor_hover = True
                break

        if cursor_hover:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
