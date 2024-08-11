from PyQt5.QtCore import QSize, pyqtSignal, QTimer, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QFont, QFontDatabase, QColor
from PyQt5.uic import loadUi

from src.ui.components.cover.cover_console import CoverConsole
from src.ui.components.controls.keyboard_interactive import KeyboardInteractive, OctagonButton


class Consoles(QWidget):
    optimizer_hidden = pyqtSignal()
    back_clicked = pyqtSignal()

    GIFS_CONSOLES = [
        "src/assets/gif/console.gif",
        "src/assets/gif/console2.gif",
        "src/assets/gif/console3.gif",
    ]

    SVGS_PATH = [
        "src/assets/svg/console.svg",
        "src/assets/svg/keyboard.svg",
    ]

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.optimizer_hidden.connect(self.handle_optimizer_hidden)

    def setup_ui(self):
        loadUi("src/ui/modules/consoles/consoles.ui", self)
        self.showMaximized()
        self.apply_styles()
        self.load_widgets()
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
        
        self.style_back_button(custom_font)
        self.style_labels(custom_font)
        self.style_options(custom_font)

        self.cover_console = CoverConsole(self.GIFS_CONSOLES)
        self.image_module.layout().addWidget(self.cover_console)

    def style_back_button(self, custom_font):
        """Aplica estilos al botón de retroceso."""
        self.button_back.style('fa.angle-left', QSize(32, 32), "Atrás", 'white')
        self.button_back.clicked.connect(self.back_clicked.emit)

    def style_labels(self, custom_font):
        """Aplica estilos a las etiquetas."""
        labels = {
            self.label_module: "Consolas",
            self.label_interactive_preview: "Vista previa interactiva",
            self.label_button_name: "",
            self.label_button_functinality: "Funcionalidad del botón",
            self.label_select_controller: "Selecciona un control",
            self.label_tittle_options: "Opciones",
            self.label_functios_avaliable: "Funciones disponibles",
            self.label_optimize: ""
        }
        for label, text in labels.items():
            label.setFont(custom_font)
            label.setText(text)
            label.setStyleSheet("color: white; font-size: 26px;")

        self.label_optimize.setVisible(False)
        self.label_optimize.setStyleSheet("background-color: transparent; color: #00ff00; font-size: 20px; font-weight: bold;")

    def style_options(self, custom_font):
        """Aplica estilos a las opciones de control."""
        self.option_keyboard.setFont(custom_font)
        self.option_controller.setFont(custom_font)
        self.option_keyboard.setStyleSheet("font-size: 24px; color: white;")
        self.option_controller.setStyleSheet("font-size: 24px; color: white;")
        self.option_controller.style(self.SVGS_PATH[0], QSize(40, 40), "Control", QColor("white"))
        self.option_keyboard.style(self.SVGS_PATH[1], QSize(40, 40), "Teclado", QColor("white"))
        self.selected_button.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border-radius: 10px;")

    def load_widgets(self):
        """Carga los widgets necesarios al QFrame interactive_preview_content."""
        if self.interactive_preview_content.layout() is None:
            self.interactive_preview_content.setLayout(QVBoxLayout())
        
        self.keyboard_interactive = KeyboardInteractive()
        self.interactive_preview_content.layout().addWidget(self.keyboard_interactive)

    def handle_optimizer_hidden(self):
        """Muestra el mensaje de optimización y lo oculta después de un tiempo."""
        self.label_optimize.setText("Recursos optimizados")
        self.label_optimize.setVisible(True)
        QTimer.singleShot(3000, self.hide_optimizer)

    def hide_optimizer(self):
        """Oculta el mensaje de optimización."""
        self.label_optimize.setVisible(False)

    def connect_octagon_buttons(self):
        """Conecta la señal de hover de los OctagonButton a la actualización del label."""
        buttons = self.findChildren(OctagonButton)
        for button in buttons:
            button.hovered_signal.connect(self.update_selected_button)

    def update_selected_button(self, button_name):
        """Actualiza la vista previa del botón seleccionado."""
        self.clear_selected_button_layout()
        button_widget = self.create_button_widget(button_name)
        self.add_widget_to_layout(button_widget)

    def clear_selected_button_layout(self):
        """Elimina los widgets del layout del botón seleccionado."""
        layout = self.selected_button.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def create_button_widget(self, button_name):
        """Crea un widget con un botón de forma octagonal."""
        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        widget.setStyleSheet("background-color: transparent;")
        widget.layout().setContentsMargins(0, 0, 0, 0)
        widget.layout().setSpacing(0)

        button = OctagonButton(button_name)
        button.setStyleSheet("font-size: 30px;")
        button.setFixedSize(QSize(230, 230))

        widget.layout().addWidget(button)
        return widget

    def add_widget_to_layout(self, widget):
        """Añade un widget al layout de 'self.selected_button'."""
        if self.selected_button.layout() is None:
            self.selected_button.setLayout(QVBoxLayout())
        
        layout = self.selected_button.layout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addStretch()
        layout.addWidget(widget, alignment=Qt.AlignCenter)
        layout.addStretch()