from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import (
    QPainter,
    QPainterPath,
    QBrush,
    QLinearGradient,
    QColor,
    QFont,
    QRadialGradient,
)
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
        # ? : Crear la silueta del mando de juego
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
        # ?: Dibujar el icono del joystick en el centro superior del mando
        pass

    def drawDPad(self, painter, path):
        # ?: Dibujar el D-Pad en la parte izquierda del mando (arriba, abajo, izquierda, derecha)

        # Configurar los colores del D-Pad
        dpad_color = QColor(30, 30, 30)  # Color negro para el D-Pad
        cross_color = QColor(
            50, 50, 50
        )  # Color gris ligeramente más claro para la cruz

        # Obtener el rectángulo delimitador del mando
        bounding_rect = path.boundingRect()
        center_x = (
            bounding_rect.left() + 300
        )  # Ajustar la posición horizontal del D-Pad
        center_y = bounding_rect.center().y() + 80

        # Tamaño del D-Pad
        dpad_radius = 50  # Radio del círculo del D-Pad
        cross_thickness = 20  # Grosor de la cruz

        # Reducir el tamaño de la cruz para que sea más pequeña que el círculo
        cross_radius = (
            dpad_radius * 0.8
        )  # Radio del círculo en el que se dibuja la cruz (80% del radio del D-Pad)
        cross_thickness = (
            cross_thickness  # Grosor de la cruz, puedes ajustar si es necesario
        )

        # Dibujar el círculo del D-Pad
        painter.setBrush(QBrush(dpad_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(
            int(center_x - dpad_radius),
            int(center_y - dpad_radius),
            int(2 * dpad_radius),
            int(2 * dpad_radius),
        )

        # Crear el alto relieve para el círculo del D-Pad
        gradient = QRadialGradient(center_x, center_y, dpad_radius)
        gradient.setColorAt(0.0, dpad_color.darker(120))  # Centro más claro
        gradient.setColorAt(1.0, dpad_color)  # Borde más oscuro

        # Aplicar el degradado al pincel para el alto relieve
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(
            int(center_x - dpad_radius),
            int(center_y - dpad_radius),
            int(2 * dpad_radius),
            int(2 * dpad_radius),
        )

        # Configurar el pincel y el color para la cruz
        painter.setBrush(QBrush(cross_color))
        painter.setPen(Qt.NoPen)

        # Líneas horizontales y verticales de la cruz
        # Línea vertical
        painter.drawRect(
            int(center_x - cross_thickness / 2),
            int(center_y - cross_radius),
            int(cross_thickness),
            int(2 * cross_radius),
        )
        # Línea horizontal
        painter.drawRect(
            int(center_x - cross_radius),
            int(center_y - cross_thickness / 2),
            int(2 * cross_radius),
            int(cross_thickness),
        )

    def drawJoysticks(self, painter, path):
        # ?: Dibujar los joysticks uno en la parte izquierda superior y otro en la parte derecha inferior
        # Configurar los colores para los joysticks
        outer_color = QColor(50, 50, 50)  # Negro ligeramente más claro
        inner_color = QColor(30, 30, 30)  # Negro oscuro

        # Configurar el pincel y el color para el joystick exterior
        painter.setBrush(QBrush(outer_color))
        painter.setPen(Qt.NoPen)

        # Definir los tamaños y posiciones de los joysticks
        joystick_radius = 50  # Radio del joystick exterior
        inner_radius = 40  # Radio del joystick interior

        # Obtener el rectángulo delimitador del mando
        bounding_rect = path.boundingRect()
        center_x = bounding_rect.center().x()
        center_y = bounding_rect.center().y()

        # Posiciones ajustadas de los joysticks (ajustar según la posición deseada)
        joystick_positions = {
            "left": QPointF(
                center_x - 220, center_y - 120
            ),  # Posición del joystick en la parte superior izquierda
            "right": QPointF(
                center_x + 100, center_y + 80
            ),  # Posición del joystick en la parte inferior derecha
        }

        # Dibujar cada joystick
        for pos in joystick_positions.values():
            # Dibujar el joystick exterior
            painter.drawEllipse(pos, joystick_radius, joystick_radius)

            # Configurar el pincel y el color para el joystick interior
            # Crear un degradado radial para simular el alto relieve
            gradient = QRadialGradient(pos, inner_radius)
            gradient.setColorAt(0.0, QColor(50, 50, 50))  # Centro más oscuro
            gradient.setColorAt(0.8, QColor(30, 30, 30))  # Borde más claro

            # Aplicar el degradado al pincel
            painter.setBrush(QBrush(gradient))

            # Dibujar el joystick interior con alto relieve
            painter.drawEllipse(pos, inner_radius, inner_radius)

            # Restaurar el pincel al color anterior para el joystick exterior
            painter.setBrush(QBrush(outer_color))

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
        button_outer_color = QColor(30, 30, 30, 200)  # Color base de los botones
        button_highlight_color = QColor(50, 50, 50, 150)  # Color para el alto relieve
        button_shadow_color = QColor(10, 10, 10, 150)  # Color para la sombra

        painter.setPen(Qt.NoPen)

        for label, pos in self.button_positions.items():
            # Crear un degradado radial para el alto relieve
            gradient = QRadialGradient(pos, self.button_radius)
            gradient.setColorAt(0.0, button_highlight_color)  # Centro más claro
            gradient.setColorAt(0.8, button_outer_color)  # Borde más oscuro

            # Aplicar el degradado al pincel para el alto relieve
            painter.setBrush(QBrush(gradient))

            # Dibujar el botón
            painter.drawEllipse(pos, self.button_radius, self.button_radius)

            # Configurar el pincel para la sombra del botón
            shadow_gradient = QRadialGradient(pos, self.button_radius * 0.8)
            shadow_gradient.setColorAt(0.0, QColor(0, 0, 0, 100))  # Sombra oscura
            shadow_gradient.setColorAt(
                1.0, QColor(0, 0, 0, 0)
            )  # Sin sombra en el borde

            # Aplicar el degradado de sombra
            painter.setBrush(QBrush(shadow_gradient))
            painter.drawEllipse(
                pos + QPointF(2, 2), self.button_radius, self.button_radius
            )  # Ajustar la posición de la sombra

            # Configurar el texto del botón
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

            # Restaurar el pincel al color base de los botones
            painter.setBrush(QBrush(button_outer_color))
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
