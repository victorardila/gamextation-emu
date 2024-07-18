import subprocess
import platform

# Gestionar las configuraciones de los entornos como docker, desarrollo, producción, etc.
class ContainerPlatform:
    def __init__(self):
        super().__init__()
    
    # Verificar la instalación de Docker según el sistema operativo
    def checkDocker():
        supported_systems = {"Windows", "Linux", "Darwin"}  # Sistemas operativos soportados
        system = platform.system()
        
        if system not in supported_systems:
            return False
        
        try:
            subprocess.run(["docker", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            title = "Error falta una dependencia"
            text = "Docker no está instalado en el sistema operativo."
            informative_text = "Por favor, instale Docker para poder ejecutar la aplicación."
            # retornar un False y los mensajes de error
            return True, title, text, informative_text # Debe retornar False para que se muestre el mensaje de error
        
        return True
    
    # Verificar docker esta corriendo
    def checkDockerRunning():
        try:
            subprocess.run(["docker", "info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            title = "Error al ejecutar Docker"
            text = "Docker no está en ejecución."
            informative_text = "Por favor, inicie Docker para poder ejecutar la aplicación."
            # retornar un False y los mensajes de error
            return False, title, text, informative_text
        return True
    
    # Verificar si el contenedor está en ejecución
    def checkContainerRunning():
        try:
            subprocess.run(["docker", "ps"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            title = "Error al ejecutar Docker"
            text = "No hay contenedores en ejecución."
            informative_text = "Por favor, inicie un contenedor para poder ejecutar la aplicación."
            # retornar un False y los mensajes de error
            return False, title, text, informative_text
        return True
    
    # Verificar si docker esta detenido
    def checkDockerStopped():
        try:
            subprocess.run(["docker", "info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            title = "Error al ejecutar Docker"
            text = "Docker está detenido."
            informative_text = "Por favor, inicie Docker para poder ejecutar la aplicación."
            # retornar un False y los mensajes de error
            return False, title, text, informative_text
        return True
    