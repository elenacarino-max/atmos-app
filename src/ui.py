from datetime import date
from utils import normalizar_entrada 
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
    

