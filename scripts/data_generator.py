#Construir un json con datos aleatorios
import json
import random
import sys
import os

# Obtener la ruta de la carpeta 'atmos-app' Y subir un nivel desde 'scripts'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Añadir BASE_DIR al principio de la lista de búsqueda de Python
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.alerts import evaluar_alerta

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
    	"temperatura": round(random.uniform(-15, 50), 1),
    	"humedad_nivel": round(random.uniform(0, 100), 1),
    	"viento_velocidad": round(random.uniform(0, 130), 1)
    }
    
    datos_aleatorios.update(evaluar_alerta(datos_aleatorios))
    datos.append(datos_aleatorios)

# 3. Guardar todos los datos generados en un archivo con permisos de escritura (w)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "data.json")
with open(DATA_PATH, 'w') as f:
    json.dump(datos, f, indent=4)