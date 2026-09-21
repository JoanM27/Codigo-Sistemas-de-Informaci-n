# Validador de SLA

`simulacion1.py` simula mediciones por minuto y valida tres indicadores de nivel de servicio:

| Métrica | Regla de cumplimiento | Umbral |
| --- | --- | --- |
| Disponibilidad | Promedio de disponibilidad igual o superior al objetivo | 99,9 % |
| Tiempo de respuesta | Percentil 95 igual o inferior al objetivo | 300 ms |
| Tasa de resolución de incidencias | Incidencias resueltas / incidencias registradas | 95 % |

Además de imprimir el resumen en consola, la ejecución crea `reporte_cumplimiento_sla.json`. Las marcas de tiempo se escriben en ISO 8601, por lo que el reporte se puede consumir desde otro sistema.

## Justificación de los umbrales

- **99,9 % de disponibilidad** permite alrededor de 43 minutos de indisponibilidad mensual (en un mes de 30 días). Es un objetivo exigente pero alcanzable con redundancia básica, monitoreo continuo y mantenimiento planificado.
- **300 ms en el percentil 95** protege la experiencia de casi todos los usuarios sin imponer que cada solicitud individual sea perfecta. Deja margen para picos breves y operaciones más costosas, que se identifican como incidencias para su corrección.
- **95 % de resolución** exige resolver al menos 95 de cada 100 incidencias del período. El 5 % restante reconoce casos que requieren proveedores, análisis de causa raíz o cambios programados; por ello es más operativo y realista que exigir el 100 %.

Si no se registra ninguna incidencia, la tasa de resolución se reporta como 100 %, pues no existen incidencias abiertas en el período.

## Ejecución

```powershell
python simulacion1.py
```

El script abre gráficos al finalizar la generación del informe. El archivo JSON queda en el mismo directorio desde el que se ejecuta el comando.
