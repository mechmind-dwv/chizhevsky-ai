import requests
import json

def test_alerts_api():
    try:
        response = requests.get("https://services.swpc.noaa.gov/products/alerts.json", timeout=10)
        response.raise_for_status()
        alerts = response.json()
        print(f"✅ API Alerts funciona - {len(alerts)} alertas encontradas")
        print("Últimas alertas:")
        for alert in alerts[:3]:
            print(f"  - {alert['product_id']}: {alert['issue_datetime']}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_alerts_api()
