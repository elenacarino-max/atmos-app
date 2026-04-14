import os
import json
from typing import List, Dict, Any
from logger import log_info, log_error, log_warning

# Ruta al archivo json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "data.json")

def cargar_datos() -> List[Dict[str, Any]]:
    """
    Carga el histórico de registros climáticos desde el almacenamiento persistente.

    Esta función lee el archivo JSON definido en DATA_PATH y garantiza la continuidad 
    de la aplicación: si el archivo no existe o su contenido no es un JSON válido, 
    devuelve una lista vacía en lugar de interrumpir la ejecución del programa.

    Returns:
        List[Dict[str, Any]]: Lista de diccionarios con todos los registros 
            históricos. Devuelve una lista vacía si el archivo no existe, está vacío 
            o está dañado.

    Raises:
        No lanza excepciones. Los errores de E/S y de decodificación de JSON 
        son capturados internamente para asegurar la estabilidad del sistema.
    """
    log_info(f"Intentando cargar datos desde: {DATA_PATH}")

    if not os.path.exists(DATA_PATH):
        return []

    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            log_info(f"Carga exitosa. Se han recuperado {len(datos)} registros.")
            return datos
    except (json.JSONDecodeError, FileNotFoundError):
        # Manejo de error si el archivo está dañado o no existe
        log_error(f"Error al leer el archivo JSON (posible archivo corrupto): {e}")
        return []

def guardar_registro(nuevo_registro: Dict[str, Any], datos: List[Dict[str, Any]]) -> bool:
    """
    Añade un nuevo registro al archivo JSON y persiste los cambios.

    Args:
        nuevo_registro (Dict[str, Any]): Diccionario con los datos validados 
            (fecha, zona, temperatura, humedad, viento, alerta).
        datos (List[Dict[str, Any]]): Lista de diccionarios que representa 
            la base de datos actual cargada en memoria.

    Returns:
        bool: True si el registro se guardó con éxito. False si ocurrió un error de E/S (permisos, 
            disco lleno, ruta no encontrada).
    """
    datos.append(nuevo_registro)

    try:
        # Asegurar que la carpeta contenedora exista
        directorio = os.path.dirname(DATA_PATH)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
            log_info(f"Creado directorio inexistente: {directorio}")

        # Guardar manteniendo la estructura original 
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
            log_info(f"Registro guardado correctamente para la zona '{nuevo_registro.get('zona_registro')}'")
        return True
    except Exception:
        # Gestión de errores de escritura
        log_error(f"Fallo crítico al intentar persistir los datos: {e}")
        return False