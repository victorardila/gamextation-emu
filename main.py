import sys
from PyQt5.QtWidgets import *
from src.app import Aplicacion

def main():
    app = QApplication(sys.argv)
    ventana = Aplicacion()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()