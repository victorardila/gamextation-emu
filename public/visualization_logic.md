# Logica de Visualizacion

Este proyecto es desarrollado en el diseñador de interfaces mas potente que tiene la tecnologia en escritorio Pyqt

- Se arranca en un punto de origin llamado app.py la cual al hacer las diferentes validaciones de inicio redirigirá al siguiente flujo:

## `Flujo de Ejecución`

```diff
    
OriginLogic(trigger) 
+-------------------+
|      app.py       |
+-------------------+
         ↓
         ↓
   Flujo ↓          (Load Windows)
         ↓         
         ↓
 QMainWindow(Window)              QMainWindow(Window)
+-------------------+   Flujo   +---------------------+
|   animation.ui    | → → → → → |  main_container.ui  | 
+-------------------+           +---------------------+
                                    ↓        ▼
                                    ↓  QWidget(Views)                 (Load Views)
                                    ↓        │   ┌──────────────┐
                                    │→ → → → │ ► | game_load.ui |
                       Flujo triple ↓        |   └──────────────┘                     
                                    ↓      Ramas ┌──────────────┐                       ┌────────────────────┐
                                    │→ → → → │ ► | main_menu.ui | → → → QWidget(Overlay)|   overlay_menu.ui  |
                                    ↓        │   └──────────────┘                       └────────────────────┘
                                    ↓        │   ┌──────────────┐                        
                                    └ → → → →└ ► |  submenu.ui  |                       
                                                 └──────────────┘  
                                                         ↓            (Load Modules)
                                                         ↓
                                                         ↓
                                                 QWidget(Overlay)
                                               ┌────────────────────┐
                                               | overlay_submenu.ui |
                                               └────────────────────┘
                                                         ▼
                                                  QWidget(Modules)    (Load Microservices)
                                                         |
                                                         | ► Roms
                                                         | ► Consoles
                                                         | ► Store
                                                         | ► Media
                                                         | ► User
                                                         | ► Settings
                                                         | ► Optimize
                                                         | ► Update
                                                         | ► Creator
                                                         └ ► About
```
## `Descripcion de flujo`
- **`app.py:`** El punto de inicio del flujo, se encarga de la lógica inicial y las validaciones.
- **`QMainWindow (animation.ui):`** Carga el diseño de **animation.ui**.
- **`QMainWindow (main_container.ui):`** Carga el diseño de **main_container.ui** y dentro de este se encuentran las vistas.
- **`Views:`** Dentro de **main_container.ui**, se gestionan varias vistas:
  - **`game_load.ui:`** Vista para cargar juegos.
  - **`main_menu.ui:`** Vista para el menú principal.
  - **`submenu.ui:`** Vista para los submenús.
- **`Overlays y Módulos:`**
  - **`overlay_menu.ui:`** Carga sobre **main_menu.ui**.
  - **`overlay_submenu.ui:`** Carga sobre **submenu.ui**.
  - **`Modules:`** Módulos adicionales que se cargan en el flujo de ejecución.