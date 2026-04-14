import json
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta, datetime

# --- 1. GENERACIÓN DE DATOS (Tu lógica vinculada y corregida) ---
inicio = datetime(2000, 1, 1)
fin = datetime.now()

def fecha_aleatoria(inicio, fin):
    delta = fin - inicio
    dias = random.randint(0, delta.days)
    fecha = inicio + timedelta(days=dias)
    return fecha.strftime("%Y-%m-%d")

datos = []
combinaciones_usadas = set()

print("Generando datos...")
while len(datos) < 100:
    fecha = fecha_aleatoria(inicio, fin)
    zona = random.choice(["norte", "sur", "centro"])
    clave = (fecha, zona) 
    
    if clave not in combinaciones_usadas: 
        combinaciones_usadas.add(clave)
        registro = {
            "fecha_registro": fecha,
            "zona_registro": zona,
            "temperatura": round(random.uniform(-15, 50), 2),
            "humedad_nivel": round(random.uniform(0, 100), 2),
            "viento_velocidad": round(random.uniform(0, 130), 2),
            "alerta_temperatura": random.choice([True, False]),
            "alerta_humedad": random.choice([True, False]),
            "alerta_viento": random.choice([True, False])
        }
        datos.append(registro)

# Guardar en JSON
with open('datos_aleatorios.json', 'w') as f:
    json.dump(datos, f, indent=4)

# --- 2. VÍNCULO CON PANDAS Y ANÁLISIS ---
# Leemos el archivo recién creado
df = pd.read_json('datos_aleatorios.json')
df['fecha_registro'] = pd.to_datetime(df['fecha_registro'])

# Estadísticas básicas (Media por zona)
print("\n--- ESTADÍSTICAS BÁSICAS (MEDIAS POR ZONA) ---")
resumen = df.groupby('zona_registro')[['temperatura', 'humedad_nivel', 'viento_velocidad']].mean()
print(resumen.round(2))

# --- 3. VISUALIZACIÓN (Sin avisos de error/FutureWarning) ---
plt.figure(figsize=(14, 6))

# Gráfica 1: Temperatura Media por Zona
plt.subplot(1, 2, 1)
sns.barplot(
    data=df, 
    x='zona_registro', 
    y='temperatura', 
    hue='zona_registro', # Asignamos hue para evitar el aviso
    palette='coolwarm', 
    estimator='mean',
    legend=False        # Quitamos la leyenda porque el eje X ya lo explica
)
plt.title('Estadística: Temperatura Media por Zona')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Gráfica 2: Dispersión del Viento por Zona
plt.subplot(1, 2, 2)
sns.boxplot(
    data=df, 
    x='zona_registro', 
    y='viento_velocidad', 
    hue='zona_registro', # Asignamos hue para evitar el aviso
    palette='viridis',
    legend=False
)
plt.title('Distribución de Velocidad del Viento')

plt.tight_layout()
plt.show()