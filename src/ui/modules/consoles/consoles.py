from src.ui.components.cover.cover_console import CoverConsole
from src.ui.components.controls.keyboard_interactive import KeyboardInteractive
from src.ui.components.controls.keyboard_interactive import OctagonButton
from PyQt5.QtCore import QSize, pyqtSignal, QTimer, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QFont, QFontDatabase
# from src.ui.components.cover.cover_console import CoverConsole
from PyQt5.uic import loadUi

class Consoles(QWidget):
    optimizer_hidden = pyqtSignal()
    back_clicked = pyqtSignal()
    
    # arreglo de imagenes gif de consolas
    GIFS_CONSOLES = [
        "src/assets/gif/console.gif",
        "src/assets/gif/console2.gif",
        "src/assets/gif/console3.gif",
    ]
    
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.optimizer_hidden.connect(self.handle_optimizer_hidden)
        
    def setupUi(self):
        loadUi("src/ui/modules/consoles/consoles.ui", self)
        self.showMaximized()
        self.apply_styles()
        self.load_widgets()
        
        # Conectar todos los OctagonButtons al método que actualiza el label_button_name
        self.connect_octagon_buttons()
    
    def load_custom_font(self, font_path, font_size, fallback_font, fallback_size):
        """Carga una fuente personalizada o usa una fuente de reserva."""
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            return QFont(font_family, font_size)
        return QFont(fallback_font, fallback_size)
    
    def apply_styles(self):
        """Aplica los estilos al topbar y los botones."""
        custom_font = self.load_custom_font("src/assets/font/ratchet-clank-psp.ttf", 24, "Arial", 18)
        self.button_back.style('fa.angle-left', QSize(32, 32), "Atras", 'white')
        self.topbar.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border-radius: 10px;")
        self.label_module.setText("Consolas")
        self.label_module.setStyleSheet("background-color: transparent; color: white; font-size: 26px; font-weight: bold;")
        self.label_module.setFont(custom_font)
        self.label_optimize.setVisible(False)
        self.button_back.clicked.connect(self.back_clicked.emit)
        self.label_interactive_preview.setFont(custom_font)
        self.label_interactive_preview.setText("Vista previa interactiva")
        self.label_interactive_preview.setStyleSheet("color: white; font-size: 26px;")
        self.label_button_name.setFont(custom_font)
        self.label_button_name.setStyleSheet("color: white; font-size: 26px;")
        self.label_button_functinality.setFont(custom_font)
        self.label_button_functinality.setText("Funcionalidad del botón")   
        self.label_button_functinality.setStyleSheet("color: white; font-size: 26px;")
        self.label_optimize.setFont(custom_font)
        self.label_optimize.setStyleSheet("background-color: transparent; color: #00ff00; font-size: 20px; font-weight: bold;")
        self.label_select_controller.setFont(custom_font)
        self.label_select_controller.setText("Selecciona un control")
        self.label_select_controller.setStyleSheet("color: white; font-size: 26px;")
        self.label_tittle_options.setFont(custom_font)
        self.label_tittle_options.setText("Opciones")
        self.label_tittle_options.setStyleSheet("color: white; font-size: 26px;")
        # caambio el tipo de fuente personalizada a los QRadioButton a custom_font
        self.option_keyboard.setFont(custom_font)
        self.option_controller.setFont(custom_font)
        self.option_keyboard.setStyleSheet("font-size: 18px; color: white;")
        self.option_controller.setStyleSheet("font-size: 18px; color: white;")
        # agrego el CoverConsole que es el widget que contiene el gradiente al QFrame image_module
        self.cover_console = CoverConsole(self.GIFS_CONSOLES)
        self.image_module.layout().addWidget(self.cover_console)
        
    def load_widgets(self):
        """Carga los widgets necesarios al QFrame interactive_preview_content."""
        # Verificar si el widget tiene un layout, si no, asignar uno
        if self.interactive_preview_content.layout() is None:
            self.interactive_preview_content.setLayout(QVBoxLayout())
        
        # Ahora se puede añadir el widget al layout
        self.keyboard_interactive = KeyboardInteractive()
        self.interactive_preview_content.layout().addWidget(self.keyboard_interactive)

    def handle_optimizer_hidden(self):
        """Muestra el mensaje de optimización y lo oculta después de un tiempo."""
        self.label_optimize.setStyleSheet("background-color: transparent; color: #00ff00; font-size: 20px; font-weight: bold;")
        self.label_optimize.setVisible(True)
        self.label_optimize.setText("Recursos optimizados")
        QTimer.singleShot(3000, self.hide_optimizer)
    
    def hide_optimizer(self):
        """Oculta el mensaje de optimización."""
        self.label_optimize.setVisible(False)
        
    def connect_octagon_buttons(self):
        """Conectar la señal de hover de los OctagonButton a la actualización del label."""
        buttons = self.findChildren(OctagonButton)  # Encontrar todos los OctagonButton en el widget
        for button in buttons:
            button.hovered_signal.connect(self.update_selected_button)

    def update_selected_button(self, button_name):
        # Obtener el layout actual de 'self.selected_button'
        layout = self.selected_button.layout()
        
        # Verificar si el layout existe y eliminar sus widgets
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()  # Eliminar el widget de la memoria

        # Crear un nuevo widget y añadirlo al layout
        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        widget.layout().setContentsMargins(0, 0, 0, 0)
        widget.layout().setSpacing(0)

        # Crear y configurar el OctagonButton
        button = OctagonButton(button_name)
        button.setStyleSheet("font-size: 28px;")  # Ajusta el tamaño de la fuente
        button.setMinimumSize(QSize(230, 230))  # Establece el tamaño mínimo
        button.setMaximumSize(QSize(380, 380))  # Establece el tamaño máximo
        # Puedes usar setFixedSize(QSize(200, 200)) para establecer un tamaño fijo

        widget.layout().addWidget(button)

        # Verificar si el layout existe antes de añadir el nuevo widget
        if self.selected_button.layout() is None:
            self.selected_button.setLayout(QVBoxLayout())
        
        # Centrar el contenido
        layout = self.selected_button.layout()
        layout.setContentsMargins(0, 0, 0, 0)  # Elimina los márgenes
        layout.setSpacing(0)  # Establece el espaciado a 0
        
        # Añadir un espaciador para centrar el contenido
        layout.addStretch()  # Añade un espaciador antes del widget
        layout.addWidget(widget, alignment=Qt.AlignCenter)  # Centra el widget horizontalmente
        layout.addStretch()  # Añade un espaciador después del widget