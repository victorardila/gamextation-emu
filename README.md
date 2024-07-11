# GameXtation EMU🎮

![icon](https://github.com/Valfonsoardila10/GameXtation-EMU/assets/106699036/e9898358-4a60-482d-9f2a-e04e19d4383d)

## Pasos de instalacion de proyecto

## 1. Crear y Activar el entorno virtual

El entorno virtual se puede crear con venv
- Ejecute el siguiente comando para crear el entorno virtual e instalar dependencias:

### Instalacion en windows
```bash
python -m venv .venv
```
- Activar el entorno virtual:
```bash
.venv/bin/activate
```

- Desactivar el entorno virtual:
```bash
# muevete a la carpeta .venv
cd .venv/Scripts
# ejecuta el archivo deactivate
./deactivate
```
- Regenerar el archivo de bloqueo
```bash
poetry lock
```

### Instalacion de linux
```bash
python3 -m venv .venv
```
- Activar el entorno virtual:
```bash
source .venv/bin/activate
```

- Desactivar el entorno virtual:
```bash
deactivate
```

- Regenerar el archivo de bloqueo
```bash
poetry lock
```
