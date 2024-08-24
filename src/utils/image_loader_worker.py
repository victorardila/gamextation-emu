from PyQt5.QtCore import QThread, pyqtSignal
from src.services.game_requests_services import GameRequestsServices


class ImageLoaderWorker(QThread):
    # Creo una señal que emite la URL y la imagen que es de tipo BytesIO
    image_loaded = pyqtSignal(str, object)

    def __init__(self, image_url, parent=None):
        super().__init__(parent)
        self.image_url = image_url

    def run(self):
        game_request_service = GameRequestsServices()
        image = game_request_service.get_image(self.image_url)  # Obtén la imagen
        if image:
            self.image_loaded.emit(self.image_url, image)  # Emite la imagen cargada
        else:
            print(f"Error al descargar la imagen desde {self.image_url}")
