#Construir un json con datos aleatorios
import json
import random

# 1. Generar datos aleatorios
from datetime import timedelta, datetime

d=0
inicio = datetime(2000, 1, 1)
fin = datetime.now()
def fecha_aleatoria(inicio, fin):
    delta = fin - inicio
    dias = random.randint(0, delta.days)
    fecha = inicio + timedelta(days=dias)
    return fecha.strftime("%Y-%m-%d")

while d < 101:
  datos_aleatorios = {
    	"fecha_registro": fecha_aleatoria(inicio, fin),
    	"zona_registro": random.choice(["norte", "sur", "centro"]),
    	"temperatura": random.uniform(-15, 50),
    	"humedad_nivel": random.uniform(0, 100),
    	"viento_velocidad": random.uniform(0, 130),
	    "alerta_temperatura": random.choice([True, False]),
	    "alerta_humedad": random.choice([True, False]),
	    "alerta_viento": random.choice([True, False])
}

# 2. Convertir a formato JSON (cadena de texto)
  json_string = json.dumps(datos_aleatorios, indent=4) # indent=4 para legibilidad
  print(json_string)

# 3. Guardar en un archivo con permisos de escritura (w)
  with open('datos_aleatorios.json', 'w') as f:
    json.dump(datos_aleatorios, f, indent=4)
  d = d+1