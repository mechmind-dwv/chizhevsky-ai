import os
import requests

# Configurar la clave API de NOAA
NOAA_API_KEY = "EBScmUckSBriKewtpC9Oba1HIXNguUU7PqLOv3cv"

def probar_endpoints_con_api():
    """Probar endpoints de NOAA con la clave API"""
    endpoints = [
        "https://www.ncei.noaa.gov/cdo-web/api/v2/datasets",
        "https://www.ncei.noaa.gov/cdo-web/api/v2/datacategories",
        "https://www.ncei.noaa.gov/cdo-web/api/v2/datatypes"
    ]
    
    headers = {'token': NOAA_API_KEY}
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint}: FUNCIONA con API key")
                print(f"   Resultados: {len(data.get('results', []))}")
            else:
                print(f"❌ {endpoint}: Error {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Exception - {str(e)}")

def probar_swpc_con_headers():
    """Probar endpoints de SWPC con headers personalizados"""
    endpoints = [
        "https://services.swpc.noaa.gov/products/alerts.json",
        "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
    ]
    
    # User-Agent recomendado por NOAA :cite[1]:cite[8]
    headers = {
        'User-Agent': 'Chizhevsky-AI-Monitoring (https://github.com/tu-usuario/chizhevsky-ai, ia.mechmind@gmail.com)',
        'Accept': 'application/json'
    }
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint}: FUNCIONA")
                if endpoint.endswith('alerts.json'):
                    print(f"   Alertas activas: {len(data)}")
                elif endpoint.endswith('k_index_1m.json'):
                    print(f"   Registros Kp: {len(data)}")
            else:
                print(f"❌ {endpoint}: Error {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Exception - {str(e)}")

if __name__ == "__main__":
    print("🔐 Probando endpoints con clave API de NOAA...")
    probar_endpoints_con_api()
    
    print("\n🌐 Probando endpoints de SWPC con headers...")
    probar_swpc_con_headers()
