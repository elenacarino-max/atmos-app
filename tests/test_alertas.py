# Comprobación en pytest para validar el sistema de alertas
# Simulan valores críticos en este caso, temp,  viento y humedad

from src.alerts import evaluar_alerta


def test_alerta_temperatura_alta():
    registro = {
        "temperatura": 41,
        "viento_velocidad": 20,
        "humedad_nivel": 50
    }
    #pasamos datos referencia llamando funcion 
    resultado = evaluar_alerta(registro)

    #comprobar condición
    assert resultado["alerta_temperatura"]
    assert "Alarma: Riesgo de temperatura" in resultado["mensajes"]


def test_alerta_viento_alto():
    registro = {
        "temperatura": 25,
        "viento_velocidad": 70,
        "humedad_nivel": 50
    }
    #pasamos datos referencia llamando funcion 
    resultado = evaluar_alerta(registro)

    assert resultado["alerta_viento"]
    assert "Alarma: Riesgo de viento alto" in resultado["mensajes"]


def test_alerta_humedad():
    registro = {
        "temperatura": 25,
        "viento_velocidad": 20,
        "humedad_nivel": 75
    }
    #pasamos datos referencia llamando funcion  
    resultado = evaluar_alerta(registro)

    assert resultado["alerta_humedad"]
    assert "Alarma: Riesgo de humedad" in resultado["mensajes"]


def test_sin_alertas():
    registro = {
        "temperatura": 25,
        "viento_velocidad": 20,
        "humedad_nivel": 50
    }
    #pasamos datos referencia llamando funcion
    resultado = evaluar_alerta(registro)

    assert not resultado["alerta_temperatura"]
    assert not resultado["alerta_viento"]
    assert not resultado["alerta_humedad"] 