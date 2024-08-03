from PyQt5.QtWidgets import QMessageBox
from qtawesome import icon
import webbrowser
import sys

class DialogMessage:
    def __init__(self):
        pass

    def show_message_box(self, response):
        """Display a message box with custom styling and buttons."""
        if not response[0]:
            dialog = QMessageBox()
            self.setup_message_box(dialog, response)
            dialog.exec_()
            sys.exit()

    def setup_message_box(self, dialog, response):
        """Configure the message box with custom styles and buttons."""
        dialog.setStyleSheet("""
            QMessageBox {
                background-color: #fff;
                font-size: 18px;
            }
        """)
        dialog.setWindowTitle(response[1])
        dialog.setIconPixmap(self.create_warning_icon())
        dialog.setText(response[2])
        dialog.setInformativeText(response[3])
        self.setup_buttons(dialog)
        self.connect_buttons(dialog, response[4])

    def create_warning_icon(self):
        """Create and return a warning icon."""
        warning_icon = icon('fa.exclamation-triangle', color='red')
        return warning_icon.pixmap(40)

    def setup_buttons(self, dialog):
        """Style and configure buttons in the message box."""
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        dialog.button(QMessageBox.Ok).setText("Solucionar")
        dialog.button(QMessageBox.Cancel).setText("Cerrar")
        button_style = """
            font-size: 18px;
            background-color:
                qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #E1E1E1, stop:1 #FFFFFF);
            border: 1px solid #888888;
            border-radius: 10px;
            padding: 5px;
            margin: 5px;
        """
        dialog.button(QMessageBox.Ok).setStyleSheet(button_style)
        dialog.button(QMessageBox.Cancel).setStyleSheet(button_style)

    def connect_buttons(self, dialog, url):
        """Connect button actions to their respective slots."""
        dialog.button(QMessageBox.Ok).clicked.connect(lambda: self.solve_issue(url))
        dialog.button(QMessageBox.Cancel).clicked.connect(dialog.close)

    def solve_issue(self, url):
        """Open the given URL and exit the application."""
        webbrowser.open(url)
        sys.exit()