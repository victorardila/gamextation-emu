import json
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import QSize, pyqtSignal, QTimer
from src.components.cover.cover_game import CoverGame

class Roms(QWidget):
    default_game_path = 'src/data/games_default.json'
    games = []
    back_clicked = pyqtSignal()  # Definir la señal
    optimizer_hidden = pyqtSignal()  # Define la señal
    
    def __init__(self, parent=None):
        super(Roms, self).__init__(parent)
        self.load_games()
        self.setupUi()
        self.optimizer_hidden.connect(self.handle_optimizer_hidden)
    
    def load_games(self):
        with open(self.default_game_path, 'r') as file:
            self.games = json.load(file)
    
    def setupUi(self):
        loadUi("src/modules/roms/roms.ui", self)
        self.showMaximized()
        
        # Estilos del topbar del widget
        self.button_back.style('fa.angle-left', QSize(32, 32), "Atras", 'white')
        self.topbar.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border-radius: 10px;")
        self.label_module.setStyleSheet("background-color: transparent; color: white; font-size: 20px; font-weight: bold;")
        self.label_module.setText("Roms")
        self.label_name_game.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.label_name_game.setText("")
        # label_optimize no va a estar visible en un principio
        self.label_optimize.setVisible(False)
        
        # Conectar el botón a la señal
        self.button_back.clicked.connect(self.back_clicked.emit)

        # Activo el Grid layout de QWidget content
        self.grid_layout = QGridLayout(self.content)  # Guardar grid_layout como un atributo de la clase
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.content.setLayout(self.grid_layout)
        self.load_cover_games()
    
    def load_cover_games(self):
        """Método que carga los juegos en la interfaz."""
        num_columns = 5
        num_rows_default = 3
        total_slots_default = num_columns * num_rows_default
        games_desktop = self.games['desktop']
        games_browser = self.games['browser']
        
        # Utilizamos listas para evitar juegos repetidos
        used_desktop_games = []
        used_browser_games = []

        # Índices para los juegos de desktop y browser
        index_desktop = 0
        index_browser = 0

        for i in range(total_slots_default):
            cover_game = CoverGame()
            
            # Conectar la señal game_hovered a la función handle_game_hovered
            cover_game.game_hovered.connect(self.handle_game_hovered)
            
            if i % 2 == 0 and index_desktop < len(games_desktop):
                # Cargar un juego de desktop
                while games_desktop[index_desktop] in used_desktop_games and index_desktop < len(games_desktop):
                    index_desktop += 1
                if index_desktop < len(games_desktop):
                    cover_game.load_game(games_desktop[index_desktop])
                    used_desktop_games.append(games_desktop[index_desktop])
                    index_desktop += 1
            elif index_browser < len(games_browser):
                while games_browser[index_browser] in used_browser_games and index_browser < len(games_browser):
                    index_browser += 1
                if index_browser < len(games_browser):
                    cover_game.load_game(games_browser[index_browser])
                    used_browser_games.append(games_browser[index_browser])
                    index_browser += 1
            else:
                # Si no hay más juegos de uno de los tipos, usar el otro tipo
                if index_desktop < len(games_desktop):
                    cover_game.load_game(games_desktop[index_desktop])
                    used_desktop_games.append(games_desktop[index_desktop])
                    index_desktop += 1
                elif index_browser < len(games_browser):
                    cover_game.load_game(games_browser[index_browser])
                    used_browser_games.append(games_browser[index_browser])
                    index_browser += 1
                else:
                    # Si no hay más juegos de ninguno de los tipos, no se debe cargar más juegos
                    break

            row = i // num_columns
            column = i % num_columns
            self.grid_layout.addWidget(cover_game, row, column)

        # Llenar los slots vacíos si hay menos juegos que slots
        for i in range(len(self.games['desktop']) + len(self.games['browser']), total_slots_default):
            placeholder = QWidget()  # Puedes personalizar este widget si deseas
            row = i // num_columns
            column = i % num_columns
            self.grid_layout.addWidget(placeholder, row, column)

    def handle_optimizer_hidden(self):
        """Método que maneja la señal optimizer_hidden."""
        self.label_optimize.setStyleSheet("background-color: transparent; color: #00ff00; font-size: 20px; font-weight: bold;")
        self.label_optimize.setVisible(True)
        self.label_optimize.setText("Recursos optimizados")
        QTimer.singleShot(3000, self.hide_optimizer)

    def hide_optimizer(self):
        """Método que oculta el label_optimize."""
        self.label_optimize.setVisible(False) 
        self.label_optimize.setText("") 
    
    def handle_game_hovered(self, game_name):
        """Método que maneja la señal game_hovered del CoverGame."""
        self.label_name_game.setText(game_name)