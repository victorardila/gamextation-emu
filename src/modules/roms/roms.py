from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.uic import loadUi
from src.components.cover.cover_game import CoverGame

class Roms(QWidget):
    back_clicked = pyqtSignal()  # Definir la señal
    optimizer_hidden = pyqtSignal()  # Define la señal
    
    def __init__(self, parent=None):
        super(Roms, self).__init__(parent)
        self.setupUi()
        self.optimizer_hidden.connect(self.handle_optimizer_hidden)
    
    def setupUi(self):
        loadUi("src/modules/roms/roms.ui", self)
        self.showMaximized()
        
        # Estilos del topbar del widget
        self.button_back.style('fa.angle-left', QSize(32, 32), "Atras", 'white')
        self.topbar.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border-radius: 10px;")
        self.label_module.setStyleSheet("background-color: transparent; color: white; font-size: 20px; font-weight: bold;")
        self.label_module.setText("Roms")
        self.label_name_game.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.label_name_game.setText("Nombre del juego")
        # label_optimize no va a estar visible en un principio
        self.label_optimize.setVisible(False)
        
        # Conectar el botón a la señal
        self.button_back.clicked.connect(self.back_clicked.emit)

        # Activo el Grid layout de QWidget content
        grid_layout = QGridLayout(self.content)
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(10, 10, 10, 10)
        self.content.setLayout(grid_layout)
        
        num_columns = 5

        for i in range(13):
            cover_game = CoverGame()
            row = i // num_columns
            column = i % num_columns
            grid_layout.addWidget(cover_game, row, column)
            
    def handle_optimizer_hidden(self):
        """Método que maneja la señal optimizer_hidden."""
        # Estilizo el label_optimize con un verde claro
        self.label_optimize.setStyleSheet("background-color: transparent; color: #00ff00; font-size: 20px; font-weight: bold;")
        self.label_optimize.setVisible(True)
        # cambio el texto del label_optimize
        self.label_optimize.setText("Recursos optimizados")