#!/usr/bin/env python3
"""
🔧 MEJORAR CONEXIÓN NASA API
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_nasa_connection():
    """Probar diferentes endpoints de NASA"""
    api_key = os.getenv('NASA_API_KEY', 'DEMO_KEY')
    
    endpoints = [
        f"https://api.nasa.gov/DONKI/FLR?api_key={api_key}",
        f"https://api.nasa.gov/DONKI/CME?api_key={api_key}",
        f"https://api.nasa.gov/DONKI/GST?api_key={api_key}",
        "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json",
        "https://services.swpc.noaa.gov/products/solar-cycle/sunspot-numbers.json"
    ]
    
    print("🔍 Probando conexiones con APIs solares...")
    
    for url in endpoints:
        try:
            response = requests.get(url, timeout=15)
            print(f"{'✅' if response.status_code == 200 else '❌'} {url} -> {response.status_code}")
            if response.status_code != 200:
                print(f"   Error: {response.text[:100]}...")
        except Exception as e:
            print(f"❌ {url} -> Error: {e}")
    
    print("\n💡 Recomendación: Usar datos de NOAA si NASA falla")

if __name__ == "__main__":
    test_nasa_connection()
