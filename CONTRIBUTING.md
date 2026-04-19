### Guía de Contribución

#### 1. Instalación y configuración

Sigue estos pasos para preparar el entorno de Atmos-App en tu máquina local:

1. **Clonar el repositorio**:

    ```bash
    git clone https://github.com/JCRbit/atmos-app.git
    cd atmos-app
    ```

2. **Crear y activar el entorno virtual (`venv`)**:

    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En Linux/Mac:
    source venv/bin/activate
    ```

3. **Instalar dependencias**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Verificar la instalación**. Ejecuta la batería de tests inicial para confirmar que todo está en orden:

    ```bash
    pytest
    ```

#### 2. Flujo de trabajo

1. **Fork** del proyecto.
2. Crea una rama: `git checkout -b feat/nombre-de-tu-mejora`.
3. Realiza tus cambios y asegúrate de que `pytest` no dé errores.
4. Abre un **Pull Request** detallando qué problema resuelves.

#### 3. Convenciones de mensajes de commit

Para mantener un historial de cambios limpio y legible, vamos a utilizar la convención de *Conventional Commits*. Cada mensaje de commit debe seguir la estructura: `<tipo>(<alcance_opcional>): <descripción breve en minúsculas>`.

1. **Tipos de commits**:
   * **`feat`**: Nueva funcionalidad.
   * **`fix`**: Corrección de errores.
   * **`docs`**: Cambios en la documentación.
   * **`refactor`**: Mejora de código (sin cambiar lógica ni añadir funciones).
   * **`test`**: Añadir o modificar pruebas unitarias.
   * **`chore`**: Tareas de mantenimiento (dependencias, `.gitignore`).

2. **Alcances**. Utiliza estos alcances para identificar qué módulo estás modificando:
    * **`io`**: Cambios en io_manager.py o persistencia JSON.
    * **`valid`**: Lógica en `validation.py` (tipado, rangos, fechas, duplicados).
    * **`alert`**: Sistema de alertas en `alerts.py`.
    * **`ui`**: Interfaz de usuario y menús.
    * **`tests`**: pruebas unitarias.
    * **`log`**: Trazabilidad y `logger.py`.
    * **`assets`**: imágenes, iconos y recursos estáticos.
    * **`setup`**: dependencias, `.gitignore`, requirements.

3. **Recomendaciones y ejemplos** de flujo de trabajo recomendado.

   * *Pequeños commits*: En lugar de un commit gigante "terminado el módulo de datos", haz varios commits pequeños.
   * *Mensajes claros*: Evita mensajes como "arreglado", "cambios" o "uops".
   * *Cambios generales*: No usar ningún alcance específico.
   * *Ejemplos*:
     * Nuevas funcionalidades (feat):
       * `feat(validation): añadir validación de ráfagas de viento en validation.py`
       * `feat(log): implementar exportación de logs a formato CSV`
     * Corrección de errores (fix):
       * `fix(io): corregir error de lectura en io_manager cuando el json está vacío`
       * `fix(alert): ajustar umbral de alerta por calor extremo de 40 a 42 grados`
     * Documentación (docs):
       * `docs: actualizar instrucciones de instalación en el README`
       * `docs: añadir ejemplos de uso en la guía de usuario`
     * Refactorización (refactor):
       * `refactor(io): optimizar bucle de búsqueda en io_manager.py`
     * Pruebas (test):
       * `test: añadir batería de pruebas para sensores de humedad`
       * `test: corregir falsos positivos en test_alertas.py`
     * Tarea (chore):
       * `chore(setup): ignorar la carpeta .vscode y archivos .log en .gitignore`
       * `chore(setup): actualizar pandas a la versión 2.2.0`

#### 4. Estándares de código

- **Idioma**: Código y lógica en español (variables, funciones, comentarios).
- **Estilo**: PEP 8. Usa 4 espacios para indentación.
- **Tipado**: Es obligatorio usar Type Hints.
    Ejemplo:

    ```python
    def registrar(dato: dict) -> bool:
    ```
