import time
import random
import statistics
from datetime import datetime, timedelta
from typing import List, Dict
import matplotlib.pyplot as plt
import numpy as np
import threading

class ServerMonitor:
    """
    Sistema de monitoreo de servidores con alertas basadas en umbrales
    """
    
    def __init__(self):
        # Umbrales de alerta (configurables)
        self.thresholds = {
            'cpu': 80.0,        # % de uso de CPU
            'memory': 85.0,     # % de uso de memoria
            'storage': 90.0,    # % de uso de almacenamiento
            'temperature': 70.0, # °C temperatura del CPU
            'network_latency': 100.0, # ms de latencia de red
        }
        
        # Métricas históricas
        self.metrics = {
            'timestamps': [],
            'cpu_usage': [],
            'memory_usage': [],
            'storage_usage': [],
            'temperature': [],
            'network_latency': [],
            'server_status': []  # 'online', 'offline', 'degraded'
        }
        
        # Alertas activas
        self.active_alerts = {
            'cpu': [],
            'memory': [],
            'storage': [],
            'temperature': [],
            'network': [],
            'server_down': []
        }
        
        # Configuración de servidores (simulados)
        self.servers = {
            'web-server-01': {'ip': '192.168.1.10', 'type': 'web', 'status': 'online'},
            'db-server-01': {'ip': '192.168.1.20', 'type': 'database', 'status': 'online'},
            'app-server-01': {'ip': '192.168.1.30', 'type': 'application', 'status': 'online'},
            'cache-server-01': {'ip': '192.168.1.40', 'type': 'cache', 'status': 'online'}
        }
        
        # Estado del monitoreo
        self.monitoring_active = False
        self.monitoring_thread = None
        
    def generate_server_metrics(self, server_name: str) -> Dict:
        """
        Genera métricas simuladas para un servidor específico
        """
        server_type = self.servers[server_name]['type']
        
        # Patrones de uso basados en el tipo de servidor
        if server_type == 'web':
            base_cpu = random.uniform(30, 60)
            base_memory = random.uniform(40, 70)
        elif server_type == 'database':
            base_cpu = random.uniform(20, 50)
            base_memory = random.uniform(50, 80)
        elif server_type == 'application':
            base_cpu = random.uniform(40, 70)
            base_memory = random.uniform(35, 65)
        else:  # cache
            base_cpu = random.uniform(10, 40)
            base_memory = random.uniform(20, 50)
        
        # Simular picos aleatorios (5% de probabilidad)
        if random.random() < 0.05:
            cpu_spike = random.uniform(20, 40)
            memory_spike = random.uniform(15, 30)
        else:
            cpu_spike = 0
            memory_spike = 0
        
        metrics = {
            'timestamp': datetime.now(),
            'server': server_name,
            'cpu_usage': min(100, base_cpu + cpu_spike),
            'memory_usage': min(100, base_memory + memory_spike),
            'storage_usage': random.uniform(60, 95),
            'temperature': random.uniform(40, 75),
            'network_latency': random.uniform(10, 150),
            'status': self.servers[server_name]['status']
        }
        
        return metrics
    
    def check_thresholds(self, metrics: Dict) -> List[Dict]:
        """
        Verifica si las métricas exceden los umbrales definidos
        """
        alerts = []
        
        if metrics['cpu_usage'] > self.thresholds['cpu']:
            alerts.append({
                'type': 'cpu',
                'server': metrics['server'],
                'value': metrics['cpu_usage'],
                'threshold': self.thresholds['cpu'],
                'timestamp': metrics['timestamp'],
                'severity': 'high' if metrics['cpu_usage'] > 90 else 'warning'
            })
        
        if metrics['memory_usage'] > self.thresholds['memory']:
            alerts.append({
                'type': 'memory',
                'server': metrics['server'],
                'value': metrics['memory_usage'],
                'threshold': self.thresholds['memory'],
                'timestamp': metrics['timestamp'],
                'severity': 'high' if metrics['memory_usage'] > 95 else 'warning'
            })
        
        if metrics['storage_usage'] > self.thresholds['storage']:
            alerts.append({
                'type': 'storage',
                'server': metrics['server'],
                'value': metrics['storage_usage'],
                'threshold': self.thresholds['storage'],
                'timestamp': metrics['timestamp'],
                'severity': 'high' if metrics['storage_usage'] > 95 else 'warning'
            })
        
        if metrics['temperature'] > self.thresholds['temperature']:
            alerts.append({
                'type': 'temperature',
                'server': metrics['server'],
                'value': metrics['temperature'],
                'threshold': self.thresholds['temperature'],
                'timestamp': metrics['timestamp'],
                'severity': 'critical' if metrics['temperature'] > 80 else 'high'
            })
        
        if metrics['network_latency'] > self.thresholds['network_latency']:
            alerts.append({
                'type': 'network',
                'server': metrics['server'],
                'value': metrics['network_latency'],
                'threshold': self.thresholds['network_latency'],
                'timestamp': metrics['timestamp'],
                'severity': 'high' if metrics['network_latency'] > 200 else 'warning'
            })
        
        if metrics['status'] == 'offline':
            alerts.append({
                'type': 'server_down',
                'server': metrics['server'],
                'value': 'offline',
                'threshold': 'online',
                'timestamp': metrics['timestamp'],
                'severity': 'critical'
            })
        
        return alerts
    
    def simulate_server_failure(self):
        """
        Simula fallos aleatorios en servidores (para testing)
        """
        if random.random() < 0.02:
            server_name = random.choice(list(self.servers.keys()))
            if self.servers[server_name]['status'] == 'online':
                self.servers[server_name]['status'] = 'offline'
                print(f"SIMULATED FAILURE: {server_name} is now offline!")
                
                recovery_time = random.randint(60, 300)
                threading.Timer(recovery_time, self.recover_server, [server_name]).start()
    
    def recover_server(self, server_name: str):
        if server_name in self.servers:
            self.servers[server_name]['status'] = 'online'
            print(f"SERVER RECOVERED: {server_name} is back online!")
    
    def monitor_servers(self, interval: int = 60):
        while self.monitoring_active:
            try:
                self.simulate_server_failure()
                
                for server_name in self.servers.keys():
                    metrics = self.generate_server_metrics(server_name)
                    
                    self.metrics['timestamps'].append(metrics['timestamp'])
                    self.metrics['cpu_usage'].append(metrics['cpu_usage'])
                    self.metrics['memory_usage'].append(metrics['memory_usage'])
                    self.metrics['storage_usage'].append(metrics['storage_usage'])
                    self.metrics['temperature'].append(metrics['temperature'])
                    self.metrics['network_latency'].append(metrics['network_latency'])
                    self.metrics['server_status'].append(metrics['status'])
                    
                    alerts = self.check_thresholds(metrics)
                    for alert in alerts:
                        self.active_alerts[alert['type']].append(alert)
                        self.print_alert(alert)
                
                self.trim_metrics()
                time.sleep(interval)
                
            except Exception as e:
                print(f"Error en el monitoreo: {e}")
                time.sleep(interval)
    
    def trim_metrics(self):
        max_entries = 1000
        for key in self.metrics.keys():
            if len(self.metrics[key]) > max_entries:
                self.metrics[key] = self.metrics[key][-max_entries:]
    
    def print_alert(self, alert: Dict):
        colors = {
            'warning': '\033[93m',
            'high': '\033[91m',
            'critical': '\033[95m'
        }
        
        color = colors.get(alert['severity'], '\033[0m')
        reset = '\033[0m'
        
        print(f"{color} ALERTA [{alert['severity'].upper()}] {alert['type']} on {alert['server']}")
        print(f"   Valor: {alert['value']} | Umbral: {alert['threshold']}")
        print(f"   Hora: {alert['timestamp']}{reset}")
    
    def start_monitoring(self, interval: int = 60):
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(
                target=self.monitor_servers, 
                args=(interval,),
                daemon=True
            )
            self.monitoring_thread.start()
            print(f"Monitoreo iniciado con intervalo de {interval} segundos")
    
    def stop_monitoring(self):
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        print("Monitoreo detenido")
    
    def get_current_status(self) -> Dict:
        if not self.metrics['timestamps']:
            return {'status': 'no_data'}
        
        recent_samples = min(10, len(self.metrics['cpu_usage']))
        
        status = {
            'timestamp': datetime.now(),
            'servers_online': sum(1 for status in self.metrics['server_status'][-recent_samples:] 
                                if status == 'online'),
            'total_servers': len(self.servers),
            'avg_cpu': statistics.mean(self.metrics['cpu_usage'][-recent_samples:]),
            'avg_memory': statistics.mean(self.metrics['memory_usage'][-recent_samples:]),
            'avg_storage': statistics.mean(self.metrics['storage_usage'][-recent_samples:]),
            'active_alerts': sum(len(alerts) for alerts in self.active_alerts.values()),
            'alerts_by_type': {key: len(alerts) for key, alerts in self.active_alerts.items()}
        }
        
        return status
    
    def print_status_report(self):
        status = self.get_current_status()
        
        print("\n" + "="*60)
        print(" REPORTE DE ESTADO DEL SISTEMA")
        print("="*60)
        print(f" Hora del reporte: {status['timestamp']}")
        print(f"  Servidores: {status['servers_online']}/{status['total_servers']} online")
        print(f" CPU promedio: {status['avg_cpu']:.1f}%")
        print(f" Memoria promedio: {status['avg_memory']:.1f}%")
        print(f" Almacenamiento promedio: {status['avg_storage']:.1f}%")
        print(f" Alertas activas: {status['active_alerts']}")
        
        if status['active_alerts'] > 0:
            print("\nAlertas por tipo:")
            for alert_type, count in status['alerts_by_type'].items():
                if count > 0:
                    print(f"   - {alert_type}: {count} alertas")
        
        print("="*60)
    
    def plot_metrics_history(self, hours: int = 1):
        if not self.metrics['timestamps']:
            print("No hay datos para graficar")
            return
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        indices = [i for i, ts in enumerate(self.metrics['timestamps']) 
                  if ts >= cutoff_time]
        
        if not indices:
            print(f"No hay datos de las últimas {hours} horas")
            return
        
        timestamps = [self.metrics['timestamps'][i] for i in indices]
        cpu_data = [self.metrics['cpu_usage'][i] for i in indices]
        memory_data = [self.metrics['memory_usage'][i] for i in indices]
        storage_data = [self.metrics['storage_usage'][i] for i in indices]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        ax1.plot(timestamps, cpu_data, 'r-', label='Uso de CPU', linewidth=1)
        ax1.axhline(y=self.thresholds['cpu'], color='r', linestyle='--', 
                   label=f'Umbral ({self.thresholds["cpu"]}%)')
        ax1.set_ylabel('Uso de CPU (%)')
        ax1.set_title('Uso de CPU por Servidores')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        ax2.plot(timestamps, memory_data, 'b-', label='Uso de Memoria', linewidth=1)
        ax2.axhline(y=self.thresholds['memory'], color='b', linestyle='--', 
                   label=f'Umbral ({self.thresholds["memory"]}%)')
        ax2.set_ylabel('Uso de Memoria (%)')
        ax2.set_title('Uso de Memoria por Servidores')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)
        
        ax3.plot(timestamps, storage_data, 'g-', label='Uso de Almacenamiento', linewidth=1)
        ax3.axhline(y=self.thresholds['storage'], color='g', linestyle='--', 
                   label=f'Umbral ({self.thresholds["storage"]}%)')
        ax3.set_ylabel('Uso de Almacenamiento (%)')
        ax3.set_xlabel('Tiempo')
        ax3.set_title('Uso de Almacenamiento por Servidores')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.tick_params(axis='x', rotation=45)
        
        status_mapping = {'online': 1, 'offline': 0, 'degraded': 0.5}
        status_data = [status_mapping.get(status, 0) 
                      for status in self.metrics['server_status'][-len(indices):]]
        
        ax4.step(timestamps, status_data, 'k-', where='post', label='Estado')
        ax4.set_ylabel('Estado (1=Online, 0.5=Degradado, 0=Offline)')
        ax4.set_xlabel('Tiempo')
        ax4.set_title('Estado de los Servidores')
        ax4.set_yticks([0, 0.5, 1])
        ax4.set_yticklabels(['Offline', 'Degradado', 'Online'])
        ax4.grid(True, alpha=0.3)
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def plot_additional_metrics(self):
        """
        Gráficas adicionales para explorar mejor las métricas recolectadas
        """
        if not self.metrics['timestamps']:
            print("No hay datos para graficar")
            return

        cpu_data = np.array(self.metrics['cpu_usage'])
        memory_data = np.array(self.metrics['memory_usage'])
        storage_data = np.array(self.metrics['storage_usage'])

        fig, axs = plt.subplots(3, 2, figsize=(15, 12))

        axs[0, 0].hist(cpu_data, bins=20, color='red', alpha=0.7)
        axs[0, 0].axvline(self.thresholds['cpu'], color='r', linestyle='--', label="Umbral")
        axs[0, 0].set_title("Distribución del uso de CPU (%)")
        axs[0, 0].legend()

        axs[0, 1].hist(memory_data, bins=20, color='blue', alpha=0.7)
        axs[0, 1].axvline(self.thresholds['memory'], color='b', linestyle='--', label="Umbral")
        axs[0, 1].set_title("Distribución del uso de Memoria (%)")
        axs[0, 1].legend()

        axs[1, 0].hist(storage_data, bins=20, color='green', alpha=0.7)
        axs[1, 0].axvline(self.thresholds['storage'], color='g', linestyle='--', label="Umbral")
        axs[1, 0].set_title("Distribución del uso de Almacenamiento (%)")
        axs[1, 0].legend()

        axs[1, 1].scatter(cpu_data, memory_data, alpha=0.6, c='purple')
        axs[1, 1].set_xlabel("CPU (%)")
        axs[1, 1].set_ylabel("Memoria (%)")
        axs[1, 1].set_title("Relación CPU vs Memoria")

        window = 20 if len(cpu_data) > 20 else len(cpu_data)
        rolling_avg = np.convolve(cpu_data, np.ones(window)/window, mode='valid')
        axs[2, 0].plot(cpu_data, label="CPU")
        axs[2, 0].plot(range(window-1, len(cpu_data)), rolling_avg, label=f"Promedio móvil ({window})", color="orange")
        axs[2, 0].set_title("Promedio móvil de CPU")
        axs[2, 0].legend()

        alert_counts = {k: len(v) for k, v in self.active_alerts.items()}
        axs[2, 1].bar(alert_counts.keys(), alert_counts.values(), color='brown', alpha=0.7)
        axs[2, 1].set_title("Número de alertas por tipo")
        axs[2, 1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.show()

def main():
    monitor = ServerMonitor()
    
    try:
        monitor.start_monitoring(interval=30)
        
        print("Sistema de monitoreo de servidores iniciado")
        print("Presiona Ctrl+C para detener el monitoreo y ver reportes")
        print("\nUmbrales configurados:")
        for metric, threshold in monitor.thresholds.items():
            print(f"  - {metric}: {threshold}")
        
        time.sleep(120)
        monitor.print_status_report()
        
        while True:
            time.sleep(60)
            monitor.print_status_report()
            
    except KeyboardInterrupt:
        print("\n\nDeteniendo monitoreo...")
        monitor.stop_monitoring()
        
        print("\n" + "="*60)
        print("REPORTE FINAL")
        print("="*60)
        monitor.print_status_report()
        
        print("\nGenerando gráficos de las últimas 2 horas...")
        monitor.plot_metrics_history(hours=2)

        print("\nGenerando gráficas adicionales...")
        monitor.plot_additional_metrics()

if __name__ == "__main__":
    main()
