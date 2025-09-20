#!/usr/bin/env python3
"""
🌌 SISTEMA CHIZHEVSKY UNIFICADO - Versión estable en puerto 27357
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

class SistemaChizhevskyUnificado:
    def __init__(self):
        self.load_environment()
        self.setup_database()
        self.setup_flask()
        
    def load_environment(self):
        """Cargar variables de entorno"""
        load_dotenv()
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        self.CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
        logger.info("✅ Variables de entorno cargadas - Puerto Flask: 27357")
    
    def setup_database(self):
        """Configurar base de datos SQLite"""
        self.conn = sqlite3.connect('chizhevsky_alerts.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Asegurar que las tablas existan
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
    
    def setup_flask(self):
        """Configurar servidor Flask"""
        self.app = Flask(__name__)
        
        @self.app.route('/')
        def dashboard():
            return jsonify({
                "data_count": self.get_data_count(),
                "message": "✅ Sistema funcionando sin errores de threading",
                "port": 27357,
                "status": "active",
                "system": "Chizhevsky AI - Corregido"
            })
        
        @self.app.route('/api/datos')
        def api_datos():
            return jsonify(self.get_latest_data())
        
        @self.app.route('/status')
        def status():
            return jsonify({"status": "active", "timestamp": datetime.now().isoformat()})
    
    def get_data_count(self):
        """Obtener conteo de datos"""
        self.cursor.execute("SELECT COUNT(*) FROM datos_solares")
        return self.cursor.fetchone()[0]
    
    def get_latest_data(self):
        """Obtener últimos datos"""
        self.cursor.execute("SELECT * FROM datos_solares ORDER BY id DESC LIMIT 1")
        row = self.cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "timestamp": row[1],
                "llamaradas_m": row[2],
                "llamaradas_x": row[3],
                "indice_kp": row[4],
                "velocidad_viento_solar": row[5],
                "densidad_viento_solar": row[6],
                "protones_10mev": row[7],
                "protones_100mev": row[8],
                "riesgo_solar": row[9],
                "fuente": row[10]
            }
        return {}
    
    def get_simulated_data(self):
        """Generar datos solares simulados"""
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
    
    def save_data(self, data):
        """Guardar datos en BD"""
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
    
    def run_monitoring(self):
        """Ejecutar monitoreo en segundo plano"""
        while True:
            try:
                data = self.get_simulated_data()
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
        logger.info("🌌 INICIANDO SISTEMA CHIZHEVSKY UNIFICADO")
        
        # Iniciar monitoreo en hilo separado
        import threading
        monitor_thread = threading.Thread(target=self.run_monitoring, daemon=True)
        monitor_thread.start()
        
        # Iniciar servidor Flask
        try:
            self.app.run(host='0.0.0.0', port=27357, debug=False, use_reloader=False)
        except KeyboardInterrupt:
            logger.info("🛑 Sistema detenido por usuario")
        except Exception as e:
            logger.error(f"❌ Error en servidor Flask: {e}")

if __name__ == "__main__":
    sistema = SistemaChizhevskyUnificado()
    sistema.run()
