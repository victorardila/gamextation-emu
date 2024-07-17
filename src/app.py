from PyQt5.QtWidgets import QMainWindow
from src.windows.container.main_container import MainContainer
from src.windows.dialogs.dialog_message import DialogMessage
from config.container_platform import ContainerPlatform

class Aplicacion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitViewsContainer()
        
    def InitViewsContainer(self):
        response = ContainerPlatform.checkDocker()
        dialog_message = DialogMessage()
        check = dialog_message.showMessageBox(response)
        if check:
            self.viewsContainer = MainContainer()