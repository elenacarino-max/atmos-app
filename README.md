ATMOS APP
ATMOS APP es una aplicación que permite a los ayuntamientos y organismos públicos establecer protocolos de actuación y dar respuesta inmediata a alarmas ante sucesos meteorológicos anómalos

Estructura del proyecto: 
    {bash}
    atmos-app/
    │
    ├── src/                     # Código fuente del núcleo (Modularidad)
    │   ├── main.py              # Orquestador
    │   ├── io_manager.py        # Gestión del archivo JSON
    │   ├── validation.py        # Validación de rangos y tipos
    │   ├── alerts.py            # Logica de alertas
    │   ├── logger.py            # Configuracion de logs
    │   └── utils.py             # Utilidades
    │
    ├── data/
    │   └── data.json            # Base de datos
    |
    ├── tests/                   # Pruebas unitarias
    |   ├── test_rangos.py
    |   ├── test_duplicados.py
    │   └── test_alertas.py
    |
    ├── logs/
    │   └── sistema.log          # Archivo de trazabilidad 
    |
    ├── scripts/
    │   └── data_generator.py    # Generador de datos sintéticos
    │
    ├── docs/                    # Documentación y Recursos Visuales
    │   └── images/
    │       ├── logos\
    │       |   └── logo.png
    │       ├── esquema_arq.png  # Diagrama de flujo/arquitectura del sistema
    │       └── screenshots/     # Capturas de la App para el README
    │           ├──
    │           └──
    │
    |
    ├── .gitignore               # Archivos excluidos (venv, __pycache__, logs)
    ├── requirements.txt         # Dependencias (fastapi, uvicorn, pytest, pydantic)
    └── README.md                # Guía completa con imágenes y logo


Cómo usarlo en local: 

No necesitas instalar nada. Sigue los siguientes pasos: 
1.- Clona o descarga el repositorio
    git clone https://github.com/JCRbit/atmos-app.git

O descarga el ZIP desde GitHub y descomprímelo

2.- Abre la carpeta del proyecto: 
    cd atmos-app

3.- Aparece el menú principal 
