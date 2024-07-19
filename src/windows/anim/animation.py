from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.uic import loadUi
import os

class Animation(QMainWindow):
    video_finished = pyqtSignal()  # Definir una señal que será emitida cuando el video termine

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        loadUi("src/windows/anim/animation.ui", self)
        self.showMaximized()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Cambiar icono de la ventana
        self.setWindowIcon(QIcon("src/assets/ico/icon.png"))
        self.verticalLayout = QVBoxLayout(self.centralwidget)

        # Configuración del reproductor de video
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget(self.centralwidget)
        self.media_player.setVideoOutput(self.video_widget)
        self.verticalLayout.addWidget(self.video_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # Ruta del archivo MP4
        video_path = os.path.abspath("src/assets/video/Rander.mp4")
        video_url = QUrl.fromLocalFile(video_path)
        self.media_player.setMedia(QMediaContent(video_url))

        # Conectar la señal para detectar el final del video
        self.media_player.mediaStatusChanged.connect(self.handle_media_status_changed)

        # Reproducir el video al iniciar
        self.media_player.play()

    def handle_media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.media_player.stop()
            self.video_finished.emit()  # Emitir la señal cuando el video termine