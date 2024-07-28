from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt

class InputSearch(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.style()
        
    def style(self):
        # Estilo del QLineEdit
        self.setStyleSheet("""
            QLineEdit {
                color: white;
                font-size: 20px; /* Tamaño de la letra al escribir dentro del QLineEdit */
            }
            QLineEdit::placeholder {
                color: white;
                font-size: 20px; /* Tamaño de la letra del placeholder */
            }
        """)
        # Placeholder
        self.setPlaceholderText("Buscar")
        