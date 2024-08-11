from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QColor, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtCore import pyqtSignal
import math

class OctagonButton(QPushButton):
    hovered_signal = pyqtSignal(str)  # Señal que emitirá el texto del botón cuando se hace hover

    def __init__(self, label, parent=None):
        super().__init__(label, parent)
        self.setFixedSize(100, 100)
        self.hovered = False
        self.custom_font = QFont()  # Inicializa la fuente personalizada aquí
        
    def load_custom_font(self, font_path, font_size, fallback_font, fallback_size):
        """Carga una fuente personalizada o usa una fuente de reserva."""
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            return QFont(font_family, font_size)
        return QFont(fallback_font, fallback_size)

    def enterEvent(self, event):
        """Cambia el estado a hover cuando el mouse entra."""
        self.hovered = True
        self.hovered_signal.emit(self.text())  # Emitir señal con el texto del botón
        self.update()

    def leaveEvent(self, event):
        """Cambia el estado a no hover cuando el mouse sale."""
        self.hovered = False
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Definir el área de dibujo
        rect = QRectF(0, 0, self.width(), self.height())

        # Crear el camino en forma de octágono
        path = QPainterPath()

        radius = min(rect.width(), rect.height()) / 2.0
        center = QPointF(rect.center().x(), rect.center().y())

        for i in range(8):
            angle_deg = 45 * i
            angle_rad = math.radians(angle_deg)
            x = center.x() + radius * math.cos(angle_rad)
            y = center.y() + radius * math.sin(angle_rad)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)

        path.closeSubpath()  # Cierra la figura

        # Definir el color de fondo basado en el estado del botón
        if self.isDown():
            background_color = QColor(200, 200, 200, 100)  # Color cuando el botón está presionado
        elif self.hovered:
            background_color = QColor(255, 255, 255, 150)  # Color cuando el botón está en hover
        else:
            background_color = QColor(255, 255, 255, 180)  # Color normal

        # Dibujar el botón con el color de fondo y un borde
        painter.fillPath(path, QBrush(background_color))
        painter.setPen(QColor(255, 255, 255))
        painter.drawPath(path)

        # Configurar el texto en negrita
        font = self.font()
        font.setBold(True)  # Establecer la fuente en negrita (bold)
        painter.setFont(self.custom_font)

        # Dibujar el texto centrado
        painter.setPen(QColor(0, 0, 0))  # Texto en color negro
        painter.drawText(rect, Qt.AlignCenter, self.text())
        
class RectangularButton(QPushButton):
    hovered_signal = pyqtSignal(str)  # Señal que emitirá el texto del botón cuando se hace hover

    def __init__(self, label, parent=None):
        super().__init__(label, parent)
        self.setFixedSize(100, 60)
        self.hovered = False
        self.custom_font = QFont()  # Inicializa la fuente personalizada aquí
        
    def load_custom_font(self, font_path, font_size, fallback_font, fallback_size):
        """Carga una fuente personalizada o usa una fuente de reserva."""
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            return QFont(font_family, font_size)
        return QFont(fallback_font, fallback_size)

    def enterEvent(self, event):
        """Cambia el estado a hover cuando el mouse entra."""
        self.hovered = True
        self.hovered_signal.emit(self.text())  # Emitir señal con el texto del botón
        self.update()

    def leaveEvent(self, event):
        """Cambia el estado a no hover cuando el mouse sale."""
        self.hovered = False
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Definir el área de dibujo
        rect = QRectF(0, 0, self.width(), self.height())

        # Crear el camino en forma de rectángulo
        path = QPainterPath()
        path.addRect(rect)

        path.closeSubpath()  # Cierra la figura

        # Definir el color de fondo basado en el estado del botón
        if self.isDown():
            background_color = QColor(200, 200, 200, 100)  # Color cuando el botón está presionado
        elif self.hovered:
            background_color = QColor(255, 255, 255, 150)  # Color cuando el botón está en hover
        else:
            background_color = QColor(255, 255, 255, 180)  # Color normal

        # Dibujar el botón con el color de fondo y un borde
        painter.fillPath(path, QBrush(background_color))
        painter.setPen(QColor(255, 255, 255))
        painter.drawPath(path)

        # Configurar el texto en negrita
        font = self.font()
        font.setBold(True)  # Establecer la fuente en negrita (bold)
        painter.setFont(self.custom_font)

        # Dibujar el texto centrado
        painter.setPen(QColor(0, 0, 0))  # Texto en color negro
        painter.drawText(rect, Qt.AlignCenter, self.text())
        
class KeyboardInteractive(QWidget):
    hovered_signal = pyqtSignal(str)  # Señal que emitirá el texto del botón cuando se hace hover
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setupUi()
        
    def setupUi(self):
        # Configurar la ventana principal del teclado
        self.configure_window()
        
        # Crear el layout de la cuadrícula para el teclado
        layout = QGridLayout(self)
        layout.setSpacing(5)
        
        # Definir las filas de teclas del teclado
        keys = self.get_keyboard_layout()
        
        # Crear y añadir botones al layout
        self.create_buttons(layout, keys)
        
        self.setLayout(layout)
        self.adjustSize()
    
    def configure_window(self):
        """Configura la ventana para ser transparente y sin borde."""
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
    
    def load_custom_font(self, font_path, font_size, fallback_font, fallback_size):
        """Carga una fuente personalizada o usa una fuente de reserva."""
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            return QFont(font_family, font_size)
        return QFont(fallback_font, fallback_size)
    
    def get_keyboard_layout(self):
        """Define y devuelve la disposición de las teclas del teclado."""
        return [
            ['', '', '🔉', '🔇', '🎙️', '⚙️'],
            ['Esc', '', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'PrtSc', 'Delete'],
            ['°|¬', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
            ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
            ['Bloq Mayús', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', 'Enter'],
            ['Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift'],
            ['Ctrl', 'Fn', 'Alt', 'Inicio', '────────────', 'Alt Gr', 'Ctrl', '←', '↑', '↓', '→']
        ]
    
    def create_buttons(self, layout, keys):
        """Crea y añade los botones al layout según la disposición de teclas."""
        for row, key_row in enumerate(keys):
            col_offset = 0
            for key in key_row:
                # Ignorar los espacios vacíos representados por ''
                if key == '':
                    col_offset += 1  # Simplemente avanza a la siguiente columna
                    continue
                
                # Configurar el tamaño de la tecla "Space" para que sea más ancha
                if key == '────────────':
                    button = self.create_button(key, width=310)
                    layout.addWidget(button, row, col_offset, 1, 5)  # Ocupa 4 columnas
                    col_offset += 4  # Avanzar el offset de columna
                else:
                    button = self.create_button(key)
                    layout.addWidget(button, row, col_offset)
                    col_offset += 1  # Avanzar a la siguiente columna

    def create_button(self, key, width=60, height=60, style=None):
        """Crea y devuelve un botón con el estilo configurado."""
        button = OctagonButton(key, self) if key != '────────────' else RectangularButton(key, self)
        button.setFixedSize(width, height)
        button.load_custom_font("src/assets/font/ratchet-clank-psp.ttf", 20, "Arial", 18)  # Configura la fuente personalizada aquí
        return button