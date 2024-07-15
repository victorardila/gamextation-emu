import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt5.QtCore import Qt, QUrl, QTimer, QPropertyAnimation
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.uic import loadUi
from src.views.mainApp import MainApp

class Aplicacion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InicializarGUI()

    def InicializarGUI(self):
        loadUi("src/views/Intro.ui", self)
        self.showMaximized()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
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
            self.fade_out_intro()

    def fade_out_intro(self):
        # Animación de desvanecimiento de la ventana de introducción
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.finished.connect(self.show_main_app)
        self.animation.setDuration(1000)  # Duración de la animación en milisegundos
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.start()

    def show_main_app(self):
        # Mostrar la ventana principal (MainApp) después de que la intro se ha desvanecido
        self.main_app = MainApp()
        self.main_app.setWindowOpacity(0.0)  # Configurar la opacidad inicial en 0
        self.main_app.show()

        # Animación de aparición de la ventana principal
        self.main_app_animation = QPropertyAnimation(self.main_app, b"windowOpacity")
        self.main_app_animation.setDuration(100)  # Duración de la animación en milisegundos
        self.main_app_animation.setStartValue(0.0)
        self.main_app_animation.setEndValue(1.0)
        self.main_app_animation.start()

        self.close()  # Cerrar la ventana de introducción