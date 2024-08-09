from src.ui.components.cover.cover_console import CoverConsole
from PyQt5.QtCore import QSize, pyqtSignal, QTimer, Qt
from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtGui import QFont, QFontDatabase, QPainter, QColor, QMovie
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
        self.label_select_command.setFont(custom_font)
        self.label_select_command.setText("Selecciona una consola para jugar")
        self.label_select_command.setStyleSheet("color: white; font-size: 26px;")
        # agrego el CoverConsole que es el widget que contiene el gradiente al QFrame image_module
        self.cover_console = CoverConsole(self.GIFS_CONSOLES)
        self.image_module.layout().addWidget(self.cover_console)
        
    def handle_optimizer_hidden(self):
        """Muestra el mensaje de optimización y lo oculta después de un tiempo."""
        self.label_optimize.setStyleSheet("background-color: transparent; color: #00ff00; font-size: 20px; font-weight: bold;")
        self.label_optimize.setVisible(True)
        self.label_optimize.setText("Recursos optimizados")
        QTimer.singleShot(3000, self.hide_optimizer)
    
    def hide_optimizer(self):
        """Oculta el mensaje de optimización."""
        self.label_optimize.setVisible(False)