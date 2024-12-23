from config.storagesys.storage_system import StorageSystem
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from src.ui.views.menu.main_menu import MainMenu
from src.ui.views.submenu.submenu import SubMenu
from src.ui.views.game.game_loaded import GameLoaded
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
import random
import pygame
import os


class MainContainer(QMainWindow):
    SOUND = None

    def __init__(self):
        super().__init__()
        self.storage = StorageSystem("config.ini")
        self.resize_timer = QTimer(self)  # Inicializa el temporizador aquí
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.print_window_size)
        self.read_config_file()
        self.init_song()
        self.init_gui()

    def read_config_file(self):
        config_file = "config.ini"
        storage = StorageSystem(config_file)
        settings = storage.read_config()
        self.SOUND = settings.get("General", {}).get("sound", None)

    def init_gui(self):
        loadUi("src/ui/windows/container/main_container.ui", self)
        self.setup_window()
        self.setup_widgets()
        self.connect_signals()

    def setup_window(self):
        self.showMaximized()
        self.setWindowTitle("GameXtation")
        self.setWindowIcon(QIcon("src/assets/ico/icon.png"))

    def setup_widgets(self):
        self.layout_views = self.centralWidget().findChild(
            QStackedWidget, "layout_views"
        )
        self.mainMenu = MainMenu()
        self.submenu = SubMenu()
        self.gameLoaded = GameLoaded()
        self.layout_views.addWidget(self.mainMenu)
        self.layout_views.addWidget(self.submenu)
        self.layout_views.addWidget(self.gameLoaded)
        self.layout_views.setCurrentWidget(self.mainMenu)

    def connect_signals(self):
        self.mainMenu.menu_button_clicked.connect(self.switch_view)
        self.mainMenu.menu_exit_clicked.connect(self.close_application)
        self.mainMenu.sound_switch_state.connect(self.switch_sound_state)
        self.submenu.menu_return_clicked.connect(self.switch_to_mainmenu)
        self.submenu.menu_exit_clicked.connect(self.close_application)
        self.submenu.game_data_received.connect(self.switch_view)
        self.gameLoaded.return_to_menu.connect(self.switch_view)

    def init_song(self):
        if self.SOUND == "on":
            self.song_path = "src/assets/song/"
            self.song_files = [
                f"{self.song_path}{file}"
                for file in os.listdir(self.song_path)
                if file.endswith(".mp3")
            ]
            self.current_song = None
            self.play_song()

    def play_song(self):
        if not self.song_files:
            self.reload_song_files()

        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.3)

        if self.current_song:
            pygame.mixer.music.stop()

        random_index = random.randint(0, len(self.song_files) - 1)
        self.current_song = self.song_files.pop(random_index)

        pygame.mixer.music.load(self.current_song)
        pygame.mixer.music.play()
        self.song_files.append(self.current_song)

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.queue(self.song_files[0])

    def reload_song_files(self):
        self.song_files = [
            f"{self.song_path}{file}"
            for file in os.listdir(self.song_path)
            if file.endswith(".mp3")
        ]

    def switch_view(self, message):
        if "Submenu" in message:
            self.layout_views.setCurrentWidget(self.submenu)
            self.submenu.load_module(message)
        elif "Game" in message:
            self.layout_views.setCurrentWidget(self.gameLoaded)
        else:
            self.layout_views.setCurrentWidget(self.mainMenu)

    def switch_sound_state(self):
        if self.SOUND == "on":
            self.SOUND = "off"
            self.storage.update_config("General", "sound", "off")
            pygame.mixer.music.stop()
        else:
            self.SOUND = "on"
            self.storage.update_config("General", "sound", "on")
            self.init_song()

    def switch_to_mainmenu(self):
        self.layout_views.setCurrentWidget(self.mainMenu)

    def close_application(self):
        self.close()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_timer.start(200)  # Reinicia el temporizador a 200 ms

    def print_window_size(self):
        width = self.width()
        height = self.height()
        self.storage.update_config("General", "screenwidth", str(width))
        self.storage.update_config("General", "screenheight", str(height))
