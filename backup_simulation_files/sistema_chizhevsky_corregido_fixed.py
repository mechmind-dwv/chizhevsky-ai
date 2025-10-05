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
FLASK_PORT = 27777  # Nuevo puerto

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
    
    # ... (el resto del código se mantiene igual)
    # CONTINÚA CON TODAS LAS DEMÁS FUNCIONES EXISTENTES

if __name__ == "__main__":
    sistema = SistemaChizhevskyCorregido()
    sistema.run()
