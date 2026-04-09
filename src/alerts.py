def evaluar_alerta(registro):
    alerts = []

    #Temperatura (°C) 
    #Se considera alerta si está fuera del rango definido
    temp = registro["temperatura"]
    alerta_temp = temp < -8 or temp > 40
    if alerta_temp:
        alerts.append("Alarma: Riesgo de temperatura")
    #Viento (km/h)
    #Se considera alerta si está fuera del rango definido 
    viento = registro["viento_velocidad"]
    alerta_viento = viento >= 70
    if alerta_viento:
        alerts.append("Alarma: Riesgo de viento alto")
    #Humedad (%) 
    #Se considera alerta si está fuera del rango definido
    hum = registro["humedad_nivel"]
    alerta_hum = (0 < hum <= 20) or (70 < hum <= 100)
    if alerta_hum:
        alerts.append("Alarma: Riesgo de humedad")

    #Devolveremos tanto mensajes de alertas como definicion del bool alerta
    return {
        "mensajes": alerts,
        "alerta_temperatura": alerta_temp,
        "alerta_viento": alerta_viento,
        "alerta_humedad": alerta_hum
    }