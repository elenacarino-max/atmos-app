import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.widgets import RadioButtons
import matplotlib.animation as animation
from matplotlib.dates import DateFormatter, AutoDateLocator
import mplcyberpunk
import numpy as np
import locale
from typing import List, Dict, Any

# Configuración de idioma
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES')
    except:
        pass

# Configuración de estilo
plt.style.use("cyberpunk")
sns.set_context("notebook", font_scale=1.1)

def mostrar_grafico_interactivo(fechas: List[Any], 
                                datos_sensores: Dict[str, Any], 
                                zona: str) -> None:
    """
    Genera una interfaz visual interactiva para el monitoreo de mediciones.

    La función crea un gráfico dinámico con animaciones de alerta y un menú de selección
    para alternar entre datos de temperatura, humedad y viento. Incluye cálculos 
    estadísticos (media, desviación) y resaltado de valores máximos y mínimos.

    Args:
        fechas (List[Any]): Lista de marcas de tiempo o fechas para el eje X.
        datos_sensores (Dict[str, Any]): Diccionario que contiene las claves 
            'temperatura', 'humedad' y 'viento'. Cada clave debe tener:
            - 'datos': np.array o lista con los valores numéricos.
            - 'alertas': máscara booleana o índices de puntos de alerta.
        zona (str): Nombre de la ubicación geográfica para mostrar en el título.

    Returns:
        None: La función despliega la ventana de Matplotlib y bloquea la ejecución 
        hasta que esta se cierra.
    """
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='#212946')
    ax.set_facecolor('#212946')
    
    plt.subplots_adjust(left=0.1, right=0.88, top=0.82, bottom=0.15)

    ax.xaxis.set_major_locator(AutoDateLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%b %Y"))

    colores_neon = ["#08F7FE", "#FE53BB", "#FF9427"]
    conf = {
        'temperatura': {'color': colores_neon[0], 'uni': 'Temperatura (°C)'},
        'humedad':     {'color': colores_neon[1], 'uni': 'Humedad (%)'},
        'viento':      {'color': colores_neon[2], 'uni': 'Velocidad del viento (km/h)'}
    }

    s_id = 'temperatura'
    d_raw = np.array(datos_sensores[s_id]['datos'])
    a_raw = np.array(datos_sensores[s_id]['alertas'])
    color_act = conf[s_id]['color']

    ax.set_xlim(fechas[0], fechas[-1])

    linea, = ax.plot(fechas, d_raw, color=color_act, lw=2.5, zorder=4, marker='o', markersize=4)
    
    m, s = np.mean(d_raw), np.std(d_raw)
    v_max, v_min = np.max(d_raw), np.min(d_raw)
    
    sombreado = ax.fill_between(fechas, m-s, m+s, color=color_act, alpha=0.1, zorder=2)
    linea_media = ax.axhline(m, color='#FFFFFF', ls='--', lw=1, alpha=0.3, zorder=1)
    
    estilo_txt = {'transform': ax.get_yaxis_transform(), 'fontsize': 9, 'fontweight': 'bold'}
    texto_media = ax.text(1.01, m, f'Media: {m:.1f}', color='#FFFFFF', alpha=0.6, **estilo_txt)
    texto_max = ax.text(1.01, v_max, f'Máximo: {v_max:.1f}', color=color_act, **estilo_txt)
    texto_min = ax.text(1.01, v_min, f'Mínimo: {v_min:.1f}', color=color_act, **estilo_txt)

    marcad_alarmas = ax.scatter(np.array(fechas)[a_raw], d_raw[a_raw], s=100, 
                                facecolors='#FF003C', edgecolors='none', linewidths=0, zorder=10)

    ax.set_title(f"ATMOS. Gráficos | Zona: {zona}", loc='left', fontsize=16, 
                 fontweight='bold', color='#CFD8DC', pad=40)
    
    ax.set_ylabel(conf[s_id]['uni'], fontsize=12, color=color_act, labelpad=15)
    
    ax.grid(color='#2A3459') 
    sns.despine(left=True, bottom=True)

    def actualizar(label: str) -> None:
        """Callback para actualizar los datos del gráfico según el RadioButton."""
        nonlocal sombreado
        s_id = label.lower()
        d_new = np.array(datos_sensores[s_id]['datos'])
        a_new = np.array(datos_sensores[s_id]['alertas'])
        c_new, u_new = conf[s_id]['color'], conf[s_id]['uni']

        linea.set_ydata(d_new); linea.set_color(c_new)
        ax.set_ylabel(u_new, color=c_new)
        marcad_alarmas.set_offsets(np.c_[np.array(fechas)[a_new], d_new[a_new]])

        m_n, v_mx, v_mn = np.mean(d_new), np.max(d_new), np.min(d_new)
        s_n = np.std(d_new)
        
        linea_media.set_ydata([m_n, m_n])
        texto_media.set_text(f'Media: {m_n:.1f}'); texto_media.set_position((1.01, m_n))
        texto_max.set_text(f'Máximo: {v_mx:.1f}'); texto_max.set_position((1.01, v_mx)); texto_max.set_color(c_new)
        texto_min.set_text(f'Mínimo: {v_mn:.1f}'); texto_min.set_position((1.01, v_mn)); texto_min.set_color(c_new)
        
        sombreado.remove()
        sombreado = ax.fill_between(fechas, m_n-s_n, m_n+s_n, color=c_new, alpha=0.1, zorder=2)

        ax.relim()
        ax.autoscale_view(scalex=False, scaley=True) 
        plt.draw()

    ax_menu = plt.axes([0.72, 0.83, 0.2, 0.12], facecolor='#212946', frameon=False)
    selector = RadioButtons(ax_menu, ('Temperatura', 'Humedad', 'Viento'), activecolor='#CFD8DC')
    
    for l in selector.labels: 
        l.set_color('#CFD8DC')
        l.set_fontsize(10)
    
    selector.on_clicked(actualizar)

    def animar(f: int) -> Any:
        """Efecto de parpadeo para los puntos de alerta."""
        marcad_alarmas.set_visible(not marcad_alarmas.get_visible())
        return marcad_alarmas,

    # Lanzamiento de la animación y visualización
    ani = animation.FuncAnimation(fig, animar, interval=600, blit=True, cache_frame_data=False)
    plt.show()