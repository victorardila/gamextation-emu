from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QFont

class InputSearch(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Buscar")
        self.style()
        
    def style(self):
        # Crear un objeto QFont y establecer el tamaño de la fuente
        font = QFont()
        font.setPointSize(20)
        # Aplicar el objeto QFont al QLineEdit
        self.setFont(font)
        