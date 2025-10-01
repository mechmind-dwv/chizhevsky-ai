import requests
import json

def test_endpoints():
    endpoints = [
        "https://services.swpc.noaa.gov/products/alerts.json",
        "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json",
        "https://services.swpc.noaa.gov/json/goes/primary/xray-1-day.json"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint}: FUNCIONA ({len(data) if isinstance(data, list) else 'datos'} obtenidos)")
                # Mostrar muestra de datos
                if endpoint.endswith('alerts.json'):
                    print(f"   Última alerta: {data[0]['product_id']} - {data[0]['issue_datetime']}")
                elif endpoint.endswith('k_index_1m.json'):
                    print(f"   Último Kp: {data[0]['kp_index']} a las {data[0]['time_tag']}")
            else:
                print(f"❌ {endpoint}: Error {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Exception - {str(e)}")

if __name__ == "__main__":
    test_endpoints()
