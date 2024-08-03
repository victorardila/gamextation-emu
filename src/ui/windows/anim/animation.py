from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import pygame
import os

class Animation(QMainWindow):
    video_finished = pyqtSignal()
    sound_path = 'src/assets/sfx/intro.mp3'

    def __init__(self):
        super().__init__()
        self.init_sfx()
        self.init_ui()

    def init_ui(self):
        loadUi("src/ui/windows/anim/animation.ui", self)
        self.setup_window_properties()
        self.setup_video_player()
        self.play_video()

    def setup_window_properties(self):
        self.showMaximized()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(QIcon("src/assets/ico/icon.png"))

    def setup_video_player(self):
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget(self.centralwidget)
        self.media_player.setVideoOutput(self.video_widget)
        self.verticalLayout.addWidget(self.video_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        video_path = os.path.abspath("src/assets/video/Rander.mp4")
        video_url = QUrl.fromLocalFile(video_path)
        self.media_player.setMedia(QMediaContent(video_url))
        self.media_player.mediaStatusChanged.connect(self.handle_media_status_changed)

    def play_video(self):
        self.media_player.play()

    def init_sfx(self):
        pygame.mixer.init()
        self.intro_sound = pygame.mixer.Sound(self.sound_path)
        self.intro_sound.set_volume(0.5)
        self.intro_sound.play()

    def handle_media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.media_player.stop()
            self.video_finished.emit()