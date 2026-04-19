import time
from datetime import date
import sys
import validation as val
from typing import Callable, Optional
from utils import (
    formatear_texto, 
    normalizar_entrada, 
    imprimir_encabezado_h1, 
    limpiar_pantalla 
)

def solicitar_fecha(msg_fecha: str) -> str:
    """
    Solicita una fecha al usuario por consola con opción de valor por defecto.

    Mantiene al usuario en un bucle hasta que el dato esté validado.

    Args:
        msg (str): El mensaje descriptivo que se mostrará al usuario.

    Returns:
        str: La fecha validada en formato string. Si el usuario presiona ENTER, 
             devuelve la fecha actual.
    """
    while True:
        fecha = input(f"➤  {msg_fecha}").strip()
        if fecha == "":
            return str(date.today())
        elif val.validar_fecha_registro(fecha):
            return fecha
        else:
            print(f"   {formatear_texto('Error')}:"
                  f" {formatear_texto(fecha, estilo="normal")} no es una fecha válida.")
        
def solicitar_zona(msg_zona: str) -> str:
    """
    Solicita y valida el nombre de una zona geográfica por teclado.

    Mantiene un bucle hasta que se introduce una zona que cumple con las reglas
    definidas en el módulo de validación.

    Args:
        msg_zona (str): El mensaje o etiqueta que se mostrará al usuario.

    Returns:
        str: El nombre de la zona validado, en minúsculas y sin espacios extra.
    """
    while True:
        zona = input(f"➤  {msg_zona}").strip().lower()
        if val.validar_zona_registro(zona):
            return zona
        elif zona == "":
            print(f"   {formatear_texto('Error')}: Este campo no puede"
                  f" estar {formatear_texto('vacío', estilo="normal")}.")
        else:
            print(f"   {formatear_texto('Error')}: "
                  f"{formatear_texto(zona, estilo="normal")} no es una zona válida.")
        
def solicitar_dato_numerico(msg_dato: str, 
                            f_validacion: Callable[[float], bool], 
                            medida: str = "medida") -> float:
    """
    Solicita, normaliza y valida una entrada numérica (temperatura, humedad, viento).

    Convierte comas en puntos, transforma la entrada a float y aplica una 
    función de validación externa para comprobar rangos.

    Args:
        msg_dato (str): El mensaje que se mostrará al usuario para pedir el dato.
        f_validacion (Callable[[float], bool]): Una función que reciba un float 
            y devuelva un booleano.
        medida (str, opcional): El nombre de la magnitud.

    Returns:
        float: El valor numérico validado.
    """
    while True:  
        dato = input(f"➤  {msg_dato}").strip().lower()
        # Normalizar antes de validar: cambiar ',' por '.'
        dato = normalizar_entrada(dato)
        
        try:
            dato = float(dato)
            es_valido = f_validacion(dato)
            if es_valido:
                return dato
            else:
                print(f"   {formatear_texto('Error')}: "
                      f"{formatear_texto(dato, estilo="normal")} "
                      f"no está dentro del rango permitido.")
        except ValueError:
            if dato == "":
                print(f"   {formatear_texto('Error')}: Este campo no "
                      f"puede estar {formatear_texto('vacío', estilo="normal")}.")                        
            else:
                print(f"   {formatear_texto('Error')}: "
                      f"{formatear_texto(dato, estilo="normal")} no es una {medida} permitida.")         
        
def solicitar_medicion() -> Optional[dict]:
    """
    RCoordina la recogida de todos los datos necesarios para una medición meteorológica.

    La función invoca secuencialmente las peticiones de fecha, zona y datos numéricos.
    Si el usuario cancela mediante KeyboardInterrupt (Ctrl+C), la función captura
    la excepción y regresa al menú principal de forma segura.ecoge una medición completa.

    Returns:
        Optional[dict]: Un diccionario con las claves 'fecha_registro', 'zona_registro', 
                        'temperatura', 'humedad_nivel' y 'viento_velocidad'. 
                        Devuelve None si el proceso es interrumpido o cancelado.
    """  
    try:
        # Solicitar datos
        print("\n (Presiona ENTER para usar la fecha de hoy)")
        fecha = solicitar_fecha("Fecha (AAAA-MM-DD): ")
        if fecha is None:
            return
        
        zona = solicitar_zona("Zona/Distrito [Norte - Centro - Sur]: ")
        if zona is None:
            return
        
        temperatura = solicitar_dato_numerico("Temperatura [-15°C - 50°C]: ", 
                                                val.validar_temperatura, 
                                                "temperatura")
        if temperatura is None:
            return
        
        humedad = solicitar_dato_numerico("Humedad [0 % - 100 %]: ", 
                                          val.validar_humedad_nivel, 
                                          "humedad")
        if humedad is None:
            return
        
        viento = solicitar_dato_numerico("Velocidad del viento [0 km/h - 130 km/h]: ", 
                                         val.validar_viento_velocidad, 
                                         "velocidad")
        if viento is None:
            return

        return {
            "fecha_registro": fecha,
            "zona_registro": zona,
            "temperatura": temperatura,
            "humedad_nivel": humedad,
            "viento_velocidad": viento
        }  

    except KeyboardInterrupt:
        print(f"\n\n  {formatear_texto('Operación cancelada', 'amarillo')}: "
               "Volviendo al menú principal.")
        time.sleep(2)
        return

