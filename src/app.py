from config.dependencies.container_platform import ContainerPlatform
from src.ui.windows.container.main_container import MainContainer
from src.ui.windows.dialogs.dialog_message import DialogMessage
from src.ui.windows.anim.animation import Animation
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QMainWindow

class Aplicacion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_views_container()
        
    # Diccionario de validaciones
    validations = {
        "docker": ContainerPlatform.checkDocker(),
    }
    
    def init_views_container(self):
        """Inicializa el contenedor de vistas y gestiona la lógica de validación."""
        # Verifica las validaciones
        all_validations_passed = all(value[0] for value in self.validations.values())

        if all_validations_passed:
            self.show_intro_animation()
        else:
            self.show_validation_errors()

    def show_intro_animation(self):
        """Muestra la ventana de introducción y configura la animación de desvanecimiento."""
        self.intro = Animation()
        self.intro.video_finished.connect(self.fade_out_intro)
        self.intro.show()

    def show_validation_errors(self):
        """Muestra un diálogo con los errores de validación."""
        dialog_message = DialogMessage()
        for key, value in self.validations.items():
            if not value[0]:
                dialog_message.show_message_box(value)

    def fade_out_intro(self):
        """Gestiona la animación de desvanecimiento de la ventana de introducción."""
        self.animation = QPropertyAnimation(self.intro, b"windowOpacity")
        self.animation.finished.connect(self.show_main_container)
        self.animation.setDuration(1000)  # Duración en milisegundos
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.start()

    def show_main_container(self):
        """Muestra la ventana principal después de la animación de desvanecimiento."""
        self.views_container = MainContainer()
        self.views_container.setWindowOpacity(0.0)  # Configurar la opacidad inicial en 0
        self.views_container.show()

        # Animación de aparición de la ventana principal
        self.views_container_animation = QPropertyAnimation(self.views_container, b"windowOpacity")
        self.views_container_animation.setDuration(10)  # Duración en milisegundos
        self.views_container_animation.setStartValue(0.0)
        self.views_container_animation.setEndValue(1.0)
        self.views_container_animation.start()

        # Cierra la ventana de introducción
        self.intro.close()