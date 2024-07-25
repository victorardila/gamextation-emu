from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import QSize
from PyQt5.uic import loadUi
from src.components.cover.cover_game import CoverGame
class Roms(QWidget):
    def __init__(self, parent=None):
        super(Roms, self).__init__(parent)
        self.setupUi()
    
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
        # activo el Grid layout de QWidget content
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