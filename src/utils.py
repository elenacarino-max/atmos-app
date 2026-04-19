import sys
import subprocess
import platform
from datetime import datetime
from logger import log_warning

def limpiar_pantalla():
    """
    Limpia la consola dependiendo del sistema operativo.
    """
    try:
        print("\033[H\033[2J", end="", flush=True)

        # En caso de que el código ANSII no funcione
        # Definir el comando según el sistema operativo
        es_windows = platform.system() == "Windows"
        comando = "cls" if es_windows else "clear"
        subprocess.run(comando, shell=es_windows, check=True)
        
    except Exception as e:
        log_warning(f"No se pudo limpiar la pantalla: {e}")
        print("\033[H\033[2J", end="")

def imprimir_encabezado_h1(titulo):
    """
    Imprime un encabezado para el menú principal de la consola.
    """
    ancho = 50
    print("╔" + "═" * (ancho - 2) + "╗")
    print(f"║{titulo.center(ancho - 2)}║")
    print("╚" + "═" * (ancho - 2) + "╝")

def imprimir_encabezado_h2(titulo: str):
    """
    Imprime un encabezado para los menus secundarios de la consola.
    """
    ancho = 50
    print("=" * ancho)
    print(f"{titulo.center(ancho)}")
    print("=" * ancho)

def normalizar_entrada(texto: str) -> str:
    """
    Limpia el texto de entrada: elimina espacios extra y convierte 
    comas en puntos para asegurar que float() no falle.
    """
    if not texto:
        return ""
    return texto.strip().replace(",", ".")

def formatear_texto(texto: str, color: str = "rojo", estilo: str = "negrita") -> str:
    """
    Aplica códigos de escape ANSI para dar formato de color y estilo al texto en la terminal.

    Args:
        texto (str): La cadena de texto que se quiere formatear.
        color (str, opcional): El color de la fuente. 
        estilo (str, opcional): El estilo de la fuente. 

    Returns:
        str: El texto original envuelto en los códigos ANSI de formato y reseteo.
    """
    RESET = "\033[0m"
    
    colores = {
        "rojo": "\033[31m",
        "amarillo": "\033[33m",
        "verde": "\033[32m",
        "azul": "\033[34m",
        "blanco": ""
    }

    estilos = {
        "negrita": "\033[1m",
        "cursiva": "\033[3m",
        "normal": ""
    }
    
    codigo_color = colores.get(color, "")
    codigo_estilo = estilos.get(estilo, "")
    
    return f"{codigo_estilo}{codigo_color}{texto}{RESET}"

def borrar_lineas(n: int) -> None:
    """Retrocede el cursor n líneas y borra el contenido."""
    for _ in range(n):
        sys.stdout.write("\033[F") # Mueve el cursor a la línea anterior
        sys.stdout.write("\033[K") # Borra la línea actual
    sys.stdout.flush()