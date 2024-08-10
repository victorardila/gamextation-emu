from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPainter
from PyQt5.QtCore import Qt, QSize, QEvent
from PyQt5.QtSvg import QSvgRenderer

class RadioButtonIcon(QRadioButton):
    gradient_color_selection_dark = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(173, 216, 230, 10), stop:1 rgba(0, 255, 127, 255));"

    def __init__(self, icon_index=0, parent=None):
        super().__init__(parent)
        self.icon_index = icon_index
        self.original_color = QColor("white")  # Color por defecto
        self.hover_color = QColor("black")  # Color al hacer hover
        self.setup_ui()
        self.installEventFilter(self)  # Instalar el filtro de eventos
    
    def setup_ui(self):
        # Configura el estilo para ocultar el indicador predeterminado
        self.setStyleSheet("QRadioButton::indicator {width: 0px; height: 0px;}")
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)
        self.setChecked(False)  # El valor predeterminado será no seleccionado
        self.setAutoExclusive(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setAttribute(Qt.WA_Hover)  # Asegura que el evento hover esté habilitado
    
    def style(self, svg, size=QSize(24, 24), tooltip="", color=QColor("white"), hover_color=QColor("black")):
        """
        Aplica el ícono SVG, establece el tamaño del ícono, y configura el tooltip.
        
        :param svg: Ruta del archivo SVG.
        :param size: Tamaño del ícono (QSize).
        :param tooltip: Texto del tooltip.
        :param color: Color para el ícono SVG en estado normal.
        :param hover_color: Color para el ícono SVG al hacer hover.
        """
        self.original_color = color
        self.hover_color = hover_color
        
        # Cargar el contenido del SVG
        renderer = QSvgRenderer(svg)
        
        # Crear un QPixmap para renderizar el SVG
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)  # Asegurar fondo transparente
        
        # Crear un QPainter para pintar en el QPixmap
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        # Cambiar el color del SVG
        self.apply_color_to_svg(pixmap, self.original_color)
        
        # Crear un QIcon a partir del QPixmap
        icon = QIcon(pixmap)
        self.setIcon(icon)
        self.setIconSize(size)
        
        # Configurar el tooltip si se proporciona
        if tooltip:
            self.setToolTip(tooltip)
    
    def apply_color_to_svg(self, pixmap, color):
        """
        Cambia el color del ícono SVG en el QPixmap.
        
        :param pixmap: QPixmap que contiene el ícono SVG.
        :param color: Color para aplicar al SVG.
        """
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            self.set_hover_stylesheet()
        elif event.type() == QEvent.Leave:
            self.set_default_stylesheet()
        return super().eventFilter(obj, event)
        
    def set_hover_stylesheet(self):
        self.setStyleSheet(
            f"""
            QRadioButton {{
                border: none;
                border-radius: 10px;
                background: {self.gradient_color_selection_dark};
                color: white;
                font-size: 24px;
                font-weight: bold;
            }}
            QRadioButton::indicator {{
                width: 10px;
                height: 10px;
                color: white;
            }}
            {self.tooltip_stylesheet()}
            """
        )

    def set_default_stylesheet(self):
        self.setStyleSheet(self.default_stylesheet() + self.tooltip_stylesheet())
    
    def tooltip_stylesheet(self):
        """
        Retorna el CSS para el tooltip.
        """
        return "QRadioButton::tooltip { color: black; }"

    def default_stylesheet(self):
        """
        Retorna el CSS por defecto para el QRadioButton.
        """
        return "QRadioButton { border: none; border-radius: 10px; background: transparent; color: white; font-size: 24px; font-weight: normal; }"