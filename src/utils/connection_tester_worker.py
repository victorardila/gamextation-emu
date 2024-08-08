from PyQt5.QtCore import QThread, pyqtSignal
from src.services.connection_request_services import ConnectionRequestsServices

class ConnectionTesterWorker(QThread):
    # Creo una señal para enviar la url y el estado de la conexión
    stateConnection = pyqtSignal(str, bool)

    def __init__(self, urlToCheck, check_interval=5000, parent=None):
        super().__init__(parent)
        self.check_interval = check_interval  # Intervalo de verificación en milisegundos
        self.url_to_check = urlToCheck

    def run(self):
        while True:
            connection_request_services = ConnectionRequestsServices()
            state = connection_request_services.check_connection_state(self.url_to_check)
            self.stateConnection.emit(self.url_to_check, state)
            self.msleep(self.check_interval)