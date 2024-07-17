from PyQt5.QtWidgets import QMessageBox
from qtawesome import icon
import sys

class DialogMessage():
    def __init__(self):
        pass

    def showMessageBox(self, response):
        if not response[0]:
            dialog = QMessageBox()
            dialog.setStyleSheet("""
                QMessageBox {
                    background-color: #fff;
                    font-size: 18px; /* Tamaño de la fuente personalizado */
                }
            """)
            dialog.setWindowTitle(response[1])
            # Agregar un icono al mensaje de alerta
            icon_warning = icon('fa.exclamation-triangle', color='red')  # Icono de FontAwesome para advertencia
            dialog.setIconPixmap(icon_warning.pixmap(40))  # Tamaño del icono
            dialog.setText(response[2])
            dialog.setInformativeText(response[3])
            # Personalizar el tamaño de la fuente del texto del botón
            dialog.setStandardButtons(QMessageBox.Ok)
            # Cambiar texto del botón por "Cerrar" y hacer la letra más grande
            dialog.button(QMessageBox.Ok).setText("Cerrar")
            # Cambiar el estilo del botón con efecto hover
            dialog.button(QMessageBox.Ok).setStyleSheet("""
                font-size: 18px;
                background-color:
                    qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #E1E1E1, stop:1 #FFFFFF);
                border: 1px solid #888888;
                border-radius: 10px;
                padding: 5px;
                margin: 5px;
            """)
            dialog.buttonClicked.connect(dialog.close)
            
            dialog.exec_()
            sys.exit()
        return response[0]