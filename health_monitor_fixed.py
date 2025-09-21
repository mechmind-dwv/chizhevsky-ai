#!/usr/bin/env python3
"""
🔬 MONITOR DE SALUD - Puerto 27778
"""
import requests
import time
from datetime import datetime

BASE_URL = "http://localhost:27778"

def get_data(endpoint):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        return response.json()
    except:
        return None

def main():
    print("🔬 Monitor de Salud Chizhevsky")
    print("==============================")
    
    while True:
        try:
            metrics = get_data('/cosmic-api/hospital/metrics')
            health = get_data('/cosmic-api/health-status')
            
            if metrics and health:
                print(f"\n🕐 {datetime.now().strftime('%H:%M:%S')}")
                print(f"🌞 Solar: {health['solar_activity']:.2f} - {health['emergency_level']}")
                print(f"🏥 Camas: {metrics['bed_occupancy']}% - Críticos: {metrics['critical_cases']}")
                print(f"📈 Esperados: {health['predictions']['expected_emergency_cases']} casos")
                
                if health['solar_activity'] > 7:
                    print("⚠️  ALERTA: Alta actividad solar!")
            else:
                print("❌ Error obteniendo datos")
                
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\n🛑 Monitor detenido")
            break
        except Exception as e:
            print(f"💥 Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
