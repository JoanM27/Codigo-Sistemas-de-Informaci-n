import random
import statistics
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Tuple
import matplotlib.pyplot as plt
import numpy as np


class SLAValidator:
    """
    Clase para validar métricas de servicio contra los SLAs definidos
    SLA de disponibilidad: 99.9%
    SLA de tiempo de respuesta: < 300 ms
    SLA de resolución de incidencias: >= 95%
    """

    def __init__(self):
        self.availability_threshold = 99.9  # 99.9% de disponibilidad
        self.response_time_threshold = 300  # 300 ms máximo
        self.incident_resolution_threshold = 95.0  # Porcentaje mínimo de incidencias resueltas
        self.metrics = {
            "availability": [],
            "response_times": [],
            "timestamps": [],
            "incidents": [],
        }

    def generate_sample_data(self, hours: int = 24) -> None:
        """
        Genera datos de muestra para simular métricas reales
        """
        print("Generando datos de muestra...")

        current_time = datetime.now()
        for i in range(hours * 60):  # Datos por minuto durante X horas
            timestamp = current_time - timedelta(minutes=i)

            # Simular disponibilidad (99.5% - 99.95% para hacerlo realista)
            availability = random.uniform(99.5, 99.95)

            # Simular tiempos de respuesta (250ms - 350ms con algunos picos)
            if random.random() < 0.05:  # 5% de probabilidad de pico
                response_time = random.uniform(350, 500)
            else:
                response_time = random.uniform(250, 320)

            self.metrics["availability"].append(availability)
            self.metrics["response_times"].append(response_time)
            self.metrics["timestamps"].append(timestamp)

            # Una incidencia representa un evento registrado durante la medición.
            # La mayoría se resuelve dentro de la ventana de reporte.
            if random.random() < 0.03:
                self.metrics["incidents"].append(
                    {
                        "id": f"INC-{i + 1:05d}",
                        "reported_at": timestamp,
                        "resolved": random.random() < 0.97,
                    }
                )

        # Invertir para tener datos cronológicos
        for key in ("availability", "response_times", "timestamps", "incidents"):
            self.metrics[key].reverse()

    def calculate_incident_resolution_compliance(self) -> Tuple[float, bool, int, int]:
        """Calcula la tasa de resolución de las incidencias registradas."""
        incidents = self.metrics["incidents"]
        total_incidents = len(incidents)
        resolved_incidents = sum(incident["resolved"] for incident in incidents)

        # Si no se registran incidencias, no queda ninguna sin resolver en el período.
        resolution_rate = 100.0 if total_incidents == 0 else (resolved_incidents / total_incidents) * 100
        complies = resolution_rate >= self.incident_resolution_threshold

        print(f"Tasa de resolución de incidencias: {resolution_rate:.2f}%")
        print(f"Incidencias resueltas: {resolved_incidents}/{total_incidents}")
        print(f"Umbral SLA: {self.incident_resolution_threshold}%")
        print(f"¿Cumple SLA? {'OK' if complies else 'No'}")

        return resolution_rate, complies, resolved_incidents, total_incidents

    def calculate_availability_compliance(self) -> Tuple[float, bool]:
        """
        Calcula el cumplimiento del SLA de disponibilidad
        Returns: (disponibilidad_promedio, cumple_sla)
        """
        if not self.metrics["availability"]:
            raise ValueError("No se han generado datos de disponibilidad")

        avg_availability = statistics.mean(self.metrics["availability"])
        complies = avg_availability >= self.availability_threshold

        print(f"Disponibilidad promedio: {avg_availability:.3f}%")
        print(f"Umbral SLA: {self.availability_threshold}%")
        print(f"¿Cumple SLA? {'OK' if complies else 'No'}")

        return avg_availability, complies

    def calculate_response_time_compliance(self) -> Tuple[float, float, bool]:
        """
        Calcula el cumplimiento del SLA de tiempo de respuesta
        Returns: (promedio, percentil_95, cumple_sla)
        """
        if not self.metrics["response_times"]:
            raise ValueError("No se han generado datos de tiempo de respuesta")

        avg_response = statistics.mean(self.metrics["response_times"])
        percentile_95 = float(np.percentile(self.metrics["response_times"], 95))

        # El SLA se cumple si el percentil 95 está por debajo del umbral
        complies = percentile_95 <= self.response_time_threshold

        print(f"Tiempo de respuesta promedio: {avg_response:.2f} ms")
        print(f"Percentil 95: {percentile_95:.2f} ms")
        print(f"Umbral SLA: {self.response_time_threshold} ms")
        print(f"¿Cumple SLA? {'OK' if complies else 'No'}")

        return avg_response, percentile_95, complies

    def identify_violations(self) -> Dict:
        """
        Identifica violaciones específicas de los SLAs
        """
        violations = {
            "availability_violations": [],
            "response_time_violations": [],
            "concurrent_violations": [],
            "unresolved_incidents": [],
        }

        for avail, resp_time, timestamp in zip(
            self.metrics["availability"],
            self.metrics["response_times"],
            self.metrics["timestamps"],
        ):
            # Verificar violaciones de disponibilidad
            if avail < self.availability_threshold:
                violations["availability_violations"].append(
                    {"timestamp": timestamp, "value": avail, "threshold": self.availability_threshold}
                )

            # Verificar violaciones de tiempo de respuesta
            if resp_time > self.response_time_threshold:
                violations["response_time_violations"].append(
                    {"timestamp": timestamp, "value": resp_time, "threshold": self.response_time_threshold}
                )

            # Verificar violaciones concurrentes
            if avail < self.availability_threshold and resp_time > self.response_time_threshold:
                violations["concurrent_violations"].append(
                    {"timestamp": timestamp, "availability": avail, "response_time": resp_time}
                )

        for incident in self.metrics["incidents"]:
            if not incident["resolved"]:
                violations["unresolved_incidents"].append(incident)

        return violations

    def generate_compliance_report(self) -> Dict:
        """
        Genera un reporte completo de cumplimiento de SLAs
        """
        print("\n" + "=" * 50)
        print("REPORTE DE CUMPLIMIENTO DE SLA")
        print("=" * 50)

        # Calcular métricas principales
        avg_availability, availability_complies = self.calculate_availability_compliance()
        avg_response, percentile_95, response_complies = self.calculate_response_time_compliance()
        resolution_rate, resolution_complies, resolved_incidents, total_incidents = (
            self.calculate_incident_resolution_compliance()
        )

        # Identificar violaciones
        violations = self.identify_violations()

        # Calcular porcentajes de cumplimiento
        total_samples = len(self.metrics["availability"])
        availability_compliance_rate = (1 - len(violations["availability_violations"]) / total_samples) * 100
        response_time_compliance_rate = (1 - len(violations["response_time_violations"]) / total_samples) * 100

        report = {
            "generated_at": datetime.now(),
            "overall_availability": {
                "value": avg_availability,
                "threshold": self.availability_threshold,
                "complies": availability_complies,
                "compliance_rate": availability_compliance_rate,
            },
            "response_time": {
                "average": avg_response,
                "percentile_95": percentile_95,
                "threshold": self.response_time_threshold,
                "complies": response_complies,
                "compliance_rate": response_time_compliance_rate,
            },
            "incident_resolution": {
                "resolution_rate": resolution_rate,
                "threshold": self.incident_resolution_threshold,
                "complies": resolution_complies,
                "resolved_incidents": resolved_incidents,
                "total_incidents": total_incidents,
            },
            "violations": violations,
            "summary": {
                "total_samples": total_samples,
                "overall_compliance": availability_complies and response_complies and resolution_complies,
                "availability_violation_count": len(violations["availability_violations"]),
                "response_time_violation_count": len(violations["response_time_violations"]),
                "concurrent_violation_count": len(violations["concurrent_violations"]),
                "unresolved_incident_count": len(violations["unresolved_incidents"]),
            },
        }

        # Imprimir resumen
        print(f"\nResumen de violaciones:")
        print(f"- Violaciones de disponibilidad: {report['summary']['availability_violation_count']}")
        print(f"- Violaciones de tiempo de respuesta: {report['summary']['response_time_violation_count']}")
        print(f"- Violaciones concurrentes: {report['summary']['concurrent_violation_count']}")
        print(f"- Incidencias sin resolver: {report['summary']['unresolved_incident_count']}")
        print(f"\nCumplimiento general del SLA: {'OK' if report['summary']['overall_compliance'] else 'No'}")

        return report

    @staticmethod
    def save_report_as_json(report: Dict, output_path: str = "reporte_cumplimiento_sla.json") -> Path:
        """Guarda el reporte en JSON, convirtiendo las fechas al formato ISO 8601."""
        destination = Path(output_path)
        with destination.open("w", encoding="utf-8") as file:
            json.dump(report, file, ensure_ascii=False, indent=2, default=lambda value: value.isoformat())

        print(f"Informe JSON generado: {destination.resolve()}")
        return destination

    def plot_metrics(self) -> None:
        """
        Genera gráficos para visualizar las métricas y el cumplimiento del SLA
        """
        if not self.metrics["timestamps"]:
            raise ValueError("No hay datos para graficar")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

        # Gráfico de disponibilidad
        ax1.plot(self.metrics["timestamps"], self.metrics["availability"], "b-", label="Disponibilidad")
        ax1.axhline(
            y=self.availability_threshold,
            color="r",
            linestyle="--",
            label=f"Umbral SLA ({self.availability_threshold}%)",
        )
        ax1.set_ylabel("Disponibilidad (%)")
        ax1.set_title("Disponibilidad del Servicio")
        ax1.legend()
        ax1.grid(True)

        # Gráfico de tiempo de respuesta
        ax2.plot(self.metrics["timestamps"], self.metrics["response_times"], "g-", label="Tiempo de respuesta")
        ax2.axhline(
            y=self.response_time_threshold,
            color="r",
            linestyle="--",
            label=f"Umbral SLA ({self.response_time_threshold} ms)",
        )
        ax2.set_ylabel("Tiempo de respuesta (ms)")
        ax2.set_xlabel("Tiempo")
        ax2.set_title("Tiempo de Respuesta del Servicio")
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()
        plt.show()


