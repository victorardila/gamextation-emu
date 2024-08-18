from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QMovie
from qtawesome import icon
import os


class ButtonIcon(QPushButton):
    def __init__(self, parent=QWidget | None):
        super().__init__(parent)
        self.installEventFilter(self)
        self.setCursor(Qt.PointingHandCursor)
        self.movie = None  # Mantener una referencia a QMovie

    def style(self, icon_name, size, tooltip, color="white", gif_speed=800):
        if self._is_image_path(icon_name):
            if icon_name.lower().endswith(".gif"):
                self._set_gif(icon_name, size, gif_speed)
            else:
                self._set_static_image(icon_name, size)
        else:
            self.setIcon(QIcon(icon(icon_name, color=color)))

        self.setIconSize(size)
        self.setToolTip(tooltip)
        self.setText("")
        self.setStyleSheet(self.default_stylesheet())

    def _set_static_image(self, path, size):
        pixmap = QPixmap(path).scaled(size)
        self.setIcon(QIcon(pixmap))

    def _set_gif(self, path, size, speed):
        self.movie = QMovie(path)
        self.movie.setScaledSize(size)
        self.movie.setSpeed(speed)  # Ajustar la velocidad del GIF
        self.movie.frameChanged.connect(self._update_icon_from_movie)
        self.movie.start()

    def _update_icon_from_movie(self):
        self.setIcon(QIcon(self.movie.currentPixmap()))

    def _is_image_path(self, path):
        return os.path.isfile(path) and path.lower().endswith(
            (".png", ".jpg", ".jpeg", ".gif")
        )

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
