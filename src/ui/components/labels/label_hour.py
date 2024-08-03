from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class LabelHour(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.installEventFilter(self)
        
    def style(self, text, color, size, font_family, alignment):
        self.setText(text)
        self.setStyleSheet(f"color: {color};")
        
        # Crear una fuente con el tamaño y familia especificados
        font = QFont()
        font.setPointSize(size)
        
        # Asegurarse de que font_family es una cadena
        if isinstance(font_family, QFont):
            font.setFamily(font_family.family())
        else:
            font.setFamily(font_family)
        
        self.setFont(font)
        self.setAlignment(alignment)
        self.setCursor(Qt.PointingHandCursor)
        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setWordWrap(True)