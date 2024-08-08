from src.ui.components.cover.cover_game import CoverGame
from PyQt5.QtCore import QSize, pyqtSignal, QTimer, Qt
from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtGui import QFont, QFontDatabase, QPainter, QColor, QMovie
# from src.ui.components.cover.cover_console import CoverConsole
from PyQt5.uic import loadUi

class Consoles(QWidget):
    optimizer_hidden = pyqtSignal()
    back_clicked = pyqtSignal()
    GIF_CONSOLE = "src/assets/gif/console.gif"
    
    # arreglo de imagenes gif de consolas
    # GIF_CONSOLE = [
    #     "src/assets/gif/console.gif",
    #     "src/assets/gif/console2.gif",
    #     "src/assets/gif/console3.gif",
    # ]
    
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
        
        # Cargar al label label_gif la imagen de la consola
        self.load_gif()
        
    def load_gif(self):
        """Carga el GIF en el QLabel y ajusta su tamaño."""
        self.movie = QMovie(self.GIF_CONSOLE)
        self.label_gif.setMovie(self.movie)
        self.movie.frameChanged.connect(self.resize_gif)
        self.movie.start()
        
    def resize_gif(self):
        """Ajusta el tamaño del GIF al ancho del QLabel manteniendo la proporción."""
        frame = self.movie.currentPixmap()
        if not frame.isNull():
            label_width = self.label_gif.width()
            frame = frame.scaledToWidth(label_width, Qt.SmoothTransformation)
            self.label_gif.setPixmap(frame)
        
    def handle_optimizer_hidden(self):
        """Muestra el mensaje de optimización y lo oculta después de un tiempo."""
        self.label_optimize.setStyleSheet("background-color: transparent; color: #00ff00; font-size: 20px; font-weight: bold;")
        self.label_optimize.setVisible(True)
        self.label_optimize.setText("Recursos optimizados")
        QTimer.singleShot(3000, self.hide_optimizer)
    
    def hide_optimizer(self):
        """Oculta el mensaje de optimización."""
        self.label_optimize.setVisible(False)