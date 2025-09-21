#!/usr/bin/env python3
"""
🌌 SISTEMA CHIZHEVSKY COMPLETO CORREGIDO - Sin errores de threading
"""
import os
import sqlite3
import requests
import numpy as np
from datetime import datetime, timedelta
import time
import logging
from flask import render_template
from chizhevsky_ai.core.hematology.integrator import HematologyIntegrator
from hospital_integration.oms_connector_simple import CosmicHealthConnector
from predictive_analytics.cosmic_predictor_simple import CosmicPredictor
from dotenv import load_dotenv
from flask import Flask, jsonify, request, current_app
import threading

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chizhevsky.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configurar puerto
FLASK_PORT = 27777  # Nuevo puerto

class SistemaChizhevskyCorregido:
    def __init__(self):
        self.load_environment()
        self.app = Flask(__name__)
        self.setup_routes()
        self.hematology_integrator = HematologyIntegrator(self)
        self.health_connector = CosmicHealthConnector()
        self.predictor = CosmicPredictor()
        
    def load_environment(self):
        """Cargar variables de entorno"""
        load_dotenv()
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        self.CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
        logger.info(f"✅ Variables de entorno cargadas - Puerto Flask: {FLASK_PORT}")
    
    def get_db_connection(self):
        """Crear nueva conexión a la base de datos (thread-safe)"""
        conn = sqlite3.connect('chizhevsky_alerts.db')
        conn.row_factory = sqlite3.Row
        return conn
    
    def setup_routes(self):
        """Configurar rutas de Flask"""
        
        @self.app.route('/hematology')
        def hematology_dashboard():
            return render_template('hematology_dashboard.html')
        
        @self.app.route('/')
        def dashboard():
            try:
                conn = self.get_db_connection()
                count = conn.execute("SELECT COUNT(*) as count FROM datos_solares").fetchone()['count']
                conn.close()
                
                return jsonify({
                    'status': 'active',
                    'system': 'Chizhevsky AI - Corregido',
                    'port': FLASK_PORT,
                    'data_count': count,
                    'message': '✅ Sistema funcionando sin errores de threading'
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/datos')
        def api_datos():
            try:
                conn = self.get_db_connection()
                datos = conn.execute(
                    "SELECT * FROM datos_solares ORDER BY id DESC LIMIT 1"
                ).fetchone()
                conn.close()
                
                if datos:
                    return jsonify({
                        'id': datos['id'],
                        'timestamp': datos['timestamp'],
                        'llamaradas_m': datos['llamaradas_m'],
                        'llamaradas_x': datos['llamaradas_x'],
                        'indice_kp': datos['indice_kp'],
                        'velocidad_viento_solar': datos['velocidad_viento_solar'],
                        'densidad_viento_solar': datos['densidad_viento_solar'],
                        'protones_10mev': datos['protones_10mev'],
                        'protones_100mev': datos['protones_100mev'],
                        'riesgo_solar': datos['riesgo_solar'],
                        'fuente': datos['fuente']
                    })
                return jsonify({'error': 'No hay datos disponibles'}), 404
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/status')
        def status():
            return jsonify({
                'status': 'active',
                'timestamp': datetime.now().isoformat(),
                'system': 'Chizhevsky AI - Corregido',
                'port': FLASK_PORT
            })
            
        @self.app.route('/api/hematology/risk')
        def hematology_risk():
            try:
                solar_data = self.get_spaceweather_data()
                risk_assessment = self.hematology_integrator.generate_hematology_alert(
                    solar_data.get('riesgo', 0) * 10  # Convertir a escala 0-10
                )
                return jsonify(risk_assessment)
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/hematology/analysis', methods=['POST'])
        def hematology_analysis():
            try:
                data = request.json
                analysis = self.hematology_integrator.hematology.calculate_erythrocyte_electrical_properties(
                    data.get('sedimentation_rate', 0), 
                    data.get('environmental_ions', 0)
                )
                return jsonify(analysis)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    def get_spaceweather_data(self):
        """Obtener datos de Space Weather API desde endpoints funcionales"""
        try:
            # Importar y usar el nuevo fetcher
            from noaa_fix import obtener_datos_noaa_actualizados
            datos = obtener_datos_noaa_actualizados()
            
            # Adaptar al formato esperado por el sistema
            return {
                'llamaradas_m': datos['llamaradas_m'],
                'llamaradas_x': datos['llamaradas_x'],
                'indice_kp': datos['indice_kp'],
                'viento_velocidad': datos['velocidad_viento_solar'],
                'viento_densidad': datos['densidad_viento_solar'],
                'protones_10mev': datos['protones_10mev'],
                'protones_100mev': datos['protones_100mev'],
                'riesgo': datos['riesgo_solar'] / 100.0,  # Convertir de porcentaje a decimal
                'fuente': datos['fuente']
            }
                
        except Exception as e:
            logger.error(f"Error obteniendo datos: {e}")
            return self.get_fallback_data()
            
    def get_fallback_data(self):
        """Datos de fallback"""
        hora_actual = datetime.now().hour
        ciclo_diario = np.sin(hora_actual * np.pi / 12)
        
        return {
            'llamaradas_m': max(0, int(2 + ciclo_diario * 2)),
            'llamaradas_x': 1 if ciclo_diario > 0.8 else 0,
            'indice_kp': round(2 + abs(ciclo_diario) * 3, 1),
            'viento_velocidad': 400 + ciclo_diario * 200,
            'viento_densidad': 3 + abs(ciclo_diario) * 2,
            'protones_10mev': int(100 + abs(ciclo_diario) * 300),
            'protones_100mev': int(10 + abs(ciclo_diario) * 20),
            'riesgo': min(0.3 + abs(ciclo_diario) * 0.4, 0.9),
            'fuente': 'SIMULADO'
        }
    
    def calculate_risk_from_data(self, data):
        """Calcular riesgo"""
        risk = 0.0
        if data.get('xray_flares_x', 0) > 0: risk += 0.4
        elif data.get('xray_flares_m', 0) >= 2: risk += 0.2
        if data.get('kp_index', 0) >= 5: risk += 0.3
        elif data.get('kp_index', 0) >= 4: risk += 0.2
        if data.get('solar_wind_speed', 0) > 600: risk += 0.2
        return min(risk, 1.0)
    
    def save_data(self, data):
        """Guardar datos en la base de datos"""
        try:
            conn = self.get_db_connection()
            conn.execute('''
                INSERT INTO datos_solares 
                (llamaradas_m, llamaradas_x, indice_kp, velocidad_viento_solar, 
                 densidad_viento_solar, protones_10mev, protones_100mev, riesgo_solar, fuente)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['llamaradas_m'], data['llamaradas_x'], data['indice_kp'],
                data['viento_velocidad'], data['viento_densidad'],
                data['protones_10mev'], data['protones_100mev'],
                data['riesgo'], data['fuente']
            ))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error guardando datos: {e}")
            return False
    
    def send_telegram_message(self, message):
        """Enviar mensaje por Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendMessage"
            payload = {'chat_id': self.CHAT_ID, 'text': message, 'parse_mode': 'HTML'}
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error enviando Telegram: {e}")
            return False
    
    def start_flask_server(self):
        """Iniciar servidor Flask"""
        def run_flask():
            self.app.run(host='0.0.0.0', port=FLASK_PORT, debug=False, threaded=True)
        
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        logger.info(f"🌐 Servidor Flask iniciado en puerto {FLASK_PORT}")
    
    def run(self):
        """Ejecutar sistema completo"""
        logger.info("🌌 INICIANDO SISTEMA CHIZHEVSKY CORREGIDO")
        
        # Iniciar servidor web
        self.start_flask_server()
        
        # Mensaje de inicio
        self.send_telegram_message(
            f"🚀 <b>SISTEMA CHIZHEVSKY CORREGIDO</b>\n\n"
            f"✅ Sin errores de threading\n"
            f"🌐 Puerto: {FLASK_PORT}\n"
            f"📊 Base de datos optimizada\n"
            f"🩸 Módulo de hematología integrado"
        )
        
        # Bucle principal
        try:
            while True:
                data = self.get_spaceweather_data()
                data['riesgo'] = self.calculate_risk_from_data(data)
                
                if self.save_data(data):
                    logger.info(
                        f"📊 Datos: {data['llamaradas_m']}M {data['llamaradas_x']}X, "
                        f"Kp={data['indice_kp']}, Viento={data['viento_velocidad']}km/s, "
                        f"Riesgo={data['riesgo']:.0%}, Fuente={data['fuente']}"
                    )
                
                if data['riesgo'] > 0.6:
                    message = f"⚠️ <b>ALERTA SOLAR</b>\n\nRiesgo: {data['riesgo']:.0%}"
                    self.send_telegram_message(message)
                
                time.sleep(300)  # 5 minutos
                
        except KeyboardInterrupt:
            logger.info("🛑 Sistema detenido por usuario")
        except Exception as e:
            logger.error(f"❌ Error en bucle principal: {e}")

if __name__ == "__main__":
    sistema = SistemaChizhevskyCorregido()
    sistema.run()

# ==================== NUEVOS PODERES CÓSMICOS ====================

from hospital_integration.oms_connector_simple import CosmicHealthConnector
from predictive_analytics.cosmic_predictor_simple import CosmicPredictor

class SistemaChizhevskyMejorado(SistemaChizhevskyCorregido):
    def __init__(self):
        super().__init__()
        self.health_connector = CosmicHealthConnector()
        self.predictor = CosmicPredictor()
        self.setup_enhanced_routes()
    
    def setup_enhanced_routes(self):
        """Configurar rutas mejoradas"""
        @self.app.route('/api/cosmic/health-status')
        def cosmic_health_status():
            try:
                solar_data = self.get_spaceweather_data()
                health_data = self.health_connector.get_oms_health_alerts()
                predictions = self.predictor.predict_health_impact({
                    'activity_level': solar_data.get('riesgo', 0) * 10
                })
                
                return jsonify({
                    'solar_activity': solar_data.get('riesgo', 0) * 10,
                    'health_alerts': health_data,
                    'predictions': predictions,
                    'timestamp': datetime.now().isoformat(),
                    'system_status': 'cosmic_enhanced'
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/hospital/metrics')
        def hospital_metrics():
            try:
                metrics = self.health_connector.get_hospital_metrics('default')
                return jsonify(metrics)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/early-warnings')
        def early_warnings():
            try:
                warnings = self.predictor.generate_early_warnings()
                return jsonify(warnings)
            except Exception as e:
                return jsonify({'error': str(e)}), 500

# Reemplazar la clase principal
if __name__ == "__main__":
    sistema = SistemaChizhevskyMejorado()
    sistema.run()

# ==================== NUEVOS PODERES CÓSMICOS ====================

from hospital_integration.oms_connector_simple import CosmicHealthConnector
from predictive_analytics.cosmic_predictor_simple import CosmicPredictor

class SistemaChizhevskyMejorado(SistemaChizhevskyCorregido):
    def __init__(self):
        super().__init__()
        self.health_connector = CosmicHealthConnector()
        self.predictor = CosmicPredictor()
        self.setup_enhanced_routes()
    
    def setup_enhanced_routes(self):
        """Configurar rutas mejoradas"""
        @self.app.route('/api/cosmic/health-status')
        def cosmic_health_status():
            try:
                solar_data = self.get_spaceweather_data()
                health_data = self.health_connector.get_oms_health_alerts()
                predictions = self.predictor.predict_health_impact({
                    'activity_level': solar_data.get('riesgo', 0) * 10
                })
                
                return jsonify({
                    'solar_activity': solar_data.get('riesgo', 0) * 10,
                    'health_alerts': health_data,
                    'predictions': predictions,
                    'timestamp': datetime.now().isoformat(),
                    'system_status': 'cosmic_enhanced'
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/hospital/metrics')
        def hospital_metrics():
            try:
                metrics = self.health_connector.get_hospital_metrics('default')
                return jsonify(metrics)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/early-warnings')
        def early_warnings():
            try:
                warnings = self.predictor.generate_early_warnings()
                return jsonify(warnings)
            except Exception as e:
                return jsonify({'error': str(e)}), 500

# Reemplazar la clase principal
if __name__ == "__main__":
    sistema = SistemaChizhevskyMejorado()
    sistema.run()

# ========== COSMIC UPGRADE INYECTADO ==========
from hospital_integration.oms_connector_simple import CosmicHealthConnector
from predictive_analytics.cosmic_predictor_simple import CosmicPredictor

# Modificar la clase principal para añadir nuevas capacidades
original_init = SistemaChizhevskyCorregido.__init__
original_setup_routes = SistemaChizhevskyCorregido.setup_routes


        @self.app.route('/api/cosmic/health-status')
        def cosmic_health_status():
            try:
                solar_data = self.get_spaceweather_data()
                health_data = self.health_connector.get_oms_health_alerts()
                predictions = self.predictor.predict_health_impact({
                    'activity_level': solar_data.get('riesgo', 0) * 10
                })
                
                return jsonify({
                    'solar_activity': solar_data.get('riesgo', 0) * 10,
                    'health_alerts': health_data,
                    'predictions': predictions,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/hospital/metrics')
        def hospital_metrics():
            try:
                metrics = self.health_connector.get_hospital_metrics('default')
                return jsonify(metrics)
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/early-warnings')
        def early_warnings():
            try:
                warnings = self.predictor.generate_early_warnings()
                return jsonify(warnings)
            except Exception as e:
                return jsonify({'error': str(e)}), 500

def new_init(self):
    original_init(self)
    self.health_connector = CosmicHealthConnector()
    self.predictor = CosmicPredictor()

def new_setup_routes(self):
    original_setup_routes(self)
    
        @self.app.route('/api/cosmic/health-status')
    def cosmic_health_status():
        try:
            solar_data = self.get_spaceweather_data()
            health_data = self.health_connector.get_oms_health_alerts()
            predictions = self.predictor.predict_health_impact({
                'activity_level': solar_data.get('riesgo', 0) * 10
            })
            
            return jsonify({
                'solar_activity': solar_data.get('riesgo', 0) * 10,
                'health_alerts': health_data,
                'predictions': predictions,
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        @self.app.route('/api/hospital/metrics')
    def hospital_metrics():
        try:
            metrics = self.health_connector.get_hospital_metrics('default')
            return jsonify(metrics)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        @self.app.route('/api/early-warnings')
    def early_warnings():
        try:
            warnings = self.predictor.generate_early_warnings()
            return jsonify(warnings)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Aplicar el parche
SistemaChizhevskyCorregido.__init__ = new_init
SistemaChizhevskyCorregido.setup_routes = new_setup_routes

# Añadir esta ruta en setup_routes()
@app.route('/api/cosmic/proxy/<path:subpath>')
def cosmic_proxy(subpath):
    """Proxy para el servidor de salud cósmica"""
    try:
        import requests
        response = requests.get(f'http://localhost:27779/cosmic-api/{subpath}', timeout=5)
        return response.json(), response.status_code
    except Exception as e:
        return jsonify({'error': f'Proxy error: {str(e)}'}), 502
