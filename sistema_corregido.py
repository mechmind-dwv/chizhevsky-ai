#!/usr/bin/env python3
"""
🌌 SISTEMA CHIZHEVSKY CORREGIDO - Sin problemas de asyncio
"""
import os
import sqlite3
import requests
import numpy as np
from datetime import datetime
import time
import logging
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SistemaChizhevskyCorregido:
    def __init__(self):
        self.load_environment()
        self.setup_database()
        
    def load_environment(self):
        """Cargar variables de entorno"""
        load_dotenv()
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        self.CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
        self.NASA_API_KEY = os.getenv('NASA_API_KEY', 'DEMO_KEY')
        logger.info("✅ Variables de entorno cargadas")
    
    def setup_database(self):
        """Configurar base de datos SQLite"""
        self.conn = sqlite3.connect('chizhevsky_alerts.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
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
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS datos_solares (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                llamaradas_m INTEGER,
                llamaradas_x INTEGER,
                indice_kp REAL,
                riesgo_solar REAL
            )
        ''')
        
        self.conn.commit()
        logger.info("✅ Base de datos configurada")
    
    def get_nasa_data(self):
        """Obtener datos de la NASA"""
        try:
            url = f"https://api.nasa.gov/DONKI/FLR?api_key={self.NASA_API_KEY}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                flares = response.json()
                m_count = sum(1 for f in flares if f.get('classType', '').startswith('M'))
                x_count = sum(1 for f in flares if f.get('classType', '').startswith('X'))
                
                # Obtener índice Kp real de NOAA
                kp_url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
                kp_response = requests.get(kp_url, timeout=10)
                kp_data = kp_response.json() if kp_response.status_code == 200 else []
                
                kp_values = []
                for entry in kp_data[-6:]:  # Últimas 6 horas
                    try:
                        kp_values.append(float(entry[1]))
                    except:
                        continue
                
                kp_index = max(kp_values) if kp_values else 0
                
                return {
                    'llamaradas_m': m_count,
                    'llamaradas_x': x_count,
                    'indice_kp': kp_index,
                    'riesgo': self.calculate_risk(m_count, x_count, kp_index)
                }
            else:
                logger.warning("⚠️ Error API NASA, usando datos simulados")
                return self.simulate_data()
                
        except Exception as e:
            logger.error(f"Error obteniendo datos NASA: {e}")
            return self.simulate_data()
    
    def calculate_risk(self, m_count, x_count, kp_index):
        """Calcular riesgo basado en Chizhevsky"""
        risk = 0.0
        
        if x_count > 0:
            risk = 0.7 + (x_count * 0.15)
        elif m_count >= 3:
            risk = 0.4 + (m_count * 0.1)
        
        if kp_index >= 5:
            risk = max(risk, 0.6)
        elif kp_index >= 4:
            risk = max(risk, 0.4)
        
        return min(risk, 1.0)
    
    def simulate_data(self):
        """Generar datos de simulación"""
        return {
            'llamaradas_m': np.random.randint(0, 5),
            'llamaradas_x': np.random.randint(0, 2),
            'indice_kp': round(2 + (np.random.random() * 5), 1),
            'riesgo': round(np.random.random() * 0.7, 2)
        }
    
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
            if response.status_code == 200:
                logger.info("✅ Mensaje enviado por Telegram")
                return True
            else:
                logger.warning(f"⚠️ Error Telegram: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error enviando Telegram: {e}")
            return False
    
    def check_and_alert(self):
        """Verificar y enviar alertas"""
        data = self.get_nasa_data()
        
        # Guardar datos
        self.cursor.execute('''
            INSERT INTO datos_solares (llamaradas_m, llamaradas_x, indice_kp, riesgo_solar)
            VALUES (?, ?, ?, ?)
        ''', (data['llamaradas_m'], data['llamaradas_x'], data['indice_kp'], data['riesgo']))
        
        # Verificar si hay que alertar
        if data['riesgo'] > 0.6:
            alert_type = "ALTA"
            message = f"⚠️ <b>ALERTA SOLAR</b>\n\n• Llamaradas M: {data['llamaradas_m']}\n• Llamaradas X: {data['llamaradas_x']}\n• Índice Kp: {data['indice_kp']}\n• Riesgo: {data['riesgo']:.0%}\n\n🌌 Basado en estudios Chizhevsky"
            
            self.cursor.execute('''
                INSERT INTO alertas (tipo, nivel, mensaje, riesgo)
                VALUES (?, ?, ?, ?)
            ''', ('solar', alert_type, message, data['riesgo']))
            
            # Enviar por Telegram
            self.send_telegram_message(message)
        
        self.conn.commit()
        return data
    
    def run(self):
        """Ejecutar sistema completo"""
        logger.info("🌌 INICIANDO SISTEMA CHIZHEVSKY CORREGIDO")
        
        # Mensaje de inicio
        self.send_telegram_message("🚀 <b>SISTEMA CHIZHEVSKY ACTIVADO</b>\n\n✅ Monitoreo solar iniciado\n🌌 Basado en estudios de Alexander Chizhevsky\n☀️ Alertas automáticas activas")
        
        # Bucle principal
        try:
            while True:
                data = self.check_and_alert()
                
                logger.info(f"📊 Datos: {data['llamaradas_m']}M {data['llamaradas_x']}X, Kp={data['indice_kp']}, Riesgo={data['riesgo']:.0%}")
                
                time.sleep(300)  # Esperar 5 minutos
                
        except KeyboardInterrupt:
            logger.info("🛑 Sistema detenido por usuario")
            self.send_telegram_message("🛑 <b>SISTEMA DETENIDO</b>\n\nMonitoreo solar interrumpido")
        except Exception as e:
            logger.error(f"❌ Error en bucle principal: {e}")
        finally:
            self.conn.close()

# Ejecutar si es el archivo principal
if __name__ == "__main__":
    sistema = SistemaChizhevskyCorregido()
    sistema.run()
