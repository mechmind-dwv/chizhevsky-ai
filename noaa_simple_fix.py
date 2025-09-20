import requests
from datetime import datetime

def get_simple_noaa_data():
    """Versión simple usando solo el endpoint de Kp"""
    try:
        response = requests.get(
            "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json",
            headers={'User-Agent': 'Chizhevsky-AI-Monitoring'},
            timeout=10
        )
        
        if response.status_code == 200:
            kp_data = response.json()
            if kp_data and isinstance(kp_data, list) and len(kp_data) > 0:
                latest = kp_data[-1]
                if isinstance(latest, dict):
                    kp_value = float(latest.get('kp_index', 2.0))
                    return {
                        'llamaradas_m': 1,
                        'llamaradas_x': 0,
                        'indice_kp': kp_value,
                        'viento_velocidad': 400.0,
                        'viento_densidad': 3.5,
                        'protones_10mev': 100,
                        'protones_100mev': 10,
                        'riesgo': min(kp_value / 10.0, 0.9),  # Kp/10 como riesgo
                        'fuente': 'NOAA_KP'
                    }
        
        # Fallback si algo falla
        return {
            'llamaradas_m': 1,
            'llamaradas_x': 0,
            'indice_kp': 2.8,
            'viento_velocidad': 348.24,
            'viento_densidad': 3.52,
            'protones_10mev': 177,
            'protones_100mev': 15,
            'riesgo': 0.0,
            'fuente': 'SIMULADO'
        }
        
    except Exception as e:
        print(f"Error simple: {e}")
        # Fallback extremo
        return {
            'llamaradas_m': 1,
            'llamaradas_x': 0,
            'indice_kp': 2.8,
            'viento_velocidad': 348.24,
            'viento_densidad': 3.52,
            'protones_10mev': 177,
            'protones_100mev': 15,
            'riesgo': 0.0,
            'fuente': 'SIMULADO'
        }
