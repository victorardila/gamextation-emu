import os
import sys
import shutil
from PyQt5.QtWidgets import QApplication
from src.app import Aplicacion
from config.storagesys.storage_system import StorageSystem

def remove_pycache_dirs():
    for root, dirs, files in os.walk('.'):
        for dir in dirs:
            if dir == '__pycache__':
                shutil.rmtree(os.path.join(root, dir))

# crea un archivo de configuración si no existe
def create_config_file():
    config_file = 'config.ini'
    storage = StorageSystem(config_file)
    if not os.path.exists(config_file):
        settings = {
            'General': {
                'sound': 'on',
                'theme': 'light',
                'language': 'en'
            }
        }
        storage.create_config(settings)

def main():
    create_config_file()
    app = QApplication(sys.argv)
    # Eliminar directorios __pycache__ generados por Python
    remove_pycache_dirs()
    aplication = Aplicacion()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
