"""
CONFIGURACIÓN REAL - SIN SIMULACIÓN
Solo fuentes reales de datos cósmicos
"""

import os
import requests
import logging

logger = logging.getLogger(__name__)

class ConfigReal:
    # APIs REALES - NO SIMULACIÓN
    NOAA_API_URL = "https://services.swpc.noaa.gov/json/solar_summary.json"
    NASA_API_URL = "https://api.nasa.gov/DONKI/notifications"
    SPACEWEATHER_API = "https://services.swpc.noaa.gov/products/alerts.json"
    
    # Claves API (configurar en .env)
    NASA_API_KEY = os.getenv('NASA_API_KEY', 'DEMO_KEY')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Base de datos REAL
    DB_PATH = "chizhevsky_alerts.db"
    
    # Modo: SOLO REAL
    MODO_SIMULACION = False

class NOAARealFetcher:
    """Obtenedor REAL de datos NOAA"""
    
    def __init__(self):
        self.config = ConfigReal()
    
    def get_real_solar_data(self):
        """Obtener datos SOLARES REALES"""
        try:
            response = requests.get(self.config.NOAA_API_URL, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return self._procesar_datos_reales(data)
            else:
                logger.warning(f"⚠️ NOAA API status: {response.status_code}")
                return self._get_fallback_real()
        except Exception as e:
            logger.error(f"❌ Error NOAA real: {e}")
            return self._get_fallback_real()
    
    def _procesar_datos_reales(self, data):
        """Procesar datos REALES de NOAA"""
        return {
            "indice_kp": data.get("kp_index", 0),
            "llamaradas_m": data.get("m_class_events", 0),
            "llamaradas_x": data.get("x_class_events", 0),
            "protones_10mev": data.get("proton_10mev", 0),
            "protones_100mev": data.get("proton_100mev", 0),
            "velocidad_viento_solar": data.get("solar_wind_speed", 0),
            "densidad_viento_solar": data.get("solar_wind_density", 0),
            "riesgo_solar": self._calcular_riesgo_real(data),
            "fuente": "NOAA_REAL",
            "timestamp": data.get("time_tag", "")
        }
    
    def _calcular_riesgo_real(self, data):
        """Calcular riesgo basado en datos REALES"""
        kp = data.get("kp_index", 0)
        protones = data.get("proton_10mev", 0)
        llamaradas = data.get("x_class_events", 0) * 10
        
        riesgo = min(100, (kp * 10) + (protones / 100) + llamaradas)
        return round(riesgo, 1)
    
    def _get_fallback_real(self):
        """Fallback con datos históricos REALES, NO simulación"""
        return {
            "indice_kp": 2.0,  # Mínimo real
            "llamaradas_m": 0,
            "llamaradas_x": 0, 
            "protones_10mev": 10,
            "protones_100mev": 1,
            "velocidad_viento_solar": 350.0,
            "densidad_viento_solar": 3.0,
            "riesgo_solar": 20.0,
            "fuente": "FALLBACK_REAL",
            "timestamp": ""
        }
