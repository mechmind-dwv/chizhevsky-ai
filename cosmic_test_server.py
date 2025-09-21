from flask import Flask, jsonify
import random
from datetime import datetime

app = Flask(__name__)

# Simular el conector OMS
class MockHealthConnector:
    def get_hospital_metrics(self):
        return {
            'emergency_admissions': random.randint(30, 60),
            'bed_occupancy': round(random.uniform(60, 95), 1),
            'medical_staff': random.randint(10, 20),
            'blood_supply': random.randint(80, 150),
            'critical_cases': random.randint(5, 15),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_oms_health_alerts(self):
        return {
            'respiratory_cases': random.randint(500, 1500),
            'emergency_events': random.randint(10, 50),
            'vaccination_rate': round(random.uniform(70, 85), 1),
            'timestamp': datetime.now().isoformat()
        }

# Simular el predictor
class MockPredictor:
    def predict_health_impact(self, solar_data):
        activity_level = solar_data.get('activity_level', 0)
        return {
            'expected_emergency_cases': int(activity_level * 8.5),
            'predicted_blood_demand': int(activity_level * 15 + 80),
            'cardiac_risk_level': min(activity_level / 2, 5.0)
        }
    
    def generate_early_warnings(self):
        return {
            'high_risk_periods': ['next_24_hours'],
            'recommendations': ['increase_staffing', 'monitor_vitals'],
            'timestamp': datetime.now().isoformat()
        }

connector = MockHealthConnector()
predictor = MockPredictor()

@app.route('/api/hospital/metrics')
def hospital_metrics():
    return jsonify(connector.get_hospital_metrics())

@app.route('/api/cosmic/health-status')
def cosmic_health_status():
    solar_activity = random.uniform(0, 10)
    return jsonify({
        'solar_activity': solar_activity,
        'health_alerts': connector.get_oms_health_alerts(),
        'predictions': predictor.predict_health_impact({'activity_level': solar_activity})
    })

@app.route('/api/early-warnings')
def early_warnings():
    return jsonify(predictor.generate_early_warnings())

if __name__ == '__main__':
    print("🚀 Servidor de prueba cósmico ejecutándose en http://localhost:27779")
    print("📊 Endpoints disponibles:")
    print("   http://localhost:27779/api/hospital/metrics")
    print("   http://localhost:27779/api/cosmic/health-status")
    print("   http://localhost:27779/api/early-warnings")
    app.run(port=27779, debug=True)
