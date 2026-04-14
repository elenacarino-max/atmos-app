#Construir un json con datos aleatorios
import json
import random

# 1. Generar datos aleatorios
from datetime import timedelta, datetime

inicio = datetime(2000, 1, 1)
fin = datetime.now()
def fecha_aleatoria(inicio, fin):
    delta = fin - inicio
    dias = random.randint(0, delta.days)
    fecha = inicio + timedelta(days=dias)
    return fecha.strftime("%Y-%m-%d")

datos = []
combinaciones_usadas = set()
while len(datos) < 100:
  ## Evitar combinaciones repetidas de fecha y zona
  fecha = fecha_aleatoria(inicio, fin)
  zona = random.choice(["norte", "sur", "centro"])
  clave = (fecha, zona) #Combinación única de fecha y zona
  if clave not in combinaciones_usadas: 
    combinaciones_usadas.add(clave)
    datos_aleatorios = {
    	"fecha_registro": fecha,
    	"zona_registro": zona,
    	"temperatura": random.uniform(-15, 50),
    	"humedad_nivel": random.uniform(0, 100),
    	"viento_velocidad": random.uniform(0, 130),
	    "alerta_temperatura": random.choice([True, False]),
	    "alerta_humedad": random.choice([True, False]),
	    "alerta_viento": random.choice([True, False])
}

    datos.append(datos_aleatorios)

# 3. Guardar todos los datos generados en un archivo con permisos de escritura (w)
with open('datos_aleatorios.json', 'w') as f:
    json.dump(datos, f, indent=4)