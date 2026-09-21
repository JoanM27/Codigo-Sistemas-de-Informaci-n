# identificacion_alertas_fix.py

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

# ------------------------------------------------------------------
# 0) Intento de forzar la salida UTF-8 para evitar UnicodeEncodeError
#    (funciona en Python 3.7+ en muchas consolas). Si falla, se ignora.
# ------------------------------------------------------------------
try:
    # Reconfigure stdout to use UTF-8 (y reemplazar caracteres inválidos si los hay)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    # Algunos entornos no permiten reconfigure; en ese caso continuamos
    # y usaremos un fallback al imprimir el mensaje de alerta.
    pass

# ------------------------------------------------------------------
# 1) Generación de datos simulados (DataFrame con métricas del servidor)
# ------------------------------------------------------------------
np.random.seed(42)  # reproducibilidad

# Usar 'min' en lugar de 'T' para evitar la FutureWarning
tiempo = pd.date_range(start="2025-01-01", periods=50, freq="min")

cpu = np.random.randint(10, 95, size=50)            # CPU en %
ram = np.random.randint(20, 90, size=50)            # RAM en %
almacenamiento = np.random.randint(30, 80, size=50) # Disco en %

df = pd.DataFrame({
    "Tiempo": tiempo,
    "CPU (%)": cpu,
    "RAM (%)": ram,
    "Almacenamiento (%)": almacenamiento
})

# ------------------------------------------------------------------
# 2) Detección de alertas según umbral
# ------------------------------------------------------------------
umbral = 80

# Filtramos filas donde alguna métrica supere el umbral
alertas = df[
    (df["CPU (%)"] > umbral) |
    (df["RAM (%)"] > umbral) |
    (df["Almacenamiento (%)"] > umbral)
]

# ------------------------------------------------------------------
# 3) Impresión segura del mensaje de alerta (manejo de Unicode)
# ------------------------------------------------------------------
alert_msg = "ALERTAS DETECTADAS"

# Intentamos imprimir el mensaje con emojis; si falla por codificación,
# imprimimos una versión sin emojis para evitar que el script se corte.
try:
    print(alert_msg)
except UnicodeEncodeError:
    # Fallback: mensaje sin caracteres Unicode no soportados
    print("ALERTAS DETECTADAS")

# Mostramos el DataFrame de alertas (esto no suele lanzar UnicodeEncodeError)
print(alertas)

# ------------------------------------------------------------------
# 4) Visualización: métricas y puntos resaltados para alertas
# ------------------------------------------------------------------
plt.figure(figsize=(10, 6))
plt.plot(df["Tiempo"], df["CPU (%)"], label="CPU", color="blue")
plt.plot(df["Tiempo"], df["RAM (%)"], label="RAM", color="green")
plt.plot(df["Tiempo"], df["Almacenamiento (%)"], label="Almacenamiento", color="orange")

# Si hay alertas, las marcamos; si 'alertas' está vacío, scatter acepta arrays vacíos
plt.scatter(alertas["Tiempo"], alertas["CPU (%)"], color="red", label="CPU alerta")
plt.scatter(alertas["Tiempo"], alertas["RAM (%)"], color="red", label="RAM alerta")
plt.scatter(alertas["Tiempo"], alertas["Almacenamiento (%)"], color="red", label="Almacenamiento alerta")

# Línea del umbral
plt.axhline(y=umbral, color="red", linestyle="--", label="Umbral crítico (80%)")

plt.title("Alertas de monitoreo de servidores")
plt.xlabel("Tiempo")
plt.ylabel("Uso (%)")
plt.legend()
plt.grid(True)
plt.show()
