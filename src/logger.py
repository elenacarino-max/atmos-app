import logging
import os

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")
LOG_FILE = os.path.join(LOG_DIR, "atmos_app.log")

def configurar_logger():
    """
    Configura el sistema de logging para que escriba en un archivo y
    opcionalmente en la consola.
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8'
    )

def log_info(mensaje):
    """Eventos normales: inicio de app, navegación por menús."""
    logging.info(mensaje)

def log_warning(mensaje):
    """Alertas: duplicados detectados, valores en el límite de rango."""
    logging.warning(mensaje)

def log_error(mensaje):
    """Errores: fallos al leer/escribir archivos, errores de conversión."""
    logging.error(mensaje)

def log_critico(mensaje):
    """Fallos graves: la aplicación no puede continuar."""
    logging.critical(mensaje)
    