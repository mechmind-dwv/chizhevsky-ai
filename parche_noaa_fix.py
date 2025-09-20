import requests
import json
from datetime import datetime

class NOAADataFetcher:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.headers = {
            'User-Agent': 'Chizhevsky-AI-Monitoring (ia.mechmind@gmail.com)',
            'Accept': 'application/json'
        }
        if api_key:
            self.headers['token'] = api_key

    def obtener_datos_solares(self):
        """Obtener datos solares de múltiples fuentes de NOAA"""
        datos = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'fuente': 'NOAA',
            'llamaradas_m': 0,
            'llamaradas_x': 0,
            'indice_kp': 0.0,
            'velocidad_viento_solar': 0.0,
            'densidad_viento_solar': 0.0,
            'protones_10mev': 0,
            'protones_100mev': 0,
            'riesgo_solar': 0.0
        }

        try:
            # 1. Obtener datos del índice Kp
            kp_response = requests.get(
                "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json",
                headers=self.headers, timeout=10
            )
            if kp_response.status_code == 200:
                kp_data = kp_response.json()
                if kp_data:
                    ultimo_kp = kp_data[-1]
                    datos['indice_kp'] = float(ultimo_kp.get('kp_index', 0))
            
            # 2. Obtener alertas solares
            alerts_response = requests.get(
                "https://services.swpc.noaa.gov/products/alerts.json",
                headers=self.headers, timeout=10
            )
            if alerts_response.status_code == 200:
                alerts_data = alerts_response.json()
                datos['alertas_activas'] = len(alerts_data)
                
                # Analizar alertas para determinar riesgo
                riesgo = self.calcular_riesgo(alerts_data)
                datos['riesgo_solar'] = riesgo
            
            # 3. Intentar obtener datos de viento solar (si disponible)
            try:
                # Este endpoint puede variar, es un ejemplo
                solarwind_response = requests.get(
                    "https://services.swpc.noaa.gov/json/ace/swepam/ace_swepam_1h.json",
                    headers=self.headers, timeout=5
                )
                if solarwind_response.status_code == 200:
                    solarwind_data = solarwind_response.json()
                    if solarwind_data:
                        ultimo_dato = solarwind_data[-1]
                        datos['velocidad_viento_solar'] = float(ultimo_dato.get('speed', 0))
                        datos['densidad_viento_solar'] = float(ultimo_dato.get('density', 0))
            except:
                pass  # Ignorar errores en endpoints opcionales
                
            return datos
            
        except Exception as e:
            print(f"Error obteniendo datos NOAA: {e}")
            # Retornar datos por defecto en caso de error
            return datos

    def calcular_riesgo(self, alerts_data):
        """Calcular riesgo solar basado en alertas"""
        riesgo = 0.0
        for alerta in alerts_data:
            mensaje = alerta.get('message', '')
            # Lógica simple de cálculo de riesgo
            if 'G3' in mensaje or 'Strong' in mensaje:
                riesgo = max(riesgo, 80.0)
            elif 'G2' in mensaje or 'Moderate' in mensaje:
                riesgo = max(riesgo, 60.0)
            elif 'G1' in mensaje or 'Minor' in mensaje:
                riesgo = max(riesgo, 40.0)
            elif 'Warning' in mensaje:
                riesgo = max(riesgo, 20.0)
        return riesgo

# Función de compatibilidad para el sistema existente
def obtener_datos_noaa():
    fetcher = NOAADataFetcher(api_key="EBScmUckSBriKewtpC9Oba1HIXNguUU7PqLOv3cv")
    return fetcher.obtener_datos_solares()

if __name__ == "__main__":
    datos = obtener_datos_noaa()
    print("Datos NOAA obtenidos:")
    for key, value in datos.items():
        print(f"  {key}: {value}")
