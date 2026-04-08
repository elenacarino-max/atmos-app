def evaluate_alerts(registro):
    alerts = []

    #Temperatura (°C) 
    #Se considera alerta si está fuera del rango definido
    temp = registro["temperatura"]
    alert_temp = temp < -8 or temp > 40
    if alert_temp:
        alerts.append("Alarma: Riesgo de temperatura")
    #Viento (km/h)
    #Se considera alerta si está fuera del rango definido 
    viento = registro["viento_velocidad"]
    alert_viento = viento >= 70
    if alert_viento:
        alerts.append("Alarma: Riesgo de viento alto")
    #Humedad (%) 
    #Se considera alerta si está fuera del rango definido
    hum = registro["humedad_nivel"]
    alert_hum = (0 < hum <= 20) or (70 < hum <= 100)
    if alert_hum:
        alerts.append("Alarma: Riesgo de humedad")

    #Devolveremos tanto mensajes de alertas como definicion del bool alerta
    return {
        "mensajes": alerts,
        "alerta_temperatura": alert_temp,
        "alerta_viento": alert_viento,
        "alerta_humedad": alert_hum
    }