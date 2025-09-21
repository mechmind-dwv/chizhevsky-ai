#!/usr/bin/env python3
"""
🔬 MONITOR DE SALUD CHIZHEVSKY - Versión Python
Monitor robusto con manejo de errores y parsing adecuado de JSON
"""
import requests
import time
from datetime import datetime
import json

class HealthMonitor:
    def __init__(self, base_url="http://localhost:27779"):
        self.base_url = base_url
        self.solar_history = []
        self.max_history = 20
        
    def get_data(self, endpoint):
        """Obtener datos de un endpoint con manejo de errores"""
        try:
            response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error conectando con {endpoint}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Error parseando JSON de {endpoint}: {e}")
            return None
    
    def update_display(self, metrics, health_data):
        """Actualizar la visualización con nuevos datos"""
        if not metrics or not health_data:
            return
            
        solar_activity = health_data.get('solar_activity', 0)
        emergency_level = health_data.get('emergency_level', 'UNKNOWN')
        bed_occupancy = metrics.get('bed_occupancy', 0)
        critical_cases = metrics.get('critical_cases', 0)
        
        # Añadir a historial
        self.solar_history.append(solar_activity)
        if len(self.solar_history) > self.max_history:
            self.solar_history.pop(0)
        
        # Limpiar pantalla (funciona en la mayoría de terminales)
        print("\033[H\033[J", end="")
        
        print("🔬 MONITOR DE SALUD CHIZHEVSKY - TIEMPO REAL")
        print("===========================================")
        print(f"🕐 Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Mostrar métricas principales
        print(f"🌞 ACTIVIDAD SOLAR: {solar_activity:.2f}")
        print(f"🚨 NIVEL EMERGENCIA: {emergency_level}")
        print(f"🏥 CAMAS OCUPADAS: {bed_occupancy}%")
        print(f"💔 CASOS CRÍTICOS: {critical_cases}")
        print()
        
        # Gráfico ASCII de actividad solar
        print("📈 HISTORIAL ACTIVIDAD SOLAR:")
        max_value = max(self.solar_history) if self.solar_history else 10
        for value in self.solar_history[-15:]:  # Mostrar últimos 15 valores
            bar_length = int((value / max_value) * 40) if max_value > 0 else 0
            bar = "█" * bar_length
            print(f"{value:5.2f} | {bar}")
        
        print()
        
        # Alertas
        if solar_activity > 7.0:
            print("⚠️  ALERTA ROJA: Alta actividad solar detectada!")
            print(f"   📈 Se esperan {int(solar_activity * 8)} casos de emergencia")
            print(f"   🩸 Se necesitan {int(solar_activity * 15 + 80)} unidades de sangre")
            print("   🚑 Activar protocolos de emergencia")
        elif solar_activity > 5.0:
            print("⚠️  ALERTA AMARILLA: Actividad solar moderada")
            print("   📋 Monitorizar pacientes de riesgo")
        
        if bed_occupancy > 85.0:
            print("⚠️  ALERTA HOSPITALARIA: Alta ocupación de camas")
            print("   🏨 Considerar habilitar camas adicionales")
        
        print()
        print("🔄 Actualizando cada 30 segundos... (Ctrl+C para salir)")
    
    def run(self):
        """Ejecutar el monitor continuamente"""
        print("Iniciando monitor de salud cósmica...")
        print("Conectando con servidor en", self.base_url)
        
        try:
            while True:
                # Obtener datos
                metrics = self.get_data('/cosmic-api/hospital/metrics')
                health_data = self.get_data('/cosmic-api/health-status')
                
                # Actualizar display
                self.update_display(metrics, health_data)
                
                # Esperar antes de la próxima actualización
                time.sleep(30)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitor detenido por el usuario")
        except Exception as e:
            print(f"💥 Error crítico en el monitor: {e}")

if __name__ == "__main__":
    monitor = HealthMonitor()
    monitor.run()