def mostrar_menu_principal() -> str:
    """
    Muestra la interfaz principal del sistema ATMOS y captura la elección del usuario.

    La función imprime el título principal y las opciones disponibles (registro, 
    consulta y gráficos), devolviendo la opción limpia de espacios.

    Returns:
        str: El carácter o número ingresado por el usuario.
    """
    imprimir_encabezado_h1("ATMOS: GESTIÓN METEOROLÓGICA URBANA")
    print(" [1] Registrar nueva medición")
    print(" [2] Consultar registro meteorológico por zona")
    print(" [3] Ver histórico")
    print(" [4] Ver gráficos")
    print(" [X] Salir")
    print("-" * 50)
    return input("Selecciona una opción: ").strip()

def mostrar_resumen_registro(registro: dict) -> str:
    """
    Imprime en consola una tabla visual con los datos meteorológicos capturados.

    Args:
        registro (dict): Diccionario que contiene los datos de la medición. 

    Returns:
        None
    """
    print("\n" + "─" * 50)
    print("RESUMEN DE LOS DATOS INTRODUCIDOS:\n")
    print(f"   • Fecha:       {registro["fecha_registro"]}")
    print(f"   • Zona:        {registro["zona_registro"].capitalize()}")
    print(f"   • Temperatura: {registro["temperatura"]}°C")
    print(f"   • Humedad:     {registro["humedad_nivel"]} %")
    print(f"   • Viento:      {registro["viento_velocidad"]} km/h")
    print("─" * 50)

def mostrar_confirmacion() -> str:
    """
    Solicita al usuario una decisión mediante una entrada de teclado.

    Returns:
        str: La opción seleccionada por el usuario.
    """
    print("\n¿Desea guardar este registro?")
    print(" [1] Aceptar")
    print(" [2] Cancelar")
    print(" [X] Salir")
    return input("\n>> Selecciona una opción: ")

def mostrar_submenu_consultas() -> str:
    """
    Muestra un menú secundario tras realizar una consulta de datos.

    Permite al usuario decidir si desea continuar consultando datos específicos 
    o regresar a la pantalla de inicio del programa.

    Returns:
        str: La opción seleccionada por el usuario.
    """
    print("\n" + "-"*50)
    print(" [1] Realizar otra consulta")
    print(" [X] Salir")
    print("-"*50)
    return input("Selecciona una opción: ").strip()

def efecto_maquina_escribir(texto: str, velocidad: float = 0.03) -> None:
    """
    Imprime un texto en la consola carácter por carácter.

    Args:
        texto: El mensaje que se desea mostrar con el efecto.
        velocidad: Tiempo de espera en segundos entre caracteres.
    
    Returns:
        None
    """
    for caracter in texto:
        sys.stdout.write(caracter)
        sys.stdout.flush()
        time.sleep(velocidad)
    print()

def transicion_bienvenida() -> None:
    """
    Orquesta la secuencia de apertura: muestra el logo y mensajes de carga.
    
    Returns:
        None
    """
    try:
        limpiar_pantalla()
        imprimir_logo_atmos('bienvenida')
        print("\n" + " " * 20 + "Iniciando Atmos® ...")
        time.sleep(1.5)  
        efecto_maquina_escribir(" " * 20 + "Cargando aplicación ...")
        time.sleep(1)
    except KeyboardInterrupt:
        return
    
def transicion_despedida() -> None:
    """
    Orquesta la secuencia de cierre: logo de despedida y mensajes finales.
    
    Returns:
        None
    """
    try: 
        limpiar_pantalla()
        imprimir_logo_atmos('despedida')
        efecto_maquina_escribir("\n" + " " * 22 + "Cerrando sesión ...")
        time.sleep(1)
        print(" " * 18 + "¡Gracias por usar Atmos®!")
        time.sleep(2)
        limpiar_pantalla()
    except KeyboardInterrupt:
        return
    
