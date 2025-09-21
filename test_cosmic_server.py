from flask import Flask, jsonify
from hospital_integration.oms_connector import CosmicHealthConnector
from predictive_analytics.cosmic_predictor import CosmicPredictor
import random
from datetime import datetime

app = Flask(__name__)
connector = CosmicHealthConnector()
predictor = CosmicPredictor()

@app.route('/test/hospital-metrics')
def test_hospital_metrics():
    return jsonify(connector.get_hospital_metrics())

@app.route('/test/cosmic-health')
def test_cosmic_health():
    solar_data = {'riesgo': random.uniform(0, 1)}
    health_data = connector.get_oms_health_alerts()
    predictions = predictor.predict_health_impact({
        'activity_level': solar_data.get('riesgo', 0) * 10
    })
    
    return jsonify({
        'solar_activity': solar_data.get('riesgo', 0) * 10,
        'health_alerts': health_data,
        'predictions': predictions
    })

@app.route('/test/early-warnings')
def test_early_warnings():
    return jsonify(predictor.generate_early_warnings())

if __name__ == '__main__':
    print("🚀 Servidor de prueba ejecutándose en http://localhost:27778")
    print("📊 Endpoints disponibles:")
    print("   http://localhost:27778/test/hospital-metrics")
    print("   http://localhost:27778/test/cosmic-health") 
    print("   http://localhost:27778/test/early-warnings")
    app.run(port=27778, debug=True)
