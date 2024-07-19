from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class LabelHour(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.installEventFilter(self)
        
    def style(self, text, color, size, font, alignment):
        self.setText(text)
        self.setStyleSheet(f"color: {color};")
        self.setFont(font)
        self.setAlignment(alignment)
        self.setCursor(Qt.PointingHandCursor)
        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setWordWrap(True)