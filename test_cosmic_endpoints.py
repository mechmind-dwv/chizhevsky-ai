from flask import Flask, jsonify
import random
from datetime import datetime

app = Flask(__name__)

@app.route('/api/test/hospital-metrics')
def test_hospital_metrics():
    return jsonify({
        'emergency_admissions': random.randint(30, 60),
        'bed_occupancy': random.uniform(60, 95),
        'blood_supply': random.randint(80, 150),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/test/cosmic-health')
def test_cosmic_health():
    return jsonify({
        'solar_activity': random.uniform(0, 10),
        'health_alerts': {
            'respiratory_cases': random.randint(500, 1500),
            'emergency_events': random.randint(10, 50)
        },
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(port=27778, debug=True)
