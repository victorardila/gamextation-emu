from config.storagesys.storage_system import StorageSystem
from PyQt5.QtWidgets import QApplication
from src.app import Aplicacion
from watcher import start_watching
import shutil
import sys
import os
import threading
import psutil


def remove_pycache_dirs():
    """Elimina todos los directorios __pycache__ del proyecto."""
    for root, dirs, files in os.walk("."):
        for dir in dirs:
            if dir == "__pycache__":
                shutil.rmtree(os.path.join(root, dir))


def create_config_file():
    """Crea un archivo de configuración si no existe."""
    config_file = "config.ini"
    if not os.path.exists(config_file):
        settings = {"General": {"sound": "on", "theme": "light", "language": "en"}}
        storage = StorageSystem(config_file)
        storage.create_config(settings)


def main():
    """Función principal para ejecutar la aplicación."""
    create_config_file()

    # Iniciar la aplicación PyQt
    app = QApplication(sys.argv)
    # Elimina directorios __pycache__ generados por Python
    remove_pycache_dirs()

    # Crear instancia de Aplicacion y acceder a MainContainer
    application = Aplicacion()

    # Obtener el PID de la aplicación actual
    current_process = psutil.Process(os.getpid())

    # Iniciar el watcher en un hilo separado, pasando la ventana a cerrar
    watcher_thread = threading.Thread(target=start_watching, args=(".", application))
    watcher_thread.daemon = True  # Hilo en segundo plano
    watcher_thread.start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
