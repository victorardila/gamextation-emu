import requests
from io import BytesIO

class GameRequestsServices:
    def __init__(self):
        pass

    def get_image(self, image_url):
        try:
            response = requests.get(image_url)    
            response.raise_for_status()  # Levanta un error si la solicitud no fue exitosa
            # Verificar si la respuesta es una imagen
            if 'image' not in response.headers.get('Content-Type', ''):
                print("La URL no devuelve una imagen válida.")
                return
            # Crear un BytesIO con los datos de la imagen descargada
            image_data = BytesIO(response.content)
            return image_data
        except requests.RequestException as e:
            print(f"Error downloading {image_url}: {e}")
            return None  # O maneja el error de otra manera