def imprimir_linea_por_linea(texto: str, velocidad_linea: float = 0.05) -> None:
    """
    Muestra un bloque de texto de forma animada.

    Divide el texto en líneas individuales y las imprime una a una con una breve
    pausa, creando un efecto visual de desplazamiento vertical.

    Args:
        texto: El bloque de texto completo que se desea animar.
        velocidad_linea: Segundos de espera entre la impresión de cada línea.

    Returns:
        None
    """
    try: 
        # Dividimos el texto en una lista de líneas individuales
        lineas = texto.strip('\n').split('\n')
        
        for linea in lineas:
            print(linea)
            time.sleep(velocidad_linea)
        
        time.sleep(0.5)
    except KeyboardInterrupt:
        return

def imprimir_logo_atmos(estado: str=None) -> None:
    """
    Muestra el logotipo en ASCII de ATMOS en la consola con colores.

    Dependiendo del estado del programa, imprime una versión simplificada 
    o una versión completa con el nombre "ATMOS". Utiliza códigos 
    ANSI para renderizar el arte en color azul.

    Args:
        estado: Define qué versión del logo mostrar. 
                Valores aceptados: 'bienvenida', 'despedida'. 
                Cualquier otro valor mostrará el logo por defecto.

    Returns:
        None
    """
    logo_ascii = r"""
                                                              ++++++++                                                            
                                                            ++++++++++++                                                          
                                                           ++++++++++++++                                                         
                                                           +++++++++++++++                                                        
                                                          +++++++++++++++++                                                       
                                                         +++++++++++++++++++                                                      
                                                        ++++++++++++++++++++                +++++++++++++                         
                                                       ++++++++++++++++++++++             ++++++++++++++++++                      
                                                       +++++++++++++++++++++++          ++++++++++++++++++++++                    
                                                      +++++++++++++++++++++++++        ++++++      ++++++++++++                   
                                                     +++++++++++++++++++++++++++       +++            ++++++++++                  
                                                    +++++++++++++  +++++++++++++      +++              +++++++++                  
                                                   +++++++++++++    +++++++++++++     ++               ++++++++++                 
                                                  ++++++++++++++     +++++++++++++     +               ++++++++++                 
                                                  +++++++++++++       +++++++++++++                    +++++++++                  
                                                 +++++++++++++         +++++++++++++                 +++++++++++                  
                                                +++++++++++++          ++++++++++++++              ++++++++++++                   
                                               +++++++++++++            +++++++++               ++++++++++++++                    
                                              ++++++++++++++                              +++++++++++++++++++                     
                                             ++++++++++++                +++++++++++++++++++++++++++++++++++                      
                                             +++++++         ++++++++++++++++++++++++++++++++++++++++++++                         
                                            ++++       ++++++++++++++++++++++++++++++++++++++++++++++++                           
                                           ++      ++++++++++++++++++++++++++++++++++++++++++++++++                               
                                          +     ++++++++++++++++++++++++++++++++++++++++++++                                      
                                              ++++++++++++++++++++++++++++++                                                      
                                            +++++++++++++++++++                          +++                                      
                                          +++++++++++++++                      ++++++++++++++                                     
                                        ++++++++++++++                          ++++++++++++++                                    
                                       +++++++++++++                             ++++++++++++++                                   
                                     +++++++++++++                                +++++++++++++                                   
                                    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                                  
                                   ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                                 
                                  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                                
                              ++++++++++++++++++++                                ++++++++++++++++++++                            
                          ++++++++++++++                                                     +++++++++++++                        
                       ++++++++++                                                                   +++++++++                     
                    +++++++                                                                              +++++++                  
                  ++++                                                                                        +++++               
               +++                                                                                                 +++             
    """           
    logo_nombre = r"""                                                                                                
                              ++++          ++++                                                                                  
                             ++++++         ++++       +++  ++++      +++++          +++++++          ++++++                        
                            +++  +++      ++++++++++   ++++++++++++ +++++++++      +++++++++++     +++++++++++                    
                           +++    +++       ++++       +++++    +++++     ++++    ++++     +++++  ++++                            
                          +++      +++      ++++       ++++      +++       +++   ++++        +++  ++++++                          
                         ++++++++++++++     ++++       +++       +++       +++   ++++        +++    +++++++++                     
                        ++++++++++++++++    ++++       +++       +++       +++   ++++       ++++           +++                    
                       ++++          ++++   +++++  +   +++       +++       +++    ++++++  +++++   ++++    ++++                    
                      ++++            ++++    ++++++   +++       +++       +++      +++++++++      ++++++++++                                                                             
    """
    
    logo_ascii = logo_ascii.strip('\n')
    logo_nombre = logo_nombre.strip('\n')
    
    if estado == 'bienvenida':
        imprimir_linea_por_linea(formatear_texto(logo_ascii, color="azul", estilo=""))
    elif estado == 'despedida':
        logo_completo = logo_ascii +logo_nombre
        imprimir_linea_por_linea(formatear_texto(logo_completo, color="azul", estilo=""))
    else:
        print(formatear_texto(logo_ascii, color="azul", estilo=""))