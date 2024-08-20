from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt


class GameLoaded(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        loadUi("src/ui/views/game/game_loaded.ui", self)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Añadir contenido primero
        self.add_widget_content()

        # Luego añadir sidebar encima
        self.add_widget_sidebar()

    def add_widget_sidebar(self):
        # Crear el sidebar y configurarlo para que tome toda la altura de la ventana
        self.sidebar = QWidget(self)
        self.sidebar.setFixedWidth(300)
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.sidebar.setStyleSheet("background-color: rgba(30, 250, 30, 0.8);")

        # Colocar el sidebar en la posición correcta y asegurarlo en la capa superior
        self.sidebar.setGeometry(0, 0, 300, self.height())
        self.sidebar.raise_()  # Asegura que el sidebar esté encima del content

        self.sidebar.show()

    def add_widget_content(self):
        # Crear el content para que ocupe todo el espacio restante
        self.content = QWidget(self)
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content.setStyleSheet("background-color: #2e2e2e;")

        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Asegurar que el content cubra toda la ventana
        self.content.setGeometry(0, 0, self.width(), self.height())
        self.content.show()

    def resizeEvent(self, event):
        # Redimensionar el sidebar y el content cuando se cambie el tamaño de la ventana
        self.sidebar.setGeometry(0, 0, 300, self.height())
        self.content.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)
