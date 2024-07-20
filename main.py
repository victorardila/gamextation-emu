import os
import sys
import shutil
from PyQt5.QtWidgets import QApplication
from src.app import Aplicacion

def remove_pycache_dirs():
    for root, dirs, files in os.walk('.'):
        for dir in dirs:
            if dir == '__pycache__':
                shutil.rmtree(os.path.join(root, dir))

def main():
    app = QApplication(sys.argv)
    # Eliminar directorios __pycache__ generados por Python
    remove_pycache_dirs()
    aplication = Aplicacion()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
