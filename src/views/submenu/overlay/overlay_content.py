from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QTimer
from PyQt5.uic import loadUi
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap, QPainter, QColor
from PyQt5.QtGui import QEnterEvent, QMouseEvent
from src.components.optimizer.graphics_optimizer import GraphicsOptimizer
from src.modules.roms.roms import Roms
from src.modules.consoles.consoles import Consoles
from src.modules.store.store import Store
from src.modules.media.media import Media
from src.modules.user.user import User
from src.modules.settings.settings import Settings
from src.modules.optimize.optimize import Optimize
from src.modules.update.update import Update
from src.modules.creator.creator import Creator
from src.modules.about.about import About

class OverlayContent(QWidget):
    theme_changed = pyqtSignal()  # Señal para indicar el cambio de tema
    menu_return_clicked = pyqtSignal()
    menu_exit_clicked = pyqtSignal()
    SVG_CREDITS = "src/assets/svg/icon.svg"
    
    # Arreglo de modulos
    MODULES = {
        "Juegos": Roms,
        "Consola": Consoles,
        "Tienda": Store,
        "Media": Media,
        "Usuario": User,
        "Configuraciones": Settings,
        "Optimizar": Optimize,
        "Actualizaciones": Update,
        "Creador": Creator,
        "Acerca": About,
    }
    
    def __init__(self):
        super().__init__()
        self.init_main_menu()
        self.sidebar_open = False  # Estado inicial del sidebar
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.close_sidebar_if_needed)
        
        # Conectar los botones a la señal
        self.button_return.clicked.connect(self.emit_menu_return)
        self.button_exit.clicked.connect(self.emit_menu_exit)
        
        # Instancia de GraphicsOptimizer
        self.graphics_optimizer = GraphicsOptimizer()
        self.graphics_optimizer.setParent(self)
        self.graphics_optimizer.setVisible(False)  # Inicialmente oculto
        self.graphics_optimizer_timer = QTimer()
        self.graphics_optimizer_timer.setSingleShot(True)
        self.graphics_optimizer_timer.timeout.connect(self.hide_graphics_optimizer)

    def init_main_menu(self):
        """Load the UI and initialize main menu."""
        loadUi("src/views/submenu/overlay/overlay_submenu.ui", self)
        self.load_module()
        self.setStyleSheet("background-color: transparent;")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.apply_sidebar_styles()
        self.button_menu_bar.clicked.connect(self.toggle_sidebar)  # Conectar el botón al método
        self.button_optimize.clicked.connect(self.show_graphics_optimizer)  # Conectar el botón al método

        # Conectar eventos de entrada del mouse
        self.button_menu_bar.installEventFilter(self)
        self.sidebar_menu.installEventFilter(self)
    
    def clear_layout(self, layout):
        """Helper function to clear a layout."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()

    def load_module(self, message=None):
        """Load the module for the main menu."""
        if not message:
            return

        # Encontrar la clave del módulo basado en el mensaje
        key = next((k for k in self.MODULES if k.lower() in message.lower()), None)
        if key is None:
            print(f"No se encontró ningún módulo correspondiente al mensaje: {message}")
            return  # No se encontró el módulo correspondiente

        # Crear una instancia del módulo
        self.module = self.MODULES[key]()
        
        # Conectar la señal back_clicked del módulo cargado a la señal menu_return_clicked
        self.module.back_clicked.connect(self.emit_menu_return)

        # Si ya hay un layout, limpiarlo
        if self.content_menu.layout() is not None:
            self.clear_layout(self.content_menu.layout())
        else:
            # Crear un layout si no hay uno existente
            layout = QVBoxLayout(self.content_menu)
            self.content_menu.setLayout(layout)

        # Agregar el módulo al layout
        self.content_menu.layout().addWidget(self.module)
        self.apply_content_styles()
        
    def apply_content_styles(self):
        self.content_menu.setStyleSheet("background-color: transparent;")

    def apply_sidebar_styles(self):
        """Apply styles to the sidebar and its elements."""
        custom_font = self.load_custom_font(
            font_path="src/assets/font/ratchet-clank-psp.ttf",
            font_size=24,
            fallback_font="Arial",
            fallback_size=18
        )
        
        # Apply sidebar styles
        self.sidebar_menu.setStyleSheet("background-color: rgba(0, 0, 0, 0.2);")
        self.logo_menu_content.setStyleSheet("background-color: transparent;")
        
        # Set logo with customized color and size
        self.logo.setPixmap(
            self.colorize_svg(self.SVG_CREDITS, QColor('white'), QSize(80, 80))
        )
        
        self.label_logo_menu.setStyleSheet("background-color: transparent; color: white;")
        
        # Apply FontAwesome icons to buttons
        self.apply_button_styles()
        
        # Apply custom font to all widgets in the sidebar
        self.set_custom_font_to_sidebar_widgets(custom_font)
        
        # Initialize sidebar width
        self.sidebar_menu.setMaximumWidth(0)
        self.sidebar_menu.setMinimumWidth(0)
             
    def load_custom_font(self, font_path, font_size, fallback_font, fallback_size):
        """Load a custom font, fallback to default if not available."""
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            return QFont(font_family, font_size)
        return QFont(fallback_font, fallback_size)
        
    def colorize_svg(self, svg_path, color, size):
        """Colorize an SVG file and return it as a QPixmap."""
        pixmap = QPixmap(svg_path)
        pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Apply color using QPainter
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()

        return pixmap
    
    def apply_button_styles(self):
        """Apply FontAwesome icon styles to buttons."""
        self.button_menu_bar.style('fa.angle-right', QSize(32, 32), "Desplegar", 'white')
        self.button_return.style('fa.home', QSize(32, 32), "Volver al menu", 'white')
        self.button_optimize.style('fa.leaf', QSize(32, 32), "Optimizar", 'white')
        self.button_exit.style('fa.sign-out', QSize(32, 32), "Salir", 'white')

    def set_custom_font_to_sidebar_widgets(self, custom_font):
        """Apply custom font to all widgets within the sidebar."""
        for widget in self.sidebar_menu.findChildren(QWidget):
            widget.setFont(custom_font)
    
    def toggle_sidebar(self):
        """Toggle the sidebar between open and closed states."""
        if self.sidebar_open:
            # Close the sidebar
            self.sidebar_menu.setMaximumWidth(0)
            self.sidebar_menu.setMinimumWidth(0)
            self.button_menu_bar.style('fa.angle-right', QSize(32, 32), "Desplegar", 'white')
            self.timer.stop()  # Detener el temporizador si se cierra el sidebar
        else:
            # Open the sidebar
            self.sidebar_menu.setMaximumWidth(300)
            self.sidebar_menu.setMinimumWidth(300)
            self.button_menu_bar.style('fa.angle-left', QSize(32, 32), "Cerrar", 'white')
            self.start_auto_close_timer()  # Iniciar el temporizador para cerrar automáticamente

        # Toggle the sidebar state
        self.sidebar_open = not self.sidebar_open

    def eventFilter(self, obj, event):
        """Handle events for the button_menu_bar and sidebar_menu, including hover."""
        if obj == self.button_menu_bar:
            if event.type() == QEnterEvent.Enter:
                # Handle hover event
                self.toggle_sidebar()
                self.set_button_menu_bar_opacity(1.0)  # Set opacity to 100% when hovered
            elif event.type() == QMouseEvent.MouseButtonPress:
                # Handle click event
                self.toggle_sidebar()
            elif event.type() == QMouseEvent.Leave:
                # Set opacity to 50% when not hovered
                self.set_button_menu_bar_opacity(0.5)
        elif obj == self.sidebar_menu:
            if event.type() == QEnterEvent.Enter:
                # Reset the timer if mouse enters the sidebar
                self.timer.stop()
            elif event.type() == QMouseEvent.Leave:
                # Start the timer when mouse leaves the sidebar
                self.start_auto_close_timer()
        return super().eventFilter(obj, event)
    
    def start_auto_close_timer(self):
        """Start the auto-close timer for the sidebar."""
        self.timer.start(2000)  # 5000 ms = 5 seconds
    
    def close_sidebar_if_needed(self):
        """Close the sidebar if it's open and the timer expires."""
        if self.sidebar_open:
            self.toggle_sidebar()
    
    def set_button_menu_bar_opacity(self, opacity):
        """Set the opacity of the button_menu_bar."""
        self.button_menu_bar.setWindowOpacity(opacity)
    
    def emit_menu_return(self):
        self.menu_return_clicked.emit()
    
    def emit_menu_exit(self):
        self.menu_exit_clicked.emit()

    def show_graphics_optimizer(self):
        """Mostrar el GraphicsOptimizer en la esquina superior derecha sobre el content_menu."""
        content_menu_rect = self.content_menu.rect()
        widget_rect = self.graphics_optimizer.rect()
        
        # Configurar la geometría del GraphicsOptimizer
        self.graphics_optimizer.setGeometry(
            self.content_menu.width() - widget_rect.width() - 0,  # 20 píxeles desde el borde derecho
            50,  # 30 píxeles desde el borde superior
            widget_rect.width(),
            widget_rect.height()
        )
        
        self.graphics_optimizer.setVisible(True)
        self.graphics_optimizer_timer.start(10000)  # Ocultar después de 10 segundos

    def hide_graphics_optimizer(self):
        """Ocultar el GraphicsOptimizer."""
        self.graphics_optimizer.setVisible(False)
        # enviar una señal al modulo Roms que se ha ocultado el GraphicsOptimizer
        self.module.optimizer_hidden.emit()
        
