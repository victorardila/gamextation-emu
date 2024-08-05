from io import BytesIO
import requests

class GameRequestsServices:
    def __init__(self):
        self.get_images()
    
    # Obtener imagenes de los juegos
    def get_images(self, urlImage):
        """Obtiene las imágenes de los juegos."""
        # Descargar la imagen usando requests
        response = requests.get(urlImage)
        # Verificar si la respuesta es una imagen
        if 'image' not in response.headers.get('Content-Type', ''):
            print("La URL no devuelve una imagen válida.")
            return
        # Crear un BytesIO con los datos de la imagen descargada
        image_data = BytesIO(response.content)
        return image_data
