# ATMOS APP

## 📌 Descripción

**ATMOS APP** es una aplicación desarrollada en Python para digitalizar, validar y analizar datos climáticos.  
Permite a los ayuntamientos y organismos públicos establecer protocolos de actuación y dar respuesta inmediata a alarmas ante sucesos meteorológicos anómalos.

---

## 🎯 Objetivo del proyecto

Resolver el problema del retraso y errores en la recogida de datos climáticos derivados de la no digitalización:

* Centraliza la información  
* Valida datos automáticamente  
* Detecta situaciones de riesgo  
* Mantiene el histórico digital  
* Muestra el histórico gráficamente para mejor comprensión  

---

## 🛠️ Tecnologías utilizadas

* Python 3  
* JSON (persistencia de datos)  
* Git / GitHub  

---

## 🧠 Estructura del proyecto

```bash
atmos-app/
│
├── src/                     # Código fuente del núcleo (Modularidad)
│   ├── main.py              # Orquestador
│   ├── io_manager.py        # Gestión del archivo JSON
│   ├── validation.py        # Validación de rangos y tipos
│   ├── alerts.py            # Lógica de alertas
│   ├── logger.py            # Configuración de logs
│   └── utils.py             # Utilidades
│
├── data/
│   └── data.json            # Base de datos
│
├── tests/                   # Pruebas unitarias
│   ├── test_rangos.py
│   ├── test_duplicados.py
│   └── test_alertas.py
│
├── logs/
│   └── sistema.log          # Archivo de trazabilidad 
│
├── scripts/
│   └── data_generator.py    # Generador de datos sintéticos
│
├── docs/                    # Documentación y recursos visuales
│   └── images/
│       ├── logos/
│       │   └── logo.png
│       ├── esquema_arq.png
│       └── screenshots/
│
├── .gitignore               # Archivos excluidos
├── requirements.txt         # Dependencias
└── README.md                # Documentación principal
```

### Cómo usarlo en local:

Sigue los siguientes pasos para configurar el entorno y ejecutar la aplicación: 

1. **Clona o descarga el repositorio:** `git clone https://github.com/JCRbit/atmos-app.git`  
   *O descarga el ZIP desde GitHub y descomprímelo.*

2. **Abre la carpeta del proyecto:** `cd atmos-app`

3. **Instala las librerías necesarias:** `pip install -r requirements.txt`

4. **Ejecuta la aplicación:** `python main.py`

---

## ⚙️ Funcionalidades principales

### 🧭 Menú principal

```text
 Iniciando Atmos® ...
 Cargando aplicación ...
╔════════════════════════════════════════════════╗
║      ATMOS: GESTIÓN METEOROLÓGICA URBANA       ║
╚════════════════════════════════════════════════╝
 [1] Registrar nueva medición
 [2] Consultar registro meteorológico por zona 
 [3] Ver histórico 
 [4] Ver gráficos
 [X] Salir
--------------------------------------------------
Selecciona una opción: 
```

### 📝 Registro de datos

Permite introducir:
   * Fecha
   * Zona
   * Temperatura (°C)
   * Humedad (%)
   * Viento (km/h)

### ✅ Validaciones

* Tipos de datos correctos
* Rangos lógicos:
    * **Rango de temperatura** * Valores normales : -8 <= temperatura <= 40 
        * Dato incorrecto: Temperatura < -15 or Temperatura > 50
    * **Rango de viento**
        * Valores normales: 1 < velocidad < 70 km/h 
        * Valores incorrectos: velocidad_viento >130 km/h o velocidad_viento <= 0
    * **Rango de Humedad:** * Dato erróneo es cualquier dato que no sea entre 0 y 100 

### 🚨 Sistema de alertas

Detecta automáticamente:
    * **Alerta de Temperatura:** Temperatura < -8 or Temperatura > 40
    * **Alerta de Viento:** velocidad_viento > 71 km/h or velocidad_viento < 129 km/h
    * **Alerta de Humedad:** 0 < Humedad <= 20 and 70 < humedad <= 100

### 📂 Persistencia de datos

* Los datos se almacenan en un JSON para la lectura y escritura del archivo.
* No se sobrescriben registros existentes.

### 🔎 Consulta de datos

* Filtrado y consulta por zona
* Visualización gráfica del histórico

### 🧪 Tests

Se han implementado tests unitarios para asegurar la fiabilidad de las validaciones y el sistema de alertas.

Para ejecutar los tests, utiliza el siguiente comando:

```bash
pytest
```

**Resultados de la última ejecución:**

```text
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.0.2, pluggy-1.6.0
collected 19 items

tests\test_alertas.py ....                                               [ 21%]
tests\test_duplicados.py .....                                           [ 47%]
tests\test_rangos.py ..........                                          [100%]

============================= 19 passed in 0.08s ==============================
```

### ⚠️ Manejo de errores

  * Validación de inputs del usuario
  * Uso de `try/except`
  * Mensajes claros para el que el usuario pueda corregir el error

### 👥 Trabajo en equipo

  * Uso de Git con commits descriptivos
  * Uso de Trello para la organización de las tareas del proyecto
  * Desglose de tareas por funcionalidad
  * Trabajo en entorno virtual con una rama master y ramas de desarrollo

### Mejoras futuras

  * Interfaz gráfica (GUI)
  * Versión web
  * Mejora del sistema de autenticación (hashing de contraseñas)
