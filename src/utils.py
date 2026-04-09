from datetime import datetime

def validar_rango(valor, minimo, maximo, nombre_variable):
    """Verifica si un valor está dentro de un rango lógico."""
    if minimo <= valor <= maximo:
        return True
    else:
        print(f"⚠️ Error: {nombre_variable} debe estar entre {minimo} y {maximo}.")
        return False

def solicitar_numero(mensaje, minimo, maximo, nombre_variable):
    """Pide un número y no para hasta que sea válido y esté en rango."""
    while True:
        try:
            dato = float(input(mensaje))
            if validar_rango(dato, minimo, maximo, nombre_variable):
                return dato
        except ValueError:
            print("❌ Entrada inválida: Por favor, introduce un número válido.")

def solicitar_fecha():
    """Valida que el formato de fecha sea correcto (AAAA-MM-DD)."""
    while True:
        fecha_str = input("Introduce la fecha (AAAA-MM-DD) [Enter para hoy]: ")
        if not fecha_str:
            return datetime.now().strftime("%Y-%m-%d")
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
            return fecha_str
        except ValueError:
            print("❌ Formato incorrecto. Usa el formato AAAA-MM-DD (ej. 2024-05-20).")
def registrar_medicion_completa():
    """Carga, valida, alerta y guarda el registro."""
    #historico = cargar_datos_json()

        
def solicitar_zona():
    """Carga, valida, alerta y guarda el registro."""
    #historico = cargar_datos_json()

    print("\n--- NUEVA ENTRADA DE DATOS ---")
    zona = input("zona (norte/centro/sur): ").strip().lower()
    if zona not in ['norte', 'centro', 'sur']:
        print("❌ zona no válida.")
        return 
    return zona
  
        
def capturar_datos_estacion():
   
    print("\n--- Registro de Nueva Medición ---")


    fecha = solicitar_fecha()

    # Aplicamos rangos lógicos según estándares climáticos
    zona = solicitar_zona()
    temp = solicitar_numero("Temperatura (ºC) [-8 a 40]: ", -8, 40, "La temperatura")
    humedad = solicitar_numero("Humedad (%) [21 a 69]: ", 21, 69, "La humedad")
    viento = solicitar_numero("Viento (km/h) [1 a 70]: ", 1, 70, "La velocidad del viento")

    # Retornamos un diccionario listo para ser guardado en JSON
    registro = {
        "fecha": fecha,
        "zona": zona,
        "temperatura": temp,
        "humedad": humedad,
        "viento": viento
    }

    return registro

# Prueba de ejecución
if __name__ == "__main__":
    datos = capturar_datos_estacion()
    print("\n✅ Datos validados correctamente:")
    print(datos)
    