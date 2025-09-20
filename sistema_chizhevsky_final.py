"""
🌌 SISTEMA CHIZHEVSKY DEFINITIVO - Corregido para threading
"""
import os
import sqlite3
import requests
import numpy as np
from datetime import datetime, timedelta
import time
import logging
import threading
from dotenv import load_dotenv
from flask import Flask, jsonify

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

class SistemaChizhevskyFinal:
    def __init__(self):
        self.load_environment()
        self.local = threading.local()  # Para almacenamiento por hilo
        self.setup_flask()
        
    def load_environment(self):
        """Cargar variables de entorno"""
        load_dotenv()
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        self.CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
        self.DATA_GOV_API_KEY = os.getenv('DATA_GOV_API_KEY')
        logger.info("✅ Variables de entorno cargadas")
    
    def get_db_connection(self):
        """Obtener conexión a BD segura para threading"""
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect('chizhevsky_alerts.db', check_same_thread=False)
            self.local.cursor = self.local.conn.cursor()
        return self.local.conn, self.local.cursor
    
    def setup_database(self):
        """Configurar base de datos (seguro para threading)"""
        conn, cursor = self.get_db_connection()
        
        # Verificar y crear tablas si no existen
        cursor.execute('''
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
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alertas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                tipo TEXT,
                nivel TEXT,
                mensaje TEXT,
                riesgo REAL,
                enviada BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        logger.info("✅ Base de datos configurada")
    
    def setup_flask(self):
        """Configurar servidor Flask"""
        self.app = Flask(__name__)
        self.setup_routes()
        self.setup_database()
    
    def setup_routes(self):
        """Configurar rutas de Flask"""
        @self.app.route('/')
        def dashboard():
            return jsonify({
                'status': 'active',
                'system': 'Chizhevsky AI - Definitive',
                'message': '✅ Sistema funcionando correctamente',
                'timestamp': datetime.now().isoformat()
            })
        
        @self.app.route('/api/data')
        def api_data():
            conn, cursor = self.get_db_connection()
            cursor.execute("SELECT COUNT(*) FROM datos_solares")
            count = cursor.fetchone()[0]
            return jsonify({'data_count': count})
    
    def get_real_data(self):
        """Obtener datos reales o simulados"""
        try:
            # Simular obtención de datos
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
        except Exception as e:
            logger.error(f"Error obteniendo datos: {e}")
            return self.get_fallback_data()
    
    def get_fallback_data(self):
        """Datos de fallback"""
        return {
            'llamaradas_m': 1,
            'llamaradas_x': 0,
            'indice_kp': 2.8,
            'viento_velocidad': 380.0,
            'viento_densidad': 4.1,
            'protones_10mev': 120,
            'protones_100mev': 10,
            'riesgo': 0.3,
            'fuente': 'FALLBACK'
        }
    
    def calculate_risk(self, data):
        """Calcular riesgo basado en múltiples factores"""
        risk = 0.0
        if data['llamaradas_x'] > 0: risk += 0.4
        elif data['llamaradas_m'] >= 2: risk += 0.2
        if data['indice_kp'] >= 5: risk += 0.3
        elif data['indice_kp'] >= 4: risk += 0.2
        return min(risk, 1.0)
    
    def save_data(self, data):
        """Guardar datos en BD (thread-safe)"""
        try:
            conn, cursor = self.get_db_connection()
            cursor.execute('''
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
            return True
        except Exception as e:
            logger.error(f"Error guardando datos: {e}")
            return False
    
    def run_monitoring(self):
        """Ejecutar monitoreo en segundo plano"""
        while True:
            try:
                data = self.get_real_data()
                data['riesgo'] = self.calculate_risk(data)
                
                if self.save_data(data):
                    logger.info(
                        f"📊 Datos: {data['llamaradas_m']}M {data['llamaradas_x']}X, "
                        f"Kp={data['indice_kp']}, Viento={data['viento_velocidad']}km/s, "
                        f"Riesgo={data['riesgo']:.0%}, Fuente={data['fuente']}"
                    )
                
                time.sleep(300)  # 5 minutos
                
            except Exception as e:
                logger.error(f"Error en monitoreo: {e}")
                time.sleep(60)
    
    def run(self):
        """Ejecutar sistema completo"""
        logger.info("🌌 INICIANDO SISTEMA CHIZHEVSKY DEFINITIVO")
        
        # Iniciar monitoreo en segundo plano
        monitor_thread = threading.Thread(target=self.run_monitoring, daemon=True)
        monitor_thread.start()
        
        # Iniciar servidor Flask
        try:
            self.app.run(host='0.0.0.0', port=7357, debug=False)
        except KeyboardInterrupt:
            logger.info("🛑 Sistema detenido por usuario")
        except Exception as e:
            logger.error(f"❌ Error en servidor Flask: {e}")

if __name__ == "__main__":
    sistema = SistemaChizhevskyFinal()
    sistema.run()
