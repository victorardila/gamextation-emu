from PyQt5.QtWidgets import QMainWindow
from src.windows.container.main_container import MainContainer
from PyQt5.QtCore import QPropertyAnimation
from src.windows.anim.animation import Animation
from src.windows.dialogs.dialog_message import DialogMessage
from config.dependencies.container_platform import ContainerPlatform

class Aplicacion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitViewsContainer()
        
    # Arrray de validacioens
    validations = {
        "docker": ContainerPlatform.checkDocker(),
    }
    
    def InitViewsContainer(self):
        # recorro el array de validaciones
        validateds = []
        for key, value in self.validations.items():
            if value[0] == False:
                validateds.append(False)
            else:
                validateds.append(True)
        
        # Si todas las validaciones son correctas, se muestra la ventana de introducción
        if all(validateds):
            self.intro = Animation()
            self.intro.video_finished.connect(self.fade_out_intro)
            self.intro.show()
        else:
            # mostrar cada valor falso en un dialogo
            dialog_message = DialogMessage()
            for key, value in self.validations.items():
                if value[0] == False:
                    dialog_message.showMessageBox(value)
    
    def fade_out_intro(self):
        # Animación de desvanecimiento de la ventana de introducción
        self.animation = QPropertyAnimation(self.intro, b"windowOpacity")
        self.animation.finished.connect(self.showMainContainer)
        self.animation.setDuration(1000)  # Duración de la animación en milisegundos
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.start()

    def showMainContainer(self):
        # Mostrar la ventana principal (MainApp) después de que la intro se ha desvanecido
        self.views_container = MainContainer()
        self.views_container.setWindowOpacity(0.0)  # Configurar la opacidad inicial en 0
        self.views_container.show()

        # Animación de aparición de la ventana principal
        self.views_container_animation = QPropertyAnimation(self.views_container, b"windowOpacity")
        self.views_container_animation.setDuration(10)  # Duración de la animación en milisegundos
        self.views_container_animation.setStartValue(0.0)
        self.views_container_animation.setEndValue(1.0)
        self.views_container_animation.start()

        # Cierro la ventana Intro
        self.intro.close()