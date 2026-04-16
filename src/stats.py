from datetime import datetime
import plotille
from logger import log_info, log_error
from typing import List, Dict
 
def calcular_estadisticas(datos: List[float]) -> Dict[str, float]:
    """
    Calcula el mínimo, máximo y media de una serie numérica.
    
    Args:
        datos: Lista de valores.
        
    Returns:
        Diccionario con las claves 'min', 'max' y 'media'.
    """
    if not datos:
        return {}

    return {
        "min": float(min(datos)),
        "max": float(max(datos)),
        "media": sum(datos) / len(datos)
    }

def mostrar_estadisticas(variable: str, unidad: str, datos: List[float]) -> None:
    """
    Muestra por consola un resumen estadístico de los datos.

    Args:
        variable: Nombre de la medición (ej. "Temperatura", "Viento").
        unidad: Unidad de medida (ej. "°C", "km/h").
        datos: Lista de valores numéricos para el eje vertical.
    """
    stats = calcular_estadisticas(datos)
    
    print(f"\n {variable}: "
          f"Mín.: {stats['min']:>3.1f} {unidad} | "
          f"Media: {stats['media']:>3.1f} {unidad} | "
          f"Máx.: {stats['max']:>3.1f} {unidad}")

def mostrar_grafico(variable: str, unidad: str, fechas: List[datetime], datos: List[float]) -> None:
    """
    Renderiza un gráfico de dispersión/líneas en la terminal usando Plotille.
    
    Ajusta automáticamente el eje Y con precisión de un decimal y el eje X 
    con formato mes-año, manteniendo una alineación vertical fija para 
    comparativa entre múltiples gráficos.

    Args:
        variable: Nombre de la medición (ej. "Temperatura", "Viento").
        unidad: Unidad de medida (ej. "°C", "km/h").
        fechas: Lista de objetos datetime para el eje horizontal.
        datos: Lista de valores numéricos para el eje vertical.
    """
    try:    
        log_info(f"Generando gráfico de {variable} con {len(datos)} registros.")

        # Configuración de la figura de Plotille
        fig = plotille.Figure()
        fig.width = 70
        fig.height = 8 
        fig.x_label = 'mm-yyyy'
        fig.y_label = unidad

        # Eje X: Muestra Mes-Año
        fig.register_label_formatter(datetime, lambda dt, *a, **k: dt.strftime("%m-%Y"))

        # Eje Y: Fuerza 1 decimal y reserva 7 espacios para alineación 
        fig.register_label_formatter(float, lambda v, *a, **k: f"{v:>7.1f}")

        fig.plot(fechas, datos)
        print(fig.show())

        log_info(f"Gráfico de {variable} renderizado correctamente.")

    except Exception as e:
        log_error(f"Error crítico visualizando {variable}: {str(e)}")
        print(f" Error de visualización: {e}")
        