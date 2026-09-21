# metricas_servidor.pyExplicación:

#Se generan datos aleatorios que simulan el consumo de CPU, RAM y almacenamiento.

#Se usa pandas para organizar los datos en un DataFrame.

#Se grafican las métricas en el tiempo con matplotlib, incluyendo un umbral crítico del 80%.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Simulamos 50 mediciones de un servidor
np.random.seed(42)  # Para resultados reproducibles
tiempo = pd.date_range(start="2025-01-01", periods=50, freq="T")  # 50 minutos
cpu = np.random.randint(10, 95, size=50)  # Consumo CPU %
ram = np.random.randint(20, 90, size=50)  # Consumo RAM %
almacenamiento = np.random.randint(30, 80, size=50)  # Uso de disco %

# Creamos un DataFrame con las métricas
df = pd.DataFrame({
    "Tiempo": tiempo,
    "CPU (%)": cpu,
    "RAM (%)": ram,
    "Almacenamiento (%)": almacenamiento
})

# --- Visualización ---
plt.figure(figsize=(10,6))
plt.plot(df["Tiempo"], df["CPU (%)"], label="CPU")
plt.plot(df["Tiempo"], df["RAM (%)"], label="RAM")
plt.plot(df["Tiempo"], df["Almacenamiento (%)"], label="Almacenamiento")
plt.axhline(y=80, color="r", linestyle="--", label="Umbral Crítico (80%)") # línea de umbral
plt.title("Monitoreo de métricas del servidor")
plt.xlabel("Tiempo")
plt.ylabel("Uso (%)")
plt.legend()
plt.grid(True)
plt.show()



# Definimos el umbral
umbral = 80

# Filtramos los registros que superan el umbral
alertas = df[(df["CPU (%)"] > umbral) | (df["RAM (%)"] > umbral) | (df["Almacenamiento (%)"] > umbral)]

print("⚠️ ALERTAS DETECTADAS ⚠️")
print(alertas)

# --- Visualización de alertas ---
plt.figure(figsize=(10,6))
plt.plot(df["Tiempo"], df["CPU (%)"], label="CPU", color="blue")
plt.plot(df["Tiempo"], df["RAM (%)"], label="RAM", color="green")
plt.plot(df["Tiempo"], df["Almacenamiento (%)"], label="Almacenamiento", color="orange")

# Resaltamos las alertas en rojo
plt.scatter(alertas["Tiempo"], alertas["CPU (%)"], color="red", label="CPU alerta")
plt.scatter(alertas["Tiempo"], alertas["RAM (%)"], color="red", label="RAM alerta")
plt.scatter(alertas["Tiempo"], alertas["Almacenamiento (%)"], color="red", label="Almacenamiento alerta")

plt.axhline(y=umbral, color="r", linestyle="--", label="Umbral crítico (80%)")
plt.title("Alertas de monitoreo de servidores")
plt.xlabel("Tiempo")
plt.ylabel("Uso (%)")
plt.legend()
plt.grid(True)
plt.show()
