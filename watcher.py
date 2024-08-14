from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time
import sys
import os
import signal
import psutil


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script_to_run):
        super().__init__()
        self.script_to_run = script_to_run
        self.processes = []

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"{event.src_path} has been modified. Restarting application...")
            # Cerrar procesos existentes
            self.terminate_processes()
            # Iniciar el nuevo proceso
            self.processes = [subprocess.Popen([sys.executable, self.script_to_run])]

    def terminate_processes(self):
        for proc in self.processes:
            try:
                proc.send_signal(signal.SIGTERM)  # Envía señal de terminación
                proc.wait(timeout=5)  # Espera a que el proceso se cierre
            except subprocess.TimeoutExpired:
                proc.kill()  # Fuerza la terminación si el proceso no responde
                proc.wait()  # Asegúrate de que el proceso se cierre

    def terminate_all_pyqt_processes(self):
        """Cierra todos los procesos PyQt en ejecución."""
        for proc in psutil.process_iter(["pid", "name"]):
            if proc.info["name"] == "python":
                try:
                    for child in proc.children(recursive=True):
                        if "main.py" in child.cmdline():
                            child.terminate()  # Envía señal de terminación
                            child.wait(timeout=5)  # Espera a que el proceso se cierre
                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    pass


def start_watching(script_to_run, watch_dir="."):
    event_handler = ChangeHandler(script_to_run)
    observer = Observer()
    observer.schedule(event_handler, path=watch_dir, recursive=True)
    observer.start()
    print(f"Watching for changes in {watch_dir}...")
    try:
        while True:
            time.sleep(1)
            event_handler.terminate_all_pyqt_processes()  # Asegúrate de cerrar procesos antiguos
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
