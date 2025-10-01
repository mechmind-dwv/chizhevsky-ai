# config/chizhevsky_config.py
"""
Configuración del sistema Chizhevsky AI
"""
import os
from dotenv import load_dotenv

load_dotenv()

class ChizhevskyConfig:
    # Configuración de base de datos
    DB_PATH = os.getenv('CHIZHEVSKY_DB_PATH', 'data/chizhevsky_historical.db')
    
    # Configuración de APIs
    NASA_API_KEY = os.getenv('NASA_API_KEY', 'DEMO_KEY')
    NOAA_API_KEY = os.getenv('NOAA_API_KEY', '')
    
    # Configuración de logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/chizhevsky_ai.log')
    
    # Parámetros de análisis
    HISTORICAL_START_YEAR = -400  # 400 a.C.
    HISTORICAL_END_YEAR = 2100    # Hasta 2100
    PREDICTION_CYCLES = 5         # Ciclos a predecir
    
    @classmethod
    def validate_config(cls):
        """Validar configuración"""
        required_dirs = ['data', 'logs']
        for directory in required_dirs:
            os.makedirs(directory, exist_ok=True)
        
        return True
