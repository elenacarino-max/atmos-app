

# Importamos datetime para poder comprobar si la fecha tiene el #formato correcto

from datetime import datetime, date

# Comprueba que la fecha esté escrita como AAAA-MM-DD,
# que sea una fecha válida y que no sea futura
def validar_fecha_registro(fecha_registro):
    try:
        # Convierte el texto en una fecha
        fecha_convertida = datetime.strptime(fecha_registro, "%Y-%m-%d").date()
        # Obtiene la fecha de hoy
        hoy = date.today()
        # Si la fecha es posterior a hoy, no es válida
        if fecha_convertida > hoy:
            return False
        return True
    except ValueError:
        # Si falla, significa que la fecha está mal escrita o no existe
        return False
# Comprueba que la zona sea una de las permitidas: norte, centro o sur
def validar_zona_registro(zona_registro):
    zonas_validas = ["norte", "centro", "sur"]

    if zona_registro in zonas_validas:
        return True
    return False

# Comprueba que la temperatura no sea un dato erróneo
# Es errónea si es menor que -15 o mayor que 50
def validar_temperatura(temperatura):
    if temperatura < -15 or temperatura > 50:
        return False
    return True

# Comprueba que la humedad esté entre 0 y 100
def validar_humedad_nivel(humedad_nivel):
    if humedad_nivel < 0 or humedad_nivel > 100:
        return False
    return True

# Comprueba que la velocidad del viento sea válida
# Es errónea si es menor o igual que 0 o mayor que 130
def validar_viento_velocidad(viento_velocidad):
    if viento_velocidad <= 0 or viento_velocidad > 130:
        return False
    return True

# Comprueba si ya existe un registro con la misma fecha y la misma zona
# registros_existentes será la lista de registros que ya se ha cargado desde el JSON
def validar_duplicado(fecha_registro, zona_registro, registros_existentes):
    for registro in registros_existentes:
        if (
            registro.get("fecha_registro") == fecha_registro
            and registro.get("zona_registro", "") == zona_registro
        ):
            # Si encuentra un registro con misma fecha y misma zona, está duplicado
            return False

    # Si recorre toda la lista y no encuentra ninguno igual, no está duplicado
    return True