from src.ui.components.cover.cover_game import CoverGame
from PyQt5.QtCore import QSize, pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtGui import QFont, QFontDatabase, QPainter, QColor
from PyQt5.uic import loadUi
from io import BytesIO
import json
# Render loader
from src.ui.components.loader.render_loader import RenderLoader
from src.utils.image_loader_worker import ImageLoaderWorker

class Roms(QWidget):
    default_game_path = 'src/data/games_default.json'
    games = []
    back_clicked = pyqtSignal()
    optimizer_hidden = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.loader = RenderLoader(self)
        self.loader.show_centered(self)  # Mostrar el loader centrado sobre el widget Roms
        self.setupUi()
        self.optimizer_hidden.connect(self.handle_optimizer_hidden)
        self.image_loader_workers = []  # Mantén una referencia a los workers
        self.load_games()

    def load_games(self):
        """Carga los juegos desde el archivo JSON."""
        with open(self.default_game_path, 'r') as file:
            self.games = json.load(file)
        image_urls = [game["cover_image"] for category in self.games.values() for game in category]
        for url in image_urls:
            image_loader = ImageLoaderWorker(url)
            image_loader.image_loaded.connect(self.on_image_loaded)
            self.image_loader_workers.append(image_loader)  # Mantén la referencia
            image_loader.start()
            
    def load_custom_font(self, font_path, font_size, fallback_font, fallback_size):
        """Carga una fuente personalizada o usa una fuente de reserva."""
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            return QFont(font_family, font_size)
        return QFont(fallback_font, fallback_size)

    def on_image_loaded(self, image_url, image):
        """Maneja la señal cuando una imagen está cargada."""
        # Reemplazo la URL de la imagen por la imagen descargada
        for category in self.games.values():
            for game in category:
                if game["cover_image"] == image_url:
                    game["cover_image"] = image
                    break

        # Verifica si todas las imágenes han sido cargadas
        if all(isinstance(game["cover_image"], BytesIO) for category in self.games.values() for game in category):
            self.loader.hide()  # Ocultar el loader una vez que se hayan cargado todas las imágenes
            self.load_cover_games()  # Carga las portadas de los juegos después de obtener las imágenes

    def setupUi(self):
        """Configura la interfaz de usuario."""
        loadUi("src/ui/modules/roms/roms.ui", self)
        self.showMaximized()
        self.apply_styles()
        self.setup_layout()
    
    def apply_styles(self):
        """Aplica los estilos al topbar y los botones."""
        self.button_back.style('fa.angle-left', QSize(32, 32), "Atras", 'white')
        self.topbar.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border-radius: 10px;")
        self.label_module.setStyleSheet("background-color: transparent; color: white; font-size: 20px; font-weight: bold;")
        self.label_module.setText("Roms")
        self.label_name_game.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.label_name_game.setText("")
        self.label_optimize.setVisible(False)
        self.button_back.clicked.connect(self.back_clicked.emit)

    def setup_layout(self):
        """Configura el layout del widget de contenido."""
        self.grid_layout = QGridLayout(self.content)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.content.setLayout(self.grid_layout)

    def load_cover_games(self):
        """Carga y distribuye las portadas de los juegos en el grid layout."""
        num_columns = 5
        num_rows_default = 3
        total_slots_default = num_columns * num_rows_default
        games_desktop = self.games.get('desktop', [])
        games_browser = self.games.get('browser', [])
        
        used_desktop_games = []
        used_browser_games = []
        index_desktop = 0
        index_browser = 0

        for i in range(total_slots_default):
            # Obtengo la peticion y la envio al render_loader
            cover_game = CoverGame()
            cover_game.game_hovered.connect(self.handle_game_hovered)
            if i % 2 == 0 and index_desktop < len(games_desktop):
                index_desktop = self.find_next_available_index(games_desktop, used_desktop_games, index_desktop)
                if index_desktop < len(games_desktop):
                    cover_game.load_game(games_desktop[index_desktop])
                    used_desktop_games.append(games_desktop[index_desktop])
                    index_desktop += 1
            elif index_browser < len(games_browser):
                index_browser = self.find_next_available_index(games_browser, used_browser_games, index_browser)
                if index_browser < len(games_browser):
                    cover_game.load_game(games_browser[index_browser])
                    used_browser_games.append(games_browser[index_browser])
                    index_browser += 1
            else:
                if index_desktop < len(games_desktop):
                    cover_game.load_game(games_desktop[index_desktop])
                    used_desktop_games.append(games_desktop[index_desktop])
                    index_desktop += 1
                elif index_browser < len(games_browser):
                    cover_game.load_game(games_browser[index_browser])
                    used_browser_games.append(games_browser[index_browser])
                    index_browser += 1
                else:
                    break

            row = i // num_columns
            column = i % num_columns
            self.grid_layout.addWidget(cover_game, row, column)

        self.fill_empty_slots(total_slots_default, num_columns)

    def find_next_available_index(self, games_list, used_games, index):
        """Encuentra el próximo índice disponible para un juego que no ha sido usado."""
        while index < len(games_list) and games_list[index] in used_games:
            index += 1
        return index

    def fill_empty_slots(self, total_slots, num_columns):
        """Llena los slots vacíos con widgets de marcador de posición."""
        num_filled_slots = len(self.games['desktop']) + len(self.games['browser'])
        for i in range(num_filled_slots, total_slots):
            placeholder = QWidget()
            row = i // num_columns
            column = i % num_columns
            self.grid_layout.addWidget(placeholder, row, column)

    def handle_optimizer_hidden(self):
        """Muestra el mensaje de optimización y lo oculta después de un tiempo."""
        self.label_optimize.setStyleSheet("background-color: transparent; color: #00ff00; font-size: 20px; font-weight: bold;")
        self.label_optimize.setVisible(True)
        self.label_optimize.setText("Recursos optimizados")
        QTimer.singleShot(3000, self.hide_optimizer)

    def hide_optimizer(self):
        """Oculta el label_optimize."""
        self.label_optimize.setVisible(False) 
        self.label_optimize.setText("") 
    
    def handle_game_hovered(self, game_name):
        """Actualiza el nombre del juego en el label cuando se pasa el ratón sobre una portada."""
        # cambio el tipo de letra
        custom_font = self.load_custom_font("src/assets/font/ratchet-clank-psp.ttf", 24, "Arial", 18)
        self.label_name_game.setText(game_name)
        self.label_name_game.setFont(custom_font)
        self.label_name_game.setStyleSheet("color: white; font-size: 28px;")
    
    # Este metodo es para observar el diseño del widget contenedor
    # def paintEvent(self, event):
    #     """Rellena el área del widget padre con un color para depuración."""
    #     super().paintEvent(event)  # Llama al paintEvent base para asegurar que se dibuje lo demás
    #     painter = QPainter(self)
    #     painter.setBrush(QColor(255, 0, 0, 50))  # Color rojo con transparencia
    #     painter.drawRect(self.rect())  # Dibuja un rectángulo que cubre todo el widget padre