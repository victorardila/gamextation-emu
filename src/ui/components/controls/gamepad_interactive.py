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
        # Configuración inicial de la ventana
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(600, 400)
        self.setMouseTracking(True)

        # Inicialización de rectángulos y colores
        self.dpad_rect = QRectF()
        self.button_options = {}
        self.button_actions = {}
        self.joysticks_rects = {side: QRectF() for side in ["left", "right"]}
        self.bumper_rects = {side: QRectF() for side in ["left", "right"]}
        self.trigger_rects = {side: QRectF() for side in ["left", "right"]}
        self.mesh_color = QColor(200, 200, 200, 50)  # Color por defecto

        # Inicialización de estados de botones y controles
        self.action_button_pressed = None
        self.option_button_pressed = None
        self.pressed_side = None
        self.dpad_button_pressed = {
            direction: False for direction in ["up", "down", "left", "right"]
        }
        self.bumper_pressed = {side: False for side in ["left", "right"]}
        self.trigger_pressed = {side: False for side in ["left", "right"]}

        self.left_offset = QPointF()
        self.right_offset = QPointF()
        self.active_joystick = None  # Para rastrear cuál joystick está siendo movido

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
        self.drawJoysticks(painter, path, self.left_offset, self.right_offset)
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

    def drawJoysticks(self, painter, path, left_offset, right_offset):
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
        for pos_key, pos in joystick_positions.items():
            # Dibujar el joystick exterior
            painter.drawEllipse(pos, joystick_radius, joystick_radius)

            # Offset para el movimiento del joystick interior
            offset = left_offset if pos_key == "left" else right_offset

            # Limitar el movimiento del joystick interior dentro del joystick exterior
            distance = min(
                (offset.x() ** 2 + offset.y() ** 2) ** 0.5,
                joystick_radius - inner_radius,
            )
            angle = math.atan2(offset.y(), offset.x())
            adjusted_offset = QPointF(
                distance * math.cos(angle), distance * math.sin(angle)
            )

            # Posición ajustada del joystick interior
            inner_pos = pos + adjusted_offset

            # Configurar el pincel y el color para el joystick interior
            # Crear un degradado radial para simular el alto relieve
            gradient = QRadialGradient(inner_pos, inner_radius)
            gradient.setColorAt(0.0, QColor(50, 50, 50))  # Centro más oscuro
            gradient.setColorAt(0.8, QColor(30, 30, 30))  # Borde más claro

            # Aplicar el degradado al pincel
            painter.setBrush(QBrush(gradient))

            # Dibujar el joystick interior con alto relieve
            painter.drawEllipse(inner_pos, inner_radius, inner_radius)

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
                        inner_pos.x() - cup_radius,
                        inner_pos.y() - cup_radius,
                        2 * cup_radius,
                        2 * cup_radius,
                    ),
                    start_angle,
                    arc_span_angle,
                )

            # Restaurar el pincel al color anterior para el joystick exterior
            painter.setBrush(QBrush(outer_color))
            painter.setPen(Qt.NoPen)

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
        shadow_color = QColor(20, 20, 20)  # Color para la sombra

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

        # Dibuja la cruz del D-Pad
        def draw_cross(painter, side_pressed):
            painter.setBrush(QBrush(cross_color))
            painter.setPen(Qt.NoPen)

            # Dibuja la sombra en función del lado presionado
            if side_pressed in ["up", "down"]:
                painter.setBrush(QBrush(shadow_color))
                if side_pressed == "up":
                    painter.drawRect(
                        int(center_x - cross_thickness / 2),
                        int(center_y - cross_radius),
                        int(cross_thickness),
                        int(cross_radius),
                    )
                elif side_pressed == "down":
                    painter.drawRect(
                        int(center_x - cross_thickness / 2),
                        int(center_y),
                        int(cross_thickness),
                        int(cross_radius),
                    )
            elif side_pressed in ["left", "right"]:
                painter.setBrush(QBrush(shadow_color))
                if side_pressed == "left":
                    painter.drawRect(
                        int(center_x - cross_radius),
                        int(center_y - cross_thickness / 2),
                        int(cross_radius),
                        int(cross_thickness),
                    )
                elif side_pressed == "right":
                    painter.drawRect(
                        int(center_x),
                        int(center_y - cross_thickness / 2),
                        int(cross_radius),
                        int(cross_thickness),
                    )

            # Dibuja la cruz principal
            painter.setBrush(QBrush(cross_color))
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

            # Resalta el lado presionado
            if side_pressed:
                painter.setBrush(QBrush(pressed_color))
                if side_pressed == "up":
                    painter.drawRect(
                        int(center_x - cross_thickness / 2),
                        int(center_y - cross_radius),
                        int(cross_thickness),
                        int(cross_radius),
                    )
                elif side_pressed == "down":
                    painter.drawRect(
                        int(center_x - cross_thickness / 2),
                        int(center_y),
                        int(cross_thickness),
                        int(cross_radius),
                    )
                elif side_pressed == "left":
                    painter.drawRect(
                        int(center_x - cross_radius),
                        int(center_y - cross_thickness / 2),
                        int(cross_radius),
                        int(cross_thickness),
                    )
                elif side_pressed == "right":
                    painter.drawRect(
                        int(center_x),
                        int(center_y - cross_thickness / 2),
                        int(cross_radius),
                        int(cross_thickness),
                    )

        draw_cross(painter, self.pressed_side)

        icon_up = qta.icon("fa.caret-up", color="gray")
        icon_down = qta.icon("fa.caret-down", color="gray")
        icon_left = qta.icon("fa.caret-left", color="gray")
        icon_right = qta.icon("fa.caret-right", color="gray")

        icon_size = QSize(24, 24)

        def create_highlighted_pixmap(icon, highlight):
            pixmap = icon.pixmap(icon_size)
            painter_icon = QPainter(pixmap)
            if highlight:
                painter_icon.setBrush(QBrush(highlight_color))
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
        normal_color = QColor(50, 50, 50)  # Color para los bumpers normales
        pressed_color = QColor(100, 100, 100)  # Color para los bumpers presionados
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

        # Dibujar el bumper izquierdo con su estado correspondiente
        painter.setPen(QPen(border_color, border_width))
        painter.setBrush(
            QBrush(pressed_color if self.bumper_pressed["left"] else normal_color)
        )
        painter.drawRoundedRect(left_bumper_rect, 10, 10)

        # Dibujar el bumper derecho con su estado correspondiente
        painter.setBrush(
            QBrush(pressed_color if self.bumper_pressed["right"] else normal_color)
        )
        painter.drawRoundedRect(right_bumper_rect, 10, 10)

        # Configurar el estilo del texto para los labels
        font = QFont("Arial", 12, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))

        # Calcular el texto a dibujar en los bumpers
        left_bumper_text = "L1"
        right_bumper_text = "R1"

        # Calcular el rectángulo del texto para centrarlo en el bumper
        left_bumper_text_rect = left_bumper_rect.adjusted(0, 0, 0, -5)
        right_bumper_text_rect = right_bumper_rect.adjusted(0, 0, 0, -5)

        # Dibujar los labels en los bumpers
        painter.drawText(left_bumper_text_rect, Qt.AlignCenter, left_bumper_text)
        painter.drawText(right_bumper_text_rect, Qt.AlignCenter, right_bumper_text)

        # Definir las áreas de los bumpers
        self.bumper_rects["left"] = left_bumper_rect
        self.bumper_rects["right"] = right_bumper_rect

    def drawTriggers(self, painter, path):
        # Colores de los triggers
        normal_color = QColor(70, 70, 70)
        pressed_color = QColor(100, 100, 100)  # Color más claro para indicar presión
        border_color = QColor(30, 30, 30)
        border_width = 1

        # Obtener el rectángulo delimitador del mando
        bounding_rect = path.boundingRect()
        center_x = bounding_rect.center().x()
        top_y = bounding_rect.top() - 15

        # Definir tamaños y posiciones de los triggers
        trigger_width = 60
        trigger_height = 40

        # Posiciones ajustadas de los triggers
        left_trigger_rect = QRectF(center_x - 210, top_y, trigger_width, trigger_height)
        right_trigger_rect = QRectF(
            center_x + 170, top_y, trigger_width, trigger_height
        )

        # Definir la inclinación del triángulo
        angle = 30

        def create_triangle(rect, angle):
            radians = math.radians(angle)
            points = [
                QPointF(rect.center().x(), rect.top()),
                QPointF(rect.left(), rect.bottom()),
                QPointF(rect.right(), rect.bottom()),
            ]
            matrix = QTransform()
            matrix.translate(rect.center().x(), rect.center().y())
            matrix.rotate(angle)
            matrix.translate(-rect.center().x(), -rect.center().y())

            rotated_points = [matrix.map(p) for p in points]
            return QPolygonF(rotated_points)

        # Crear triángulos para los triggers
        left_trigger_triangle = create_triangle(left_trigger_rect, angle)
        right_trigger_triangle = create_triangle(right_trigger_rect, angle)

        # Configurar el lápiz para el borde de los triggers
        painter.setPen(QPen(border_color, border_width))

        # Dibujar el trigger izquierdo con su estado correspondiente
        painter.setBrush(
            QBrush(pressed_color if self.trigger_pressed["left"] else normal_color)
        )
        painter.drawPolygon(left_trigger_triangle)

        # Dibujar el trigger derecho con su estado correspondiente
        painter.setBrush(
            QBrush(pressed_color if self.trigger_pressed["right"] else normal_color)
        )
        painter.drawPolygon(right_trigger_triangle)

        # Configurar el estilo del texto para los labels
        font = QFont("Arial", 12, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))

        # Calcular el texto a dibujar en los triggers
        left_trigger_text = "L2"
        right_trigger_text = "R2"

        def center_text_in_triangle(triangle, text):
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

        # Definir las áreas de los triggers
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
        hover_areas = [
            self.dpad_rect,
            *self.joysticks_rects.values(),
            *self.bumper_rects.values(),
            *self.trigger_rects.values(),
            *self.button_options.values(),
            *self.button_actions.values(),
        ]

        if any(rect.contains(pos) for rect in hover_areas):
            self.setCursor(Qt.PointingHandCursor)
            self.mesh_color = QColor(200, 200, 200, 200)
        else:
            self.setCursor(Qt.ArrowCursor)

        if self.active_joystick:
            joystick_rect = self.joysticks_rects[self.active_joystick]
            offset_attr = f"{self.active_joystick}_offset"
            setattr(self, offset_attr, event.pos() - joystick_rect.center())

        self.update()

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.mesh_color = QColor(200, 200, 200, 50)
        self.update()

    def mousePressEvent(self, event):
        pos = event.pos()

        for label, rect in {**self.button_actions, **self.button_options}.items():
            if rect.contains(pos):
                if label in self.button_actions:
                    self.action_button_pressed = label
                else:
                    self.option_button_pressed = label
                self.update()
                return

        if self.dpad_rect.contains(pos):
            dx, dy = (
                pos.x() - self.dpad_rect.center().x(),
                pos.y() - self.dpad_rect.center().y(),
            )
            if abs(dy) > 20:
                self.pressed_side = "up" if dy < 0 else "down"
            elif abs(dx) > 20:
                self.pressed_side = "left" if dx < 0 else "right"
            if self.pressed_side:
                self.dpad_button_pressed[self.pressed_side] = True
                self.update()
                return

        for side in ["left", "right"]:
            if self.bumper_rects[side].contains(pos):
                self.bumper_pressed[side] = True
                self.bumper_pressed[["left", "right"][side == "left"]] = False
                self.update()
                return
            if self.trigger_rects[side].contains(pos):
                self.trigger_pressed[side] = True
                self.trigger_pressed[["left", "right"][side == "left"]] = False
                self.update()
                return

        if self.joysticks_rects["left"].contains(pos):
            self.active_joystick = "left"
        elif self.joysticks_rects["right"].contains(pos):
            self.active_joystick = "right"

        self.update()

    def mouseReleaseEvent(self, event):
        self.action_button_pressed = None
        self.option_button_pressed = None
        event_pos = event.pos()

        if self.dpad_rect.contains(event_pos):
            dx, dy = (
                event_pos.x() - self.dpad_rect.center().x(),
                event_pos.y() - self.dpad_rect.center().y(),
            )

            if abs(dy) > 20:
                self.dpad_button_pressed["up" if dy < 0 else "down"] = False
            if abs(dx) > 20:
                self.dpad_button_pressed["left" if dx < 0 else "right"] = False

            self.pressed_side = None
            self.dpad_button_pressed = {key: False for key in self.dpad_button_pressed}

        for side in ["left", "right"]:
            if any(
                rect.contains(event_pos)
                for rect in [self.bumper_rects[side], self.trigger_rects[side]]
            ):
                self.bumper_pressed[side] = False
                self.trigger_pressed[side] = False

        # Restaurar las posiciones de los joysticks a su posición central
        self.left_offset = QPointF(0, 0)
        self.right_offset = QPointF(0, 0)
        self.active_joystick = None

        self.update()
