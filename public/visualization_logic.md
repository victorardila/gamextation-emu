# Logica de Visualizacion

Este proyecto es desarrollado en el diseñador de interfaces mas potente que tiene la tecnologia en escritorio Pyqt

- Se arranca en un punto de origin llamado app.py la cual al hacer las diferentes validaciones de inicio redirigirá al siguiente flujo:

## Flujo de Ejecución

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
                                    ↓  QWidget(Views)              (Load Views)
                                    ↓        │   ┌──────────────┐
                                    │→ → → → │ ► | game_load.ui |
                       Flujo triple ↓        |   └──────────────┘        
                                    ↓      Ramas ┌──────────────┐                   ┌────────────────────┐
                                    │→ → → → │ ► | main_menu.ui | → QWidget(Overlay)|   overlay_menu.ui  |
                                    ↓        │   └──────────────┘                   └────────────────────┘
                                    ↓        │   ┌──────────────┐                   
                                    └ → → → →└ ► |  submenu.ui  |  
                                                 └──────────────┘  
                                                        ↓           (Load Modules)
                                                 QWidget(Overlay)
                                               ┌────────────────────┐
                                               | overlay_submenu.ui |
                                               └────────────────────┘
```