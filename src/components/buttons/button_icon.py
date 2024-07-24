from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from qtawesome import icon

class ButtonIcon(QPushButton):
    def __init__(self, parent=QWidget | None):
        super().__init__(parent)
        self.installEventFilter(self)
        self.setCursor(Qt.PointingHandCursor)
        
    def style(self, icon_name, size, tooltip, color='white'):
        self.setIcon(QIcon(icon(icon_name, color=color)))
        self.setIconSize(size)
        self.setToolTip(tooltip)
        self.setText("")
        self.setStyleSheet(self.default_stylesheet())

    def default_stylesheet(self):
        return """
            QPushButton {
                border: none;
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 0);
            }
            QToolTip {
                background-color: #333;
                color: #fff;
                border: 0.5px solid white;
                padding: 5px;
                border-radius: 5px;
            }
        """
    
    def hover_enter_stylesheet(self):
        return """
            QPushButton {
                border: none;
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 0.2);
            }
            QToolTip {
                background-color: #333;
                color: #fff;
                border: 1px solid white;
                padding: 5px;
                border-radius: 5px;
            }
        """

    def hover_leave_stylesheet(self):
        return """
            QPushButton {
                border: none;
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 0);
            }
            QToolTip {
                background-color: #333;
                color: #fff;
                border: 0.5px solid white;
                padding: 5px;
                border-radius: 5px;
            }
        """
    
    def eventFilter(self, obj, event):
        if event.type() == event.HoverEnter:
            self.setStyleSheet(self.hover_enter_stylesheet())
        elif event.type() == event.HoverLeave:
            self.setStyleSheet(self.hover_leave_stylesheet())
        elif event.type() == event.MouseButtonPress and event.button() == Qt.LeftButton:
            pass
        return super().eventFilter(obj, event)