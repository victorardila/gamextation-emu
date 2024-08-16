from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import (
    QPainter,
    QPainterPath,
    QBrush,
    QLinearGradient,
    QColor,
    QFont,
    QRadialGradient,
    QPen,
    QPolygonF,
    QTransform,
)
from PyQt5.QtCore import Qt, QPointF, QRectF, QSize, QSizeF
import qtawesome as qta
import math


class GamepadInteractive(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(600, 400)
        self.setMouseTracking(True)
        self.dpad_rect = QRectF()
        # defino el area del mouse event
        self.button_options = {}
        self.button_actions = {}
        self.joysticks_rects = {"left": QRectF(), "right": QRectF()}
        self.bumper_rects = {"left": QRectF(), "right": QRectF()}
        self.trigger_rects = {"left": QRectF(), "right": QRectF()}
        # Color actual del mallado
        self.mesh_color = QColor(200, 200, 200, 50)  # Color por defecto
        # Estado de los botones
        self.action_button_pressed = None
        self.option_button_pressed = None
        self.dpad_button_pressed = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }

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

        # posicionar la silueta en el centro del widget
        bounding_rect = path.boundingRect()
        path.translate(
            (self.width() - bounding_rect.width()) / 2 - bounding_rect.left(),
            (self.height() - bounding_rect.height()) / 0.8 - bounding_rect.top(),
        )

        # Limitar el área de dibujo para la malla a la silueta
        painter.save()
        painter.setClipPath(path)  # Establecer la ruta de la silueta como clip

        # Dibujar la malla dentro de la silueta
        self.drawMesh(painter, path)

        # Restaurar el estado del painter
        painter.restore()

        # Dibujar la silueta del mando de juego
        painter.setPen(QPen(gradient, 1))  # Usar el gradiente para la silueta
        painter.drawPath(path)

        # Todo: partes del joystick
        self.drawIconGamepad(painter, path)
        self.drawButtonsActions(painter, path)
        self.drawButtonOptions(painter, path)
        self.drawDPad(painter, path)
        self.drawJoysticks(painter, path)
        self.drawBumpers(painter, path)
        self.drawTriggers(painter, path)

    def drawMesh(self, painter, path):
        # Dibujar la malla con el color actual
        pen = QPen(self.mesh_color)  # Usar el color actual del mallado
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        bounding_rect = path.boundingRect()
        step = 20
        for x in range(int(bounding_rect.left()), int(bounding_rect.right()), step):
            for y in range(int(bounding_rect.top()), int(bounding_rect.bottom()), step):
                if path.contains(QPointF(x + step / 2, y + step / 2)):
                    painter.drawRect(x, y, step, step)

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

    def drawIconGamepad(self, painter, path):
        # ?: Dibujar el icono del joystick en el centro superior del mando
        pass

    def drawJoysticks(self, painter, path):
        # ?: Dibujar los joysticks uno en la parte izquierda superior y otro en la parte derecha inferior
        # Configurar los colores para los joysticks
        outer_color = QColor(50, 50, 50)  # Negro ligeramente más claro
        inner_color = QColor(30, 30, 30)  # Negro oscuro
        cup_border_color = QColor(
            100, 100, 100, 90
        )  # Color para el borde de la "chupita"

        # Configurar el pincel y el color para el joystick exterior
        painter.setBrush(QBrush(outer_color))
        painter.setPen(Qt.NoPen)

        # Definir los tamaños y posiciones de los joysticks
        joystick_radius = 60  # Radio del joystick exterior
        inner_radius = 40  # Radio del joystick interior
        cup_radius = 36  # Radio de la "chupita"

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
                center_x + 100, center_y + 60
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

            # Dibujar la "chupita" en la parte superior de ambos joysticks como arcos parciales
            painter.setBrush(Qt.NoBrush)  # Sin relleno
            painter.setPen(
                QPen(cup_border_color, 2)
            )  # Borde de la "chupita" con grosor 2

            # Dibujar arcos en lugar de un círculo completo
            arc_angle_start = [
                30 * 16,  # Primer arco
                150 * 20,  # Segundo arco
                320 * 14,  # Tercer arco
            ]  # Ángulos de inicio de los arcos
            arc_span_angle = 60 * 16  # Ángulo que abarca cada arco

            for start_angle in arc_angle_start:
                painter.drawArc(
                    QRectF(
                        pos.x() - cup_radius,
                        pos.y() - cup_radius,
                        2 * cup_radius,
                        2 * cup_radius,
                    ),
                    start_angle,
                    arc_span_angle,
                )

            # Restaurar el pincel al color anterior para el joystick exterior
            painter.setBrush(QBrush(outer_color))
            painter.setPen(
                Qt.NoPen
            )  # Asegúrate de que no se dibujen bordes adicionales

        # Definir las áreas de los joysticks
        self.joysticks_rects["left"] = QRectF(
            joystick_positions["left"].x() - joystick_radius,
            joystick_positions["left"].y() - joystick_radius,
            2 * joystick_radius,
            2 * joystick_radius,
        )
        self.joysticks_rects["right"] = QRectF(
            joystick_positions["right"].x() - joystick_radius,
            joystick_positions["right"].y() - joystick_radius,
            2 * joystick_radius,
            2 * joystick_radius,
        )

    def drawDPad(self, painter, path):
        dpad_color = QColor(30, 30, 30)
        cross_color = QColor(50, 50, 50)
        highlight_color = QColor(255, 255, 0)  # Amarillo para resaltado
        pressed_color = QColor(
            100, 100, 100
        )  # Gris más oscuro para el estado presionado

        bounding_rect = path.boundingRect()
        center_x = bounding_rect.left() + 300
        center_y = bounding_rect.center().y() + 60

        dpad_radius = 60
        cross_thickness = 20
        cross_radius = dpad_radius * 0.8

        # Dibuja el fondo del D-Pad
        painter.setBrush(QBrush(dpad_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(
            int(center_x - dpad_radius),
            int(center_y - dpad_radius),
            int(2 * dpad_radius),
            int(2 * dpad_radius),
        )

        gradient = QRadialGradient(center_x, center_y, dpad_radius)
        gradient.setColorAt(0.0, dpad_color.darker(120))
        gradient.setColorAt(1.0, dpad_color)
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(
            int(center_x - dpad_radius),
            int(center_y - dpad_radius),
            int(2 * dpad_radius),
            int(2 * dpad_radius),
        )

        # Ajusta el grosor y color de la cruz según el estado de presión
        def draw_cross(painter, pressed_side):
            painter.setBrush(QBrush(cross_color))
            painter.setPen(Qt.NoPen)

            # Ajusta el grosor y la altura según el lado presionado
            if pressed_side == "up":
                painter.drawRect(
                    int(center_x - cross_thickness / 2),
                    int(center_y - cross_radius + 10),  # Menos alto
                    int(cross_thickness),
                    int(2 * (cross_radius - 10)),  # Menos ancho
                )
                painter.drawRect(
                    int(center_x - cross_radius),
                    int(center_y - cross_thickness / 2),
                    int(2 * cross_radius),
                    int(cross_thickness),
                )
            elif pressed_side == "down":
                painter.drawRect(
                    int(center_x - cross_thickness / 2),
                    int(center_y + 10),  # Menos alto
                    int(cross_thickness),
                    int(2 * (cross_radius - 10)),  # Menos ancho
                )
                painter.drawRect(
                    int(center_x - cross_radius),
                    int(center_y - cross_thickness / 2),
                    int(2 * cross_radius),
                    int(cross_thickness),
                )
            elif pressed_side == "left":
                painter.drawRect(
                    int(center_x - cross_radius + 10),  # Menos ancho
                    int(center_y - cross_thickness / 2),
                    int(2 * (cross_radius - 10)),  # Menos alto
                    int(cross_thickness),
                )
                painter.drawRect(
                    int(center_x - cross_thickness / 2),
                    int(center_y - cross_radius),
                    int(cross_thickness),
                    int(2 * cross_radius),
                )
            elif pressed_side == "right":
                painter.drawRect(
                    int(center_x + 10),  # Menos ancho
                    int(center_y - cross_thickness / 2),
                    int(2 * (cross_radius - 10)),  # Menos alto
                    int(cross_thickness),
                )
                painter.drawRect(
                    int(center_x - cross_thickness / 2),
                    int(center_y - cross_radius),
                    int(cross_thickness),
                    int(2 * cross_radius),
                )
            else:
                painter.drawRect(
                    int(center_x - cross_thickness / 2),
                    int(center_y - cross_radius),
                    int(cross_thickness),
                    int(2 * cross_radius),
                )
                painter.drawRect(
                    int(center_x - cross_radius),
                    int(center_y - cross_thickness / 2),
                    int(2 * cross_radius),
                    int(cross_thickness),
                )

        # Dibuja la cruz del D-Pad
        draw_cross(painter, self.dpad_button_pressed)

        icon_up = qta.icon("fa.caret-up", color="gray")
        icon_down = qta.icon("fa.caret-down", color="gray")
        icon_left = qta.icon("fa.caret-left", color="gray")
        icon_right = qta.icon("fa.caret-right", color="gray")

        icon_size = QSize(24, 24)

        gradient_icon = QRadialGradient(0, 0, icon_size.width() / 2)
        gradient_icon.setColorAt(0.0, QColor(200, 200, 200))
        gradient_icon.setColorAt(1.0, QColor(120, 120, 120))

        def create_highlighted_pixmap(icon, highlight):
            pixmap = icon.pixmap(icon_size)
            painter_icon = QPainter(pixmap)
            if highlight:
                painter_icon.setBrush(QBrush(highlight_color))
            else:
                painter_icon.setBrush(QBrush(gradient_icon))
            painter_icon.setPen(Qt.NoPen)
            painter_icon.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter_icon.drawRect(pixmap.rect())
            painter_icon.end()
            return pixmap

        pixmap_up = create_highlighted_pixmap(icon_up, self.dpad_button_pressed["up"])
        pixmap_down = create_highlighted_pixmap(
            icon_down, self.dpad_button_pressed["down"]
        )
        pixmap_left = create_highlighted_pixmap(
            icon_left, self.dpad_button_pressed["left"]
        )
        pixmap_right = create_highlighted_pixmap(
            icon_right, self.dpad_button_pressed["right"]
        )

        # Posiciones de las flechas
        painter.drawPixmap(
            int(center_x - icon_size.width() / 2),
            int(center_y - cross_radius - icon_size.height() / 3),
            pixmap_up,
        )
        painter.drawPixmap(
            int(center_x - icon_size.width() / 2),
            int(center_y + cross_radius - icon_size.height() / 1.5),
            pixmap_down,
        )
        painter.drawPixmap(
            int(center_x - cross_radius - icon_size.width() / 3),
            int(center_y - icon_size.height() / 2),
            pixmap_left,
        )
        painter.drawPixmap(
            int(center_x + cross_radius - icon_size.width() / 1.5),
            int(center_y - icon_size.height() / 2),
            pixmap_right,
        )

        self.dpad_rect = QRectF(
            center_x - dpad_radius,
            center_y - dpad_radius,
            2 * dpad_radius,
            2 * dpad_radius,
        )

    def drawBumpers(self, painter, path):
        # ?: Dibujar los bumpers (L1 y R1) en la parte superior del mando
        bumper_color = QColor(50, 50, 50)  # Color para los bumpers
        border_color = QColor(30, 30, 30)  # Color para el borde de los bumpers
        border_width = 2  # Grosor del borde

        # Obtener el rectángulo delimitador del mando
        bounding_rect = path.boundingRect()
        center_x = bounding_rect.center().x()
        top_y = bounding_rect.top() + 10

        # Definir tamaños y posiciones de los bumpers
        bumper_width = 80
        bumper_height = 30

        # Posiciones ajustadas de los bumpers
        left_bumper_rect = QRectF(center_x - 160, top_y, bumper_width, bumper_height)
        right_bumper_rect = QRectF(center_x + 80, top_y, bumper_width, bumper_height)

        # Configurar el lápiz para el borde de los bumpers
        painter.setPen(
            QPen(border_color, border_width)
        )  # Establecer color y grosor del borde

        # Dibujar los bumpers
        painter.setBrush(QBrush(bumper_color))
        painter.drawRoundedRect(left_bumper_rect, 10, 10)
        painter.drawRoundedRect(right_bumper_rect, 10, 10)

        # Configurar el estilo del texto para los labels
        font = QFont("Arial", 12, QFont.Bold)  # Fuente del label
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))  # Color del texto

        # Calcular el texto a dibujar en los bumpers
        left_bumper_text = "L1"
        right_bumper_text = "R1"

        # Calcular el rectángulo del texto para centrarlo en el bumper
        left_bumper_text_rect = left_bumper_rect.adjusted(
            0, 0, 0, -5
        )  # Ajustar el rectángulo para el texto
        right_bumper_text_rect = right_bumper_rect.adjusted(
            0, 0, 0, -5
        )  # Ajustar el rectángulo para el texto

        # Dibujar los labels en los bumpers
        painter.drawText(left_bumper_text_rect, Qt.AlignCenter, left_bumper_text)
        painter.drawText(right_bumper_text_rect, Qt.AlignCenter, right_bumper_text)

        # Definir las áreas de los bumpers
        self.bumper_rects["left"] = left_bumper_rect
        self.bumper_rects["right"] = right_bumper_rect

    def drawTriggers(self, painter, path):
        # ?: Dibujar los triggers (L2 y R2) en la parte superior trasera del mando
        trigger_color = QColor(70, 70, 70)  # Color para los triggers
        border_color = QColor(30, 30, 30)  # Color para el borde de los triggers
        border_width = 1  # Grosor del borde

        # Obtener el rectángulo delimitador del mando
        bounding_rect = path.boundingRect()
        center_x = bounding_rect.center().x()
        top_y = bounding_rect.top() - 15  # Ajuste para la posición vertical

        # Definir tamaños y posiciones de los triggers
        trigger_width = 60
        trigger_height = 40

        # Posiciones ajustadas de los triggers
        left_trigger_rect = QRectF(center_x - 210, top_y, trigger_width, trigger_height)
        right_trigger_rect = QRectF(
            center_x + 170, top_y, trigger_width, trigger_height
        )

        # Definir la inclinación del triángulo
        angle = 30  # Ángulo de inclinación en grados

        def create_triangle(rect, angle):
            """Crea un triángulo con la inclinación especificada."""
            # Convertir el ángulo a radianes
            radians = math.radians(angle)
            # Calcular los puntos del triángulo
            points = [
                QPointF(
                    rect.center().x(), rect.top()
                ),  # Punto superior (en el centro del rectángulo)
                QPointF(rect.left(), rect.bottom()),  # Punto inferior izquierdo
                QPointF(rect.right(), rect.bottom()),  # Punto inferior derecho
            ]
            # Rotar el triángulo alrededor de su centro
            matrix = QTransform()
            matrix.translate(rect.center().x(), rect.center().y())  # Mover al centro
            matrix.rotate(angle)  # Rotar
            matrix.translate(-rect.center().x(), -rect.center().y())  # Mover de vuelta

            rotated_points = [matrix.map(p) for p in points]
            return QPolygonF(rotated_points)

        # Crear triángulos para los triggers
        left_trigger_triangle = create_triangle(left_trigger_rect, angle)
        right_trigger_triangle = create_triangle(right_trigger_rect, angle)

        # Configurar el lápiz para el borde de los triggers
        painter.setPen(
            QPen(border_color, border_width)
        )  # Establecer color y grosor del borde

        # Dibujar los triggers
        painter.setBrush(QBrush(trigger_color))
        painter.drawPolygon(left_trigger_triangle)
        painter.drawPolygon(right_trigger_triangle)

        # Configurar el estilo del texto para los labels
        font = QFont("Arial", 12, QFont.Bold)  # Fuente del label
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))  # Color del texto

        # Calcular el texto a dibujar en los triggers
        left_trigger_text = "L2"
        right_trigger_text = "R2"

        # Calcular el rectángulo del texto para centrarlo en el trigger
        def center_text_in_triangle(triangle, text):
            """Centrar el texto dentro del triángulo."""
            rect = triangle.boundingRect()
            text_rect = QRectF(rect.center() - QPointF(20, 10), QSizeF(40, 20))
            return text_rect

        left_trigger_text_rect = center_text_in_triangle(
            left_trigger_triangle, left_trigger_text
        )
        right_trigger_text_rect = center_text_in_triangle(
            right_trigger_triangle, right_trigger_text
        )

        # Dibujar los labels en los triggers
        painter.drawText(left_trigger_text_rect, Qt.AlignCenter, left_trigger_text)
        painter.drawText(right_trigger_text_rect, Qt.AlignCenter, right_trigger_text)
        # Definir las áreas de los triggers (puedes ajustarlo según la forma)
        self.trigger_rects["left"] = left_trigger_rect
        self.trigger_rects["right"] = right_trigger_rect

    def drawButtonOptions(self, painter, path):
        button_outer_color = QColor(30, 30, 30, 200)
        button_highlight_color = QColor(50, 50, 150, 150)
        button_shadow_color = QColor(10, 10, 10, 150)

        bounding_rect = path.boundingRect()
        center_x = bounding_rect.center().x()
        top_y = bounding_rect.top() + 150

        button_positions = {
            "table": QPointF(center_x - 65, top_y),
            "user": QPointF(center_x - 10, top_y + 55),
            "bars": QPointF(center_x + 45, top_y),
        }

        button_radius = 18
        painter.setPen(Qt.NoPen)

        self.button_options = {}

        for icon_name, pos in button_positions.items():
            gradient = QRadialGradient(pos, button_radius)
            gradient.setColorAt(0.0, button_highlight_color)
            gradient.setColorAt(0.8, button_outer_color)

            painter.setBrush(QBrush(gradient))

            if self.option_button_pressed == icon_name:
                pressed_pos = pos + QPointF(2, 2)
                painter.drawEllipse(
                    pressed_pos, button_radius * 0.95, button_radius * 0.95
                )
            else:
                painter.drawEllipse(pos, button_radius, button_radius)

            shadow_gradient = QRadialGradient(pos, button_radius * 0.8)
            shadow_gradient.setColorAt(0.0, QColor(0, 0, 0, 100))
            shadow_gradient.setColorAt(1.0, QColor(0, 0, 0, 0))

            painter.setBrush(QBrush(shadow_gradient))
            painter.drawEllipse(pos + QPointF(2, 2), button_radius, button_radius)

            # Dibujar el icono
            icon_size = QSize(24, 24)
            icon = qta.icon(f"fa.{icon_name}", color="white")
            pixmap = icon.pixmap(icon_size)

            painter.drawPixmap(
                int(pos.x() - icon_size.width() / 2),
                int(pos.y() - icon_size.height() / 2),
                pixmap,
            )

            # Definir el área activa
            self.button_options[icon_name] = QRectF(
                pos.x() - button_radius,
                pos.y() - button_radius,
                2 * button_radius,
                2 * button_radius,
            )

            painter.setBrush(QBrush(button_outer_color))
            painter.setPen(Qt.NoPen)

    def drawButtonsActions(self, painter, path):
        button_outer_color = QColor(30, 30, 30, 200)
        button_highlight_color = QColor(50, 50, 50, 150)
        button_shadow_color = QColor(10, 10, 10, 150)

        button_text_colors = {
            "A": QColor(0, 255, 0),
            "B": QColor(255, 0, 0),
            "X": QColor(0, 0, 255),
            "Y": QColor(255, 255, 0),
        }

        button_radius = 35
        painter.setPen(Qt.NoPen)

        bounding_rect = path.boundingRect()
        center_x = bounding_rect.center().x()
        center_y = bounding_rect.center().y()

        button_positions = {
            "A": QPointF(center_x + 210, center_y - 20),
            "B": QPointF(center_x + 270, center_y - 70),
            "X": QPointF(center_x + 150, center_y - 70),
            "Y": QPointF(center_x + 210, center_y - 120),
        }

        self.button_actions = {}

        for label, pos in button_positions.items():
            gradient = QRadialGradient(pos, button_radius)
            gradient.setColorAt(0.0, button_highlight_color)
            gradient.setColorAt(0.8, button_outer_color)

            painter.setBrush(QBrush(gradient))

            # Modificar tamaño o posición si el botón está presionado
            if self.action_button_pressed == label:
                pressed_pos = pos + QPointF(2, 2)
                painter.drawEllipse(
                    pressed_pos, button_radius * 0.95, button_radius * 0.95
                )
            else:
                painter.drawEllipse(pos, button_radius, button_radius)

            shadow_gradient = QRadialGradient(pos, button_radius * 0.8)
            shadow_gradient.setColorAt(0.0, QColor(0, 0, 0, 100))
            shadow_gradient.setColorAt(1.0, QColor(0, 0, 0, 0))

            painter.setBrush(QBrush(shadow_gradient))
            painter.drawEllipse(pos + QPointF(2, 2), button_radius, button_radius)

            painter.setPen(button_text_colors[label])
            painter.setFont(QFont("Segoe UI", 32, QFont.Bold))
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

            self.button_actions[label] = QRectF(
                pos.x() - button_radius,
                pos.y() - button_radius,
                2 * button_radius,
                2 * button_radius,
            )

            painter.setBrush(QBrush(button_outer_color))
            painter.setPen(Qt.NoPen)

    def mouseMoveEvent(self, event):
        pos = event.pos()

        if self.dpad_rect.contains(pos):
            self.setCursor(Qt.PointingHandCursor)
            self.mesh_color = QColor(200, 200, 200, 200)
        elif any(rect.contains(pos) for rect in self.joysticks_rects.values()):
            self.setCursor(Qt.PointingHandCursor)
            self.mesh_color = QColor(200, 200, 200, 200)
        elif any(rect.contains(pos) for rect in self.bumper_rects.values()):
            self.setCursor(Qt.PointingHandCursor)
            self.mesh_color = QColor(200, 200, 200, 200)
        elif any(rect.contains(pos) for rect in self.trigger_rects.values()):
            self.setCursor(Qt.PointingHandCursor)
            self.mesh_color = QColor(200, 200, 200, 200)
        elif any(rect.contains(pos) for rect in self.button_options.values()):
            self.setCursor(Qt.PointingHandCursor)
            self.mesh_color = QColor(200, 200, 200, 200)
        elif any(rect.contains(pos) for rect in self.button_actions.values()):
            self.setCursor(Qt.PointingHandCursor)
            self.mesh_color = QColor(200, 200, 200, 200)
        else:
            self.setCursor(Qt.ArrowCursor)

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        # Restaurar el color del mallado cuando el mouse salga del área del widget
        self.mesh_color = QColor(200, 200, 200, 50)
        self.update()  # Redibujar la interfaz para aplicar el color restaurado

    def mousePressEvent(self, event):
        pos = event.pos()
        # Verificar botones de acción
        for label, rect in self.button_actions.items():
            if rect.contains(pos):
                self.action_button_pressed = label
                self.update()
                break

        # Verificar botones de opción
        for icon, rect in self.button_options.items():
            if rect.contains(pos):
                self.option_button_pressed = icon
                self.update()
                break

        if self.dpad_rect.contains(event.pos()):
            center_x = self.dpad_rect.center().x()
            center_y = self.dpad_rect.center().y()
            if event.pos().y() < center_y - 20:
                self.dpad_button_pressed["up"] = True
                self.pressed_side = "up"
            elif event.pos().y() > center_y + 20:
                self.dpad_button_pressed["down"] = True
                self.pressed_side = "down"
            if event.pos().x() < center_x - 20:
                self.dpad_button_pressed["left"] = True
                self.pressed_side = "left"
            elif event.pos().x() > center_x + 20:
                self.dpad_button_pressed["right"] = True
                self.pressed_side = "right"
            self.update()

    def mouseReleaseEvent(self, event):
        self.action_button_pressed = None
        self.option_button_pressed = None
        if self.dpad_rect.contains(event.pos()):
            center_x = self.dpad_rect.center().x()
            center_y = self.dpad_rect.center().y()
            if event.pos().y() < center_y - 20:
                self.dpad_button_pressed["up"] = False
            elif event.pos().y() > center_y + 20:
                self.dpad_button_pressed["down"] = False
            if event.pos().x() < center_x - 20:
                self.dpad_button_pressed["left"] = False
            elif event.pos().x() > center_x + 20:
                self.dpad_button_pressed["right"] = False
            self.pressed_side = None
            self.update()
