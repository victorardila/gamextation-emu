from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QLabel, QFrame
from PyQt5.uic import loadUi
from datetime import datetime
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt5.QtGui import QFont, QFontDatabase


class GameLoaded(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

        # Variables para controlar el estado del sidebar
        self.sidebar_expanded = False
        self.sidebar_width = 300
        self.collapse_threshold = 300

        # Crear un temporizador para verificar la posición del mouse periódicamente
        self.mouse_timer = QTimer(self)
        self.mouse_timer.timeout.connect(self.check_mouse_position)
        self.mouse_timer.start(50)  # Verifica la posición del mouse cada 50 ms

    def setup_ui(self):
        loadUi("src/ui/views/game/game_loaded.ui", self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.custom_font = self._load_custom_font(
            "src/assets/font/ratchet-clank-psp.ttf", 24, "Arial", 18
        )

        # Añadir contenido primero
        self.add_widget_content()

        # Luego añadir sidebar encima
        self.add_widget_sidebar()

    def design_sidebar(self):
        # Crear un layout vertical para el sidebar
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)

        self.sidebar_logo = QFrame(self.sidebar)
        self.sidebar_logo.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.sidebar_logo.setFixedHeight(200)
        self.sidebar_logo.setStyleSheet("background-color: transparent;")
        self.sidebar_layout.addWidget(self.sidebar_logo)

        self.logo_menu_content = QFrame(self.sidebar_logo)
        self.logo_menu_content.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred
        )
        self.logo_menu_content.setStyleSheet("background-color: transparent;")
        self.logo_menu_content_layout = QVBoxLayout(self.logo_menu_content)
        self.logo_menu_content_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_menu_content_layout.setSpacing(
            10
        )  # Ajusta el espacio entre los widgets si es necesario

        self.sidebar_logo_layout = QVBoxLayout(self.sidebar_logo)
        self.sidebar_logo_layout.addWidget(self.logo_menu_content)

        self.label_logo = QLabel(self.sidebar_logo)
        self.label_logo.setPixmap("src/assets/images/logo.png")

        self.label_title = QLabel("Menu de opciones", self.logo_menu_content)
        self.label_title.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet("color: white; font-size: 28px;")
        self.label_title.setFont(QFont(self.custom_font))
        self.sidebar_logo.addWidget(self.label_title)

        self.label_hour = QLabel("00:00:00 AM", self.logo_menu_content)
        self.label_hour.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.label_hour.setAlignment(Qt.AlignCenter)
        self.label_hour.setStyleSheet("color: white; font-size: 25px;")
        self.label_hour.setFont(QFont(self.custom_font))
        self.logo_menu_content_layout.addWidget(self.label_hour)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_time)
        self.timer.start(1000)

        self._update_time()

        self.sidebar_content = QFrame(self.sidebar)
        self.sidebar_content.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.sidebar_content.setStyleSheet("background-color: transparent;")
        self.sidebar_layout.addWidget(self.sidebar_content)

    def _update_time(self):
        current_time = datetime.now().strftime("%I:%M:%S %p")
        self.label_hour.setText(current_time)

    def _load_custom_font(self, font_path, font_size, fallback_font, fallback_size):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            return QFont(font_family, font_size)
        return QFont(fallback_font, fallback_size)

    def add_widget_sidebar(self):
        # Crear el sidebar y configurarlo para que tome toda la altura de la ventana
        self.sidebar = QWidget(self)
        self.sidebar.setFixedWidth(0)  # Inicialmente el sidebar está cerrado
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.sidebar.setStyleSheet("background-color: rgba(30, 30, 30, 0.5);")

        # Colocar el sidebar en la posición correcta y asegurarlo en la capa superior
        self.sidebar.setGeometry(0, 0, 0, self.height())
        self.sidebar.raise_()  # Asegura que el sidebar esté encima del content

        # Conectar eventos de entrada y salida del mouse
        self.sidebar.enterEvent = self.on_mouse_enter_sidebar
        self.sidebar.leaveEvent = self.on_mouse_leave_sidebar

        # Diseñar el contenido del sidebar
        self.design_sidebar()

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

        # Crear un label que se mostrará en el centro del content
        label = QLabel("Loaded game🎮", self.content)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white; font-size: 20px;")
        content_layout.addWidget(label)

        self.content.show()

    def resizeEvent(self, event):
        # Redimensionar el sidebar y el content cuando se cambie el tamaño de la ventana
        self.sidebar.setGeometry(0, 0, self.sidebar.width(), self.height())
        self.content.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def check_mouse_position(self):
        # Obtener la posición del mouse globalmente
        global_mouse_pos = self.mapFromGlobal(self.cursor().pos())

        if global_mouse_pos.x() <= 10 and not self.sidebar_expanded:
            self.expand_sidebar()
        elif global_mouse_pos.x() > self.collapse_threshold and self.sidebar_expanded:
            self.collapse_sidebar()

    def expand_sidebar(self):
        # Crear una animación para expandir el sidebar a 300px de ancho
        self.animation = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.animation.setDuration(300)  # Duración de la animación en milisegundos
        self.animation.setStartValue(0)
        self.animation.setEndValue(self.sidebar_width)
        self.animation.finished.connect(
            lambda: self.sidebar.setFixedWidth(self.sidebar_width)
        )
        self.animation.start()

        # Actualizar el estado del sidebar después de la animación
        self.sidebar_expanded = True

    def collapse_sidebar(self):
        # Crear una animación para colapsar el sidebar a 0px de ancho
        self.animation = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.animation.setDuration(300)  # Duración de la animación en milisegundos
        self.animation.setStartValue(self.sidebar.width())
        self.animation.setEndValue(0)
        self.animation.finished.connect(lambda: self.sidebar.setFixedWidth(0))
        self.animation.start()

        # Actualizar el estado del sidebar después de la animación
        self.sidebar_expanded = False

    def on_mouse_enter_sidebar(self, event):
        # Cambiar el cursor a una mano cuando el mouse entra en el sidebar
        self.sidebar.setCursor(Qt.PointingHandCursor)

    def on_mouse_leave_sidebar(self, event):
        # Restablecer el cursor al estado predeterminado cuando el mouse sale del sidebar
        self.sidebar.setCursor(Qt.ArrowCursor)
