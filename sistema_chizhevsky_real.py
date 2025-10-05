#!/usr/bin/env python3
"""
SISTEMA CHIZHEVSKY AI - SOLO DATOS REALES
Sin simulación - Solo APIs reales
"""

import os
import logging
import sqlite3
from flask import Flask, jsonify
import requests
import time
from datetime import datetime

# Configuración REAL
from config.chizhevsky_real import ConfigReal, NOAARealFetcher

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SistemaChizhevskyReal:
    """Sistema SOLO con datos REALES"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.port = int(os.getenv('FLASK_PORT', 27357))
        self.config = ConfigReal()
        self.noaa_fetcher = NOAARealFetcher()
        self.setup_routes()
        self.setup_database()
        
    def setup_database(self):
        """Configurar base de datos REAL"""
        self.conn = sqlite3.connect(self.config.DB_PATH, check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS datos_solares_reales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                indice_kp REAL,
                riesgo_solar REAL,
                fuente TEXT,
                llamaradas_m INTEGER,
                llamaradas_x INTEGER
            )
        ''')
        self.conn.commit()
        
    def setup_routes(self):
        """Configurar rutas con datos REALES"""
        
        @self.app.route('/')
        def index():
            return jsonify({
                "sistema": "Chizhevsky AI - SOLO REAL", 
                "version": "3.0-REAL",
                "estado": "activo",
                "modo": "SOLO_DATOS_REALES",
                "simulacion": "DESACTIVADA"
            })
        
        @self.app.route('/api/datos-reales')
        def api_datos_reales():
            """Endpoint SOLO datos REALES"""
            try:
                datos_reales = self.noaa_fetcher.get_real_solar_data()
                
                # Guardar en BD
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO datos_solares_reales 
                    (timestamp, indice_kp, riesgo_solar, fuente, llamaradas_m, llamaradas_x)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    datos_reales['indice_kp'],
                    datos_reales['riesgo_solar'], 
                    datos_reales['fuente'],
                    datos_reales['llamaradas_m'],
                    datos_reales['llamaradas_x']
                ))
                self.conn.commit()
                
                return jsonify(datos_reales)
                
            except Exception as e:
                logger.error(f"❌ Error datos reales: {e}")
                return jsonify({
                    "error": "No se pudieron obtener datos reales",
                    "fuente": "ERROR",
                    "timestamp": datetime.now().isoformat()
                }), 500
        
        @self.app.route('/api/estado')
        def api_estado():
            """Estado del sistema REAL"""
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM datos_solares_reales")
            total_registros = cursor.fetchone()[0]
            
            return jsonify({
                "sistema": "Chizhevsky AI - REAL",
                "registros_reales": total_registros,
                "ultima_actualizacion": datetime.now().isoformat(),
                "modo_simulacion": False,
                "estado": "operativo"
            })
        
        @self.app.route('/api/fuentes')
        def api_fuentes():
            """Fuentes de datos REALES configuradas"""
            return jsonify({
                "noaa_url": self.config.NOAA_API_URL,
                "nasa_url": self.config.NASA_API_URL,
                "spaceweather_url": self.config.SPACEWEATHER_API,
                "modo": "SOLO_REAL"
            })
    
    def obtener_datos_cosmicos_reales(self):
        """Bucle principal SOLO para datos REALES"""
        while True:
            try:
                datos = self.noaa_fetcher.get_real_solar_data()
                logger.info(f"🌞 DATOS REALES: Kp={datos['indice_kp']}, Riesgo={datos['riesgo_solar']}%, Fuente={datos['fuente']}")
                
                # Alertas solo si riesgo REAL es alto
                if datos['riesgo_solar'] > 60:
                    logger.warning(f"🚨 ALERTA REAL: Riesgo solar {datos['riesgo_solar']}%")
                    
            except Exception as e:
                logger.error(f"❌ Error en bucle real: {e}")
            
            time.sleep(300)  # 5 minutos entre actualizaciones REALES
    
    def run(self):
        """Ejecutar sistema REAL"""
        logger.info("🌌 INICIANDO SISTEMA CHIZHEVSKY - SOLO DATOS REALES")
        logger.info("🚫 MODO SIMULACIÓN: DESACTIVADO")
        logger.info(f"🌐 Servidor REAL en puerto {self.port}")
        
        # Iniciar bucle de datos reales en segundo plano
        import threading
        thread = threading.Thread(target=self.obtener_datos_cosmicos_reales, daemon=True)
        thread.start()
        
        # Iniciar servidor
        self.app.run(host='0.0.0.0', port=self.port, debug=False)

if __name__ == "__main__":
    sistema = SistemaChizhevskyReal()
    sistema.run()
