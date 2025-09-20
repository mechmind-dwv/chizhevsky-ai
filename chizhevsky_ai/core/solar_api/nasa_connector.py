"""
📡 CONECTOR NASA SDO - Datos solares en tiempo real
"""
import requests
import json

class NASASolarData:
    def __init__(self):
        self.base_url = "https://api.nasa.gov/DONKI/"
        self.api_key = "DEMO_KEY"  # Usa tu API key real

    def get_solar_flares(self):
        """Obtiene llamaradas solares recientes"""
        try:
            url = f"{self.base_url}FLR?api_key={self.api_key}"
            response = requests.get(url)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_geomagnetic_storms(self):
        """Obtiene tormentas geomagnéticas"""
        try:
            url = f"{self.base_url}GST?api_key={self.api_key}"
            response = requests.get(url)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
