import requests
import json
from datetime import datetime

class NOAADataFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Chizhevsky-AI-Monitoring/1.0 (ia.mechmind@gmail.com)',
            'Accept': 'application/json'
        }

    def obtener_datos_solares(self):
        """Obtener datos solares de endpoints funcionales de NOAA"""
        try:
            # Obtener datos del índice Kp
            kp_response = requests.get(
                "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json",
                headers=self.headers, timeout=10
            )
            
            # Obtener alertas solares
            alerts_response = requests.get(
                "https://services.swpc.noaa.gov/products/alerts.json", 
                headers=self.headers, timeout=10
            )
            
            # Procesar datos
            datos = self.procesar_datos_noaa(kp_response, alerts_response)
            return datos
            
        except Exception as e:
            print(f"Error obteniendo datos NOAA: {e}")
            return self.datos_fallback()

    def procesar_datos_noaa(self, kp_response, alerts_response):
        """Procesar datos de los endpoints funcionales de NOAA"""
        datos = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'fuente': 'NOAA_REAL',
            'llamaradas_m': 0,
            'llamaradas_x': 0,
            'indice_kp': 0.0,
            'velocidad_viento_solar': 400.0,  # Valor por defecto
            'densidad_viento_solar': 3.5,     # Valor por defecto
            'protones_10mev': 100,            # Valor por defecto
            'protones_100mev': 10,            # Valor por defecto
            'riesgo_solar': 0.0,
            'alertas_activas': 0
        }

        # Procesar datos del índice Kp
        if kp_response.status_code == 200:
            try:
                kp_data = kp_response.json()
                if kp_data and isinstance(kp_data, list) and len(kp_data) > 0:
                    ultimo_kp = kp_data[-1]
                    # Asegurarse de que tenemos un diccionario
                    if isinstance(ultimo_kp, dict):
                        datos['indice_kp'] = float(ultimo_kp.get('kp_index', 0))
            except Exception as e:
                print(f"Error procesando datos Kp: {e}")

        # Procesar alertas solares
        if alerts_response.status_code == 200:
            try:
                alerts_data = alerts_response.json()
                if isinstance(alerts_data, list):
                    datos['alertas_activas'] = len(alerts_data)
                    datos['riesgo_solar'] = self.calcular_riesgo(alerts_data)
            except Exception as e:
                print(f"Error procesando alertas: {e}")

        return datos

    # Mejorar la función calcular_riesgo en noaa_fix.py
def calcular_riesgo_mejorado(self, alerts_data, kp_value):
    """Calcular riesgo solar mejorado"""
    riesgo = 0.0
    
    # Riesgo basado en Kp index
    if kp_value >= 7: riesgo += 70.0
    elif kp_value >= 5: riesgo += 50.0
    elif kp_value >= 4: riesgo += 30.0
    elif kp_value >= 3: riesgo += 15.0
    
    # Riesgo basado en alertas
    for alerta in alerts_data:
        if isinstance(alerta, dict):
            mensaje = alerta.get('message', '')
            product_id = alerta.get('product_id', '')
            
            # Alertas de tormenta geomagnética
            if 'G3' in mensaje or 'Strong' in mensaje:
                riesgo = max(riesgo, 80.0)
            elif 'G2' in mensaje or 'Moderate' in mensaje:
                riesgo = max(riesgo, 60.0)
            elif 'G1' in mensaje or 'Minor' in mensaje:
                riesgo = max(riesgo, 40.0)
            
            # Alertas de protones
            if 'PX1' in product_id or 'Proton' in mensaje:
                riesgo += 20.0
                
            # Alertas de electrones
            if 'EF3' in product_id or 'Electron' in mensaje:
                riesgo += 15.0
    
    return min(riesgo, 100.0)  # Máximo 100%
    
    def datos_fallback(self):
        """Datos de fallback en caso de error"""
        return {
            'llamaradas_m': 1,
            'llamaradas_x': 0,
            'indice_kp': 2.8,
            'velocidad_viento_solar': 348.24,
            'densidad_viento_solar': 3.52,
            'protones_10mev': 177,
            'protones_100mev': 15,
            'riesgo_solar': 0.0,
            'fuente': 'SIMULADO',
            'alertas_activas': 0
        }

# Función de compatibilidad
def obtener_datos_noaa_actualizados():
    fetcher = NOAADataFetcher()
    return fetcher.obtener_datos_solares()
