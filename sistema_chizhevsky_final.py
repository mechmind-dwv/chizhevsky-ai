#!/usr/bin/env python3
"""
🌌 SISTEMA CHIZHEVSKY DEFINITIVO - Con puertos personalizados
"""
import os
import sqlite3
import requests
import numpy as np
from datetime import datetime, timedelta
import time
import logging
from dotenv import load_dotenv

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

# Cargar configuración de puertos
load_dotenv()
FLASK_PORT = int(os.getenv('FLASK_PORT', 7357))
TOR_PORT = int(os.getenv('TOR_HIDDEN_PORT', 9357))

class SistemaChizhevskyFinal:
    def __init__(self):
        self.load_environment()
        self.setup_database()
        
    def load_environment(self):
        """Cargar variables de entorno"""
        load_dotenv()
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        self.CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
        self.DATA_GOV_API_KEY = os.getenv('DATA_GOV_API_KEY')
        self.FLASK_PORT = FLASK_PORT
        logger.info(f"✅ Variables de entorno cargadas - Puerto Flask: {self.FLASK_PORT}")
    
    def setup_database(self):
        """Configurar base de datos SQLite"""
        self.conn = sqlite3.connect('chizhevsky_alerts.db')
        self.cursor = self.conn.cursor()
        
        # Aseguramos que las tablas existan
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS datos_solares (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                llamaradas_m INTEGER,
                llamaradas_x INTEGER,
                indice_kp REAL,
                velocidad_viento_solar REAL,
                densidad_viento_solar REAL,
                protones_10mev INTEGER,
                protones_100mev INTEGER,
                riesgo_solar REAL,
                fuente TEXT
            )
        ''')
        
        self.conn.commit()
        logger.info("✅ Base de datos configurada")
    
    def get_spaceweather_data(self):
        """Obtener datos de Space Weather API alternativa"""
        try:
            # API alternativa para datos solares (NOAA Space Weather)
            url = "https://services.swpc.noaa.gov/json/solar_summary.json"
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                return self.process_spaceweather_data(data)
            else:
                logger.warning(f"⚠️ Error Space Weather API: {response.status_code}")
                return self.get_fallback_data()
                
        except Exception as e:
            logger.error(f"Error obteniendo datos space weather: {e}")
            return self.get_fallback_data()
    
    def process_spaceweather_data(self, data):
        """Procesar datos de Space Weather API"""
        # Datos reales de la API de NOAA
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
        """Datos de fallback cuando las APIs no responden"""
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
        """Calcular riesgo basado en datos reales"""
        risk = 0.0
        
        # Llamaradas X son más peligrosas
        if data.get('xray_flares_x', 0) > 0:
            risk += 0.4
        elif data.get('xray_flares_m', 0) >= 2:
            risk += 0.2
        
        # Alto índice Kp indica tormenta geomagnética
        if data.get('kp_index', 0) >= 5: risk += 0.3
        elif data.get('kp_index', 0) >= 4: risk += 0.2
        
        # Viento solar muy rápido
        if data.get('solar_wind_speed', 0) > 600: risk += 0.2
        
        return min(risk, 1.0)
    
    def send_telegram_message(self, message):
        """Enviar mensaje por Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendMessage"
            payload = {
                'chat_id': self.CHAT_ID,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
                
        except Exception as e:
            logger.error(f"Error enviando Telegram: {e}")
            return False
    
    def save_data(self, data):
        """Guardar datos en la base de datos"""
        try:
            self.cursor.execute('''
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
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error guardando datos: {e}")
            return False
    
    def start_flask_server(self):
        """Iniciar servidor Flask en puerto alternativo"""
        try:
            from flask import Flask, jsonify
            app = Flask(__name__)
            
            @app.route('/')
            def dashboard():
                return jsonify({
                    'status': 'active',
                    'system': 'Chizhevsky AI',
                    'port': self.FLASK_PORT,
                    'data_count': self.get_data_count()
                })
            
            # Ejecutar en segundo plano
            import threading
            flask_thread = threading.Thread(
                target=app.run,
                kwargs={'host': '0.0.0.0', 'port': self.FLASK_PORT, 'debug': False}
            )
            flask_thread.daemon = True
            flask_thread.start()
            
            logger.info(f"🌐 Servidor Flask iniciado en puerto {self.FLASK_PORT}")
            
        except Exception as e:
            logger.error(f"Error iniciando Flask: {e}")
    
    def get_data_count(self):
        """Obtener conteo de datos"""
        self.cursor.execute("SELECT COUNT(*) FROM datos_solares")
        return self.cursor.fetchone()[0]
    
    def run(self):
        """Ejecutar sistema completo"""
        logger.info("🌌 INICIANDO SISTEMA CHIZHEVSKY DEFINITIVO")
        
        # Iniciar servidor web
        self.start_flask_server()
        
        # Mensaje de inicio
        self.send_telegram_message(
            f"🚀 <b>SISTEMA CHIZHEVSKY REINICIADO</b>\n\n"
            f"✅ Puerto Flask: {self.FLASK_PORT}\n"
            f"🌌 Monitorización solar activa\n"
            f"📊 Base de datos: {self.get_data_count()} registros"
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
        finally:
            self.conn.close()

if __name__ == "__main__":
    sistema = SistemaChizhevskyFinal()
    sistema.run()
