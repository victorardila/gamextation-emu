from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

class ButtonIcon(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFlat(True)
        self.setStyleSheet("background-color: transparent;")
        self.setText("")
        self._hoverIcon = None
        self._defaultIcon = None
    
    def setMaximumWidth(self, width):
        self.setMaximumWidth(width)
    
    def setMaximumHeight(self, height):
        self.setMaximumHeight(height)
    
    def setIcon(self, icon):
        self._defaultIcon = QIcon(icon)
        super().setIcon(self._defaultIcon)
        self.setIconSize(QSize(32, 32))

    def setIconHover(self, icon):
        self._hoverIcon = QIcon(icon)

    def enterEvent(self, event):
        if self._hoverIcon:
            super().setIcon(self._hoverIcon)

    def leaveEvent(self, event):
        if self._defaultIcon:
            super().setIcon(self._defaultIcon)