from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QApplication
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QColor
import math

class OctagonButton(QPushButton):
    def __init__(self, label, parent=None):
        super().__init__(label, parent)
        self.setFixedSize(100, 100)  # Ajusta el tamaño del botón si es necesario
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Definir el área de dibujo
        rect = QRectF(0, 0, self.width(), self.height())
        
        # Crear el camino en forma de octágono
        path = QPainterPath()

        # El octágono regular tiene 8 vértices igualmente espaciados
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

        # Dibujar el botón con un fondo y un borde
        painter.fillPath(path, QBrush(QColor(255, 255, 255, 180)))
        painter.setPen(QColor(255, 255, 255))
        painter.drawPath(path)

        # Dibujar el texto centrado
        painter.drawText(rect, Qt.AlignCenter, self.text())
class KeyboardInteractive(QWidget):
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
    
    def get_keyboard_layout(self):
        """Define y devuelve la disposición de las teclas del teclado."""
        return [
            ['', '', '🔉', '🔇'],
            ['Esc', '', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'PrtSc', 'Delete'],
            ['°|¬', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
            ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
            ['CapsLock', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', 'Enter'],
            ['Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift'],
            ['Ctrl', 'Fn', 'Alt', 'Inicio', 'Space', 'Alt Gr', 'Ctrl', '←', '↑', '↓', '→']
        ]
    
    def create_buttons(self, layout, keys):
        """Crea y añade los botones al layout según la disposición de teclas."""
        custom_styles = self.get_custom_styles()  # Obtener los estilos personalizados
        for row, key_row in enumerate(keys):
            col_offset = 0
            for key in key_row:
                # Ignorar los espacios vacíos representados por ''
                if key == '':
                    col_offset += 1  # Simplemente avanza a la siguiente columna
                    continue
                
                # Configurar el tamaño de la tecla "Space" para que sea más ancha
                if key == 'Space':
                    button = self.create_button(key, width=250, style=custom_styles.get(key))
                    layout.addWidget(button, row, col_offset, 1, 4)  # Ocupa 4 columnas
                    col_offset += 4  # Avanzar el offset de columna
                else:
                    button = self.create_button(key, style=custom_styles.get(key))
                    layout.addWidget(button, row, col_offset)
                    col_offset += 1  # Avanzar a la siguiente columna

    def create_button(self, key, width=60, height=60, style=None):
        """Crea y devuelve un botón con el estilo configurado."""
        button = OctagonButton(key) if key != 'Space' else QPushButton(key)
        button.setFixedSize(width, height)
        
        if style:
            button.setStyleSheet(style)
        else:
            button.setStyleSheet(self.get_button_style())
        
        return button
    
    def get_custom_styles(self):
        """Devuelve un diccionario con estilos personalizados para teclas específicas."""
        return {
            'Shift': """
                QPushButton {
                    background-color: rgba(100, 100, 255, 255);
                    border: 2px solid white;
                    border-radius: 5px;
                    font-size: 14px;
                    color: white;
                }
                QPushButton:pressed {
                    background-color: rgba(50, 50, 255, 255);
                }
            """,
            'Esc': """
                QPushButton {
                    background-color: rgba(100, 100, 255, 255);
                    border: 2px solid white;
                    border-radius: 5px;
                    font-size: 14px;
                    color: white;
                }
                QPushButton:pressed {
                    background-color: rgba(50, 50, 255, 255);
                }
            """,
            'Space': """
                QPushButton {
                    background-color: rgba(200, 200, 200, 255);
                    border: 2px solid white;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:pressed {
                    background-color: rgba(150, 150, 150, 255);
                }
            """,
            # Puedes agregar más estilos personalizados aquí para otras teclas
        }

    def get_button_style(self):
        """Devuelve la hoja de estilo para los botones."""
        return """
            QPushButton {
                background-color: rgba(255, 255, 255, 200);
                border: 2px solid white;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:pressed {
                background-color: rgba(200, 200, 200, 100);
            }
        """