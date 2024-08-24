from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import signal
import sys
import subprocess
import time


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, window_to_close):
        super().__init__()
        self.window_to_close = window_to_close

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Change detected in: {event.src_path}")
            self.terminate_application()

    def terminate_application(self):
        """Cierra la ventana especificada."""
        if self.window_to_close:
            self.window_to_close.close()
            self.window_to_close = None  # Opcional: liberando la referencia
        else:
            print("No window to close.")

        # Aquí puedes optar por cerrar el proceso completo si es necesario
        sys.exit()  # Esto finalizará la aplicación completa


def start_watching(root_path, window_to_close):
    event_handler = ChangeHandler(window_to_close)
    observer = Observer()
    observer.schedule(event_handler, root_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