def main():
    """
    Función principal para demostrar el uso del validador de SLA
    """
    # Crear instancia del validador
    validator = SLAValidator()

    # Generar datos de muestra (24 horas de datos por minuto)
    validator.generate_sample_data(hours=24)

    # Generar reporte de cumplimiento
    report = validator.generate_compliance_report()

    # Guardar también el informe estructurado para integrarlo con otros sistemas.
    validator.save_report_as_json(report)

    # Mostrar gráficos
    validator.plot_metrics()

    # Análisis adicional
    print("\n" + "=" * 50)
    print("ANÁLISIS DETALLADO")
    print("=" * 50)

    # Mostrar algunas violaciones específicas si existen
    if report["violations"]["availability_violations"]:
        print(f"\nPrimera violación de disponibilidad:")
        violation = report["violations"]["availability_violations"][0]
        print(f"  Hora: {violation['timestamp']}")
        print(f"  Valor: {violation['value']:.3f}%")
        print(f"  Umbral: {violation['threshold']}%")

    if report["violations"]["response_time_violations"]:
        print(f"\nPrimera violación de tiempo de respuesta:")
        violation = report["violations"]["response_time_violations"][0]
        print(f"  Hora: {violation['timestamp']}")
        print(f"  Valor: {violation['value']:.2f} ms")
        print(f"  Umbral: {violation['threshold']} ms")

    # Recomendaciones basadas en el análisis
    print(f"\nRecomendaciones:")
    if not report["overall_availability"]["complies"]:
        print("Mejorar la disponibilidad del servicio")
    if not report["response_time"]["complies"]:
        print("Optimizar el tiempo de respuesta")
    if not report["incident_resolution"]["complies"]:
        print("Reducir el backlog y priorizar la resolución de incidencias abiertas")
    if report["summary"]["overall_compliance"]:
        print("El servicio cumple con todos los SLAs")
    else:
        print("Se requieren acciones correctivas")


if __name__ == "__main__":
    main()
