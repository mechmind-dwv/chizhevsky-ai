# chizhevsky_ai/galactic_monitoring/galactic_monitor.py
"""
Monitor galáctico para seguimiento de actividad solar-terrestre
"""
import requests
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("GalacticMonitor")

class GalacticMonitor:
    def __init__(self):
        self.current_cycle = 25
        self.monitoring_start = datetime.now()
    
    def get_historical_solar_data(self):
        """Obtener datos solares históricos de múltiples fuentes"""
        # Simulación de datos históricos (en producción se conectaría a APIs)
        historical_data = {
            'years': list(range(1750, 2024)),
            'sunspots': [np.random.randint(10, 200) for _ in range(274)],
            'solar_flares': [np.random.randint(0, 50) for _ in range(274)],
            'geomagnetic_storms': [np.random.randint(0, 30) for _ in range(274)]
        }
        return historical_data
    
    def get_modern_solar_data(self):
        """Obtener datos solares modernos de APIs"""
        try:
            # Intenta obtener datos reales
            response = requests.get(
                "https://services.swpc.noaa.gov/json/solar_summary.json",
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
        except:
            logger.warning("⚠️ No se pudo conectar a API NOAA, usando datos simulados")
        
        # Datos simulados como fallback
        return {
            'sunspots': np.random.randint(50, 150),
            'solar_flares': np.random.randint(0, 20),
            'geomagnetic_activity': np.random.randint(0, 9)
        }
    
    def calculate_historical_patterns(self):
        """Calcular patrones históricos de actividad solar"""
        data = self.get_historical_solar_data()
        
        # Análisis de ciclos de 11 años (promedio)
        cycles = []
        for i in range(0, len(data['years']), 11):
            cycle_data = data['sunspots'][i:i+11]
            if len(cycle_data) == 11:
                cycles.append({
                    'start_year': data['years'][i],
                    'end_year': data['years'][i+10],
                    'max_sunspots': max(cycle_data),
                    'avg_sunspots': sum(cycle_data) / len(cycle_data)
                })
        
        return cycles
    
    def monitor_current_activity(self):
        """Monitorear actividad solar actual"""
        current_data = self.get_modern_solar_data()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'sunspots': current_data.get('sunspots', 0),
            'solar_flares': current_data.get('solar_flares', 0),
            'geomagnetic_activity': current_data.get('geomagnetic_activity', 0),
            'cycle': self.current_cycle,
            'status': self._assess_solar_status(current_data)
        }
    
    def _assess_solar_status(self, data):
        """Evaluar el estado solar actual"""
        if data.get('solar_flares', 0) > 15:
            return "HIGH_ACTIVITY"
        elif data.get('sunspots', 0) > 100:
            return "MODERATE_ACTIVITY"
        else:
            return "LOW_ACTIVITY"
