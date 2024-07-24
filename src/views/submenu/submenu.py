from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

class SubMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.InitGUI()
        
    BG_COLOR_DARK = (
        "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
        "stop:0 rgba(34, 34, 34, 255), stop:0.5 rgba(40, 40, 40, 255), "
        "stop:0.75 rgba(50, 50, 50, 255), stop:1 rgba(34, 34, 34, 255));"
    )
    BG_COLOR_LIGHT = (
        "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
        "stop:0.026178 rgba(249, 135, 11, 255), stop:0.219895 rgba(247, 134, 12, 255), "
        "stop:0.424084 rgba(241, 139, 11, 255), stop:0.715789 rgba(233, 150, 10, 255), "
        "stop:0.826316 rgba(232, 155, 13, 255), stop:1 rgba(235, 154, 11, 255));"
    )
    
    def InitGUI(self):
        loadUi("src/views/submenu/submenu.ui", self)
        