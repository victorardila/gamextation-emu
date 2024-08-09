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
        
    def apply_styles(self):
        """Aplica los estilos al topbar y los botones."""
        self.button_back.style('fa.angle-left', QSize(32, 32), "Atras", 'white')
        self.topbar.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border-radius: 10px;")
        self.label_module.setStyleSheet("background-color: transparent; color: white; font-size: 20px; font-weight: bold;")
        self.label_module.setText("Consolas")
        self.label_optimize.setVisible(False)
        self.button_back.clicked.connect(self.back_clicked.emit)
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