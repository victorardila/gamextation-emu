from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize


class ButtonIcon(QPushButton):
    def __init__(self, parent=QWidget | None):
        super().__init__(parent)
        self.installEventFilter(self)

    def style(self, icon, size, tooltip):
        self.setIcon(QIcon(icon))
        self.setIconSize(size)
        self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)
        self.setText("")
        self.setStyleSheet(
            """
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
        )

    # Métodos para darle hover al botón
    def eventFilter(self, obj, event):
        if event.type() == event.HoverEnter:
            self.setStyleSheet(
                """
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
                """)
        elif event.type() == event.HoverLeave:
            self.setStyleSheet(
                """
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
            )
        elif event.type() == event.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                pass
        return super().eventFilter(obj, event)

