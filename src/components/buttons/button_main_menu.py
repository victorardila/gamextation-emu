from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt

class ButtonMainMenu(QPushButton):
    def __init__(self, parent=QWidget | None):
        super().__init__(parent)
        self.installEventFilter(self)
        
    gradient_color = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(173, 216, 230, 255), stop:1 rgba(0, 255, 127, 255));"
    def style(self, image, size, tooltip):
        self.setImage(QImage(image))
        self.setImageSize(size)
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
                f"""
                QPushButton {{
                    border: none;
                    border-radius: 10px;
                    background: {self.gradient_color}; /* Usamos background en lugar de background-color */
                }}
                QToolTip {{
                    background-color: #333;
                    color: #fff;
                    border: 1px solid white;
                    padding: 5px;
                    border-radius: 5px;
                }}
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

