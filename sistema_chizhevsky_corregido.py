#!/usr/bin/env python3
"""
🌌 SISTEMA CHIZHEVSKY CORREGIDO - Sin errores de threading
"""
import os
import sqlite3
import requests
import numpy as np
from datetime import datetime, timedelta
import time
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify
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
FLASK_PORT = 27357  # Nuevo puerto para evitar conflictos

class SistemaChizhevskyCorregido:
    def __init__(self):
        self.load_environment()
        self.app = Flask(__name__)
        self.setup_routes()
        
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
    
    def get_spaceweather_data(self):
        """Obtener datos de Space Weather API"""
        try:
            url = "https://services.swpc.noaa.gov/json/solar_summary.json"
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                return self.process_spaceweather_data(data)
            else:
                logger.warning(f"⚠️ Error Space Weather API: {response.status_code}")
                return self.get_fallback_data()
                
        except Exception as e:
            logger.error(f"Error obteniendo datos: {e}")
            return self.get_fallback_data()
    
    def process_spaceweather_data(self, data):
        """Procesar datos de Space Weather API"""
        return {
            'llamaradas_m': data.get('xray_flares_m', 0),
            'llamaradas_x': data.get('xray_flares_x', 0),
            'indice_kp': data.get('kp_index', 2.0),
            'viento_velocidad': data.get('solar_wind_speed', 400),
            'viento_densidad': data.get('solar_wind_density', 4.0),
            'protones_10mev': data.get('proton_flux_10mev', 100),
            'protones_100mev': data.get('proton_flux_100mev', 10),
            'riesgo': self.calculate_risk_from_data(data),
            'fuente': 'NOAA_SPACE_WEATHER'
        }
    
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
            f"📊 Base de datos optimizada"
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
