from PyQt5.QtWidgets import QWidget


class GameLoaded(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("GameXtation")
        self.setGeometry(100, 100, 800, 600)
        self.show()
