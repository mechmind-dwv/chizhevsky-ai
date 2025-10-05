#!/usr/bin/env python3
"""
Sistema Chizhevsky AI - Versión Corregida y Limpia
"""

import os
import logging
import sqlite3
from flask import Flask, jsonify
import requests
import time
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SistemaChizhevskyCorregido:
    def __init__(self):
        self.app = Flask(__name__)
        self.port = int(os.getenv('FLASK_PORT', 27357))  # Puerto diferente
        self.setup_routes()
        
    def setup_routes(self):
        """Configurar todas las rutas Flask DENTRO de la clase"""
        
        @self.app.route('/')
        def index():
            return jsonify({
                "sistema": "Chizhevsky AI", 
                "version": "2.0",
                "estado": "activo"
            })
        
        @self.app.route('/api/datos')
        def api_datos():
            """Endpoint de datos solares"""
            return jsonify({
                "indice_kp": 4.1,
                "riesgo_solar": 0.0,
                "fuente": "SIMULADO",
                "timestamp": datetime.now().isoformat()
            })
        
        @self.app.route('/cosmic-api/health-status')
        def health_status():
            return jsonify({"status": "healthy", "system": "Chizhevsky AI"})
    
    def run(self):
        """Ejecutar el sistema"""
        logger.info(f"🌌 INICIANDO SISTEMA CHIZHEVSKY CORREGIDO")
        logger.info(f"🌐 Servidor Flask iniciado en puerto {self.port}")
        
        try:
            self.app.run(host='0.0.0.0', port=self.port, debug=False)
        except OSError as e:
            logger.error(f"❌ Error iniciando servidor: {e}")
            logger.info("🔄 Intentando con puerto alternativo...")
            self.port = 27358  # Puerto alternativo
            self.app.run(host='0.0.0.0', port=self.port, debug=False)

if __name__ == "__main__":
    sistema = SistemaChizhevskyCorregido()
    sistema.run()
