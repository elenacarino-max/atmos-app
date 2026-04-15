import time
from datetime import date
import sys
from utils import limpiar_pantalla, imprimir_encabezado_h1, normalizar_entrada 
import validation as val

def solicitar_fecha(msg_fecha):
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
        try:
            fecha = input(f"➤  {msg_fecha}").strip()
            if fecha == "":
                return str(date.today())
            elif val.validar_fecha_registro(fecha):
                return fecha
            else:
                print(f"   ❌ Error: {fecha} no es una fecha válida. Inténtalo de nuevo.")
        except EOFError:
            return None
        
def solicitar_zona(msg_zona):
    
    while True:
        try:
            zona = input(f"➤  {msg_zona}").strip().lower()
            if val.validar_zona_registro(zona):
                return zona
            elif zona == "":
                print(f"   ❌ Error: Este campo no puede estar vacio. Introduce una zona.")
            else:
                print(f"   ❌ Error: {zona} no es una zona válida. Inténtalo de nuevo.")
        except EOFError:
            return None
        
def solicitar_dato_numerico(msg_dato, f_validacion, medida="medida"):

    while True:
        try:    
            dato = input(f"➤  {msg_dato}").strip().lower()
            # Normalizar antes de validar: cambiar ',' por '.'
            dato = normalizar_entrada(dato)
            
            try:
                dato = float(dato)
                es_valido = f_validacion(dato)
                if es_valido:
                    return dato
                else:
                    print(f"   ❌ Error: {dato} no está dentro del rango permitido. Inténtalo de nuevo.")
            except ValueError:
                if dato == "":
                    print(f"   ❌ Error: Este campo no puede estar vacío. Inténtalo de nuevo.")                        
                else:
                    print(f"   ❌ Error: {dato} no es una medición de {medida} permitida. Inténtalo de nuevo.")         
        except EOFError:
            return None
        
def solicitar_medicion():
    """
    Recoge una medición completa.

    Returns:
        Un diccionario con la medición o None si el usuario cancela la operación.
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
        print("\n\n⚠️  Operación cancelada por el usuario.")
        print("\n ↩ Volviendo al menú principal.")
        return None

def mostrar_menu_principal() -> str:
    """
    Muestra la interfaz principal del sistema ATMOS y captura la elección del usuario.

    La función imprime el título principal y las opciones disponibles (registro, 
    consulta y estadísticas), devolviendo la opción limpia de espacios.

    Returns:
        str: El carácter o número ingresado por el usuario.
    """
    imprimir_encabezado_h1("ATMOS: GESTIÓN METEOROLÓGICA URBANA")
    print(" [1] Registrar nueva medición")
    print(" [2] Consultar registro meteorológico por zona (En desarrollo)")
    print(" [3] Ver histórico")
    print(" [4] Ver estadísticas (En desarrollo)")
    print(" [X] Salir")
    print("-" * 50)
    return input("Seleccione una opción: ").strip()

def mostrar_resumen_registro(registro) -> str:

    print("\n" + "─" * 50)
    print("RESUMEN DE LOS DATOS INTRODUCIDOS:\n")
    print(f"   • Fecha:       {registro["fecha_registro"]}")
    print(f"   • Zona:        {registro["zona_registro"].capitalize()}")
    print(f"   • Temperatura: {registro["temperatura"]}°C")
    print(f"   • Humedad:     {registro["humedad_nivel"]} %")
    print(f"   • Viento:      {registro["viento_velocidad"]} km/h")
    print("─" * 50)

def mostrar_confirmacion() -> str:

    print("\n¿Desea guardar este registro?")
    print(" [1] Aceptar")
    print(" [2] Cancelar")
    print(" [X] Salir")
    return input("\n>> Seleccione una opción: ")

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
    print(" [2] Volver al menú principal")
    print("-"*50)
    return input("Seleccione una opción: ").strip()

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

    color_azul = "\033[34m"
    reset = "\033[0m"

    logo_ascii = logo_ascii.strip('\n')
    logo_nombre = logo_nombre.strip('\n')
    
    if estado == 'bienvenida':
        imprimir_linea_por_linea(f"{color_azul}{logo_ascii}{reset}")
    elif estado == 'despedida':
        logo_completo = logo_ascii +logo_nombre
        imprimir_linea_por_linea(f"{color_azul}{logo_completo}{reset}")
    else:
        print(f"{color_azul}{logo_ascii}{reset}")