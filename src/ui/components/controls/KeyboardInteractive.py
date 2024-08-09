from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QApplication
from PyQt5.QtCore import Qt
import sys

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
            ['Esc', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'PrtSc', 'Delete'],
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
            ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
            ['CapsLock', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', 'Enter'],
            ['Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift'],
            ['Ctrl', 'Fn', 'Alt', 'Inicio', 'Space', 'Alt Gr', 'Ctrl', '←', '↑', '↓', '→']
        ]
    
    def create_buttons(self, layout, keys):
        """Crea y añade los botones al layout según la disposición de teclas."""
        for row, key_row in enumerate(keys):
            col_offset = 0
            for key in key_row:
                # Configurar el tamaño de la tecla "Space" para que sea cinco veces más ancha
                if key == 'Space':
                    button = self.create_button(key, width=250)
                    layout.addWidget(button, row, col_offset, 1, 4)  # Ocupa 5 columnas
                    col_offset += 4  # Avanzar el offset de columna
                else:
                    button = self.create_button(key)
                    layout.addWidget(button, row, col_offset)
                    col_offset += 1  # Avanzar a la siguiente columna
    
    def create_button(self, key, width=50, height=50):
        """Crea y devuelve un botón con el estilo configurado."""
        button = QPushButton(key)
        button.setFixedSize(width, height)
        button.setStyleSheet(self.get_button_style())
        return button
    
    def get_button_style(self):
        """Devuelve la hoja de estilo para los botones."""
        return """
            QPushButton {
                background-color: rgba(255, 255, 255, 255);
                border: 2px solid white;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:pressed {
                background-color: rgba(200, 200, 200, 255);
            }
        """