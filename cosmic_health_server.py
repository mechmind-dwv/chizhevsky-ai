#!/usr/bin/env python3
"""
🚑 SERVIDOR INDEPENDIENTE DE SALUD CÓSMICA - Versión Simplificada
"""
from flask import Flask, jsonify, render_template
import random
from datetime import datetime

app = Flask(__name__)

def get_hospital_metrics():
    """Simular métricas hospitalarias"""
    return {
        'emergency_admissions': random.randint(30, 60),
        'bed_occupancy': round(random.uniform(60, 95), 1),
        'medical_staff': random.randint(10, 20),
        'blood_supply': random.randint(80, 150),
        'critical_cases': random.randint(5, 15),
        'timestamp': datetime.now().isoformat()
    }

def get_health_status():
    """Simular estado de salud completo"""
    solar_activity = random.uniform(0, 10)
    
    return {
        'solar_activity': round(solar_activity, 2),
        'emergency_level': 'HIGH' if solar_activity > 7 else 'MODERATE' if solar_activity > 4 else 'LOW',
        'predictions': {
            'expected_emergency_cases': int(solar_activity * 8),
            'predicted_blood_demand': int(solar_activity * 15 + 80),
            'cardiac_risk_level': round(min(solar_activity / 2, 5.0), 1)
        },
        'timestamp': datetime.now().isoformat()
    }

@app.route('/')
def index():
    """Página principal con dashboard"""
    return render_template('simple_dashboard.html')

@app.route('/cosmic-api/hospital/metrics')
def hospital_metrics():
    return jsonify(get_hospital_metrics())

@app.route('/cosmic-api/health-status')
def cosmic_health_status():
    return jsonify(get_health_status())

@app.route('/cosmic-api/early-warnings')
def early_warnings():
    return jsonify({
        'high_risk_periods': ['next_24_hours'],
        'recommendations': ['increase_staffing', 'monitor_vitals'],
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Servidor de Salud Cósmica iniciado en http://localhost:27779")
    print("📊 Dashboard disponible en: http://localhost:27779/")
    app.run(host='0.0.0.0', port=27779, debug=False)

@app.route('/cosmic-dashboard')
def cosmic_dashboard():
    """Dashboard web de salud cósmica"""
    return render_template('cosmic_health_dashboard.html')

@app.route('/')
def index():
    """Página principal redirige al dashboard"""
    return redirect('/cosmic-dashboard')
