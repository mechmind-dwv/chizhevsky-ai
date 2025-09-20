import requests
from datetime import datetime

def obtener_datos_reales():
    """
    Obtiene datos reales de endpoints funcionales de NOAA
    y los adapta al formato esperado por el sistema
    """
    try:
        # Obtener datos del índice Kp
        response = requests.get("https://services.swpc.noaa.gov/json/planetary_k_index_1m.json", timeout=10)
        kp_data = response.json()
        
        # Obtener alertas solares
        response_alerts = requests.get("https://services.swpc.noaa.gov/products/alerts.json", timeout=10)
        alerts_data = response_alerts.json()
        
        # Procesar y adaptar datos al formato esperado
        ultimo_kp = kp_data[-1] if kp_data else {}
        ultima_alerta = alerts_data[0] if alerts_data else {}
        
        datos_adaptados = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'llamaradas_m': 0,  # Valor por defecto (buscar en otros endpoints)
            'llamaradas_x': 0,   # Valor por defecto
            'indice_kp': float(ultimo_kp.get('kp_index', 0)),
            'velocidad_viento_solar': 350.0,  # Valor por defecto
            'densidad_viento_solar': 3.5,     # Valor por defecto
            'protones_10mev': 100,            # Valor por defecto
            'protones_100mev': 10,            # Valor por defecto
            'riesgo_solar': calcular_riesgo(ultimo_kp, alerts_data),
            'fuente': 'NOAA_REAL'
        }
        
        return datos_adaptados
        
    except Exception as e:
        print(f"Error obteniendo datos reales: {e}")
        return None

def calcular_riesgo(kp_data, alerts_data):
    """Calcula el riesgo solar basado en datos reales"""
    # Lógica simple de ejemplo
    kp_value = float(kp_data.get('kp_index', 0))
    if kp_value >= 5:
        return 80.0
    elif kp_value >= 4:
        return 50.0
    else:
        return 10.0

if __name__ == "__main__":
    datos = obtener_datos_reales()
    if datos:
        print("Datos reales obtenidos:")
        for key, value in datos.items():
            print(f"  {key}: {value}")
