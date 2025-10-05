#!/usr/bin/env python3
"""
🌌 SISTEMA CHIZHEVSKY OFFLINE - Funciona sin conexión
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

class SistemaChizhevskyOffline:
    def __init__(self):
        self.load_environment()
        self.setup_database()
        
    def load_environment(self):
        """Cargar variables de entorno"""
        load_dotenv()
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        self.CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
        logger.info("✅ Variables de entorno cargadas")
    
    def setup_database(self):
        """Configurar base de datos SQLite"""
        self.conn = sqlite3.connect('chizhevsky_alerts.db')
        self.cursor = self.conn.cursor()
        
        # Verificar y crear tablas si no existen
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
        
        self.conn.commit()
        logger.info("✅ Base de datos configurada")
    
    def get_simulated_data(self):
        """Generar datos solares simulados realistas"""
        # Simular ciclo solar diario
        hora_actual = datetime.now().hour
        ciclo_diario = np.sin(hora_actual * np.pi / 12)
        
        return {
            'llamaradas_m': max(0, int(3 + ciclo_diario * 2)),
            'llamaradas_x': 1 if ciclo_diario > 0.8 else 0,
            'indice_kp': round(2 + abs(ciclo_diario) * 3, 1),
            'viento_velocidad': 400 + ciclo_diario * 200,
            'viento_densidad': 3 + abs(ciclo_diario) * 2,
            'protones_10mev': int(100 + abs(ciclo_diario) * 300),
            'protones_100mev': int(10 + abs(ciclo_diario) * 20),
            'riesgo': self.calculate_risk(ciclo_diario),
            'fuente': 'SIMULADO'
        }
    
    def calculate_risk(self, ciclo_diario):
        """Calcular riesgo basado en ciclo simulado"""
        riesgo_base = 0.3 + abs(ciclo_diario) * 0.4
        return min(riesgo_base, 0.9)
    
    def send_telegram_message(self, message):
        """Enviar mensaje por Telegram (con fallback a log)"""
        if not self.TELEGRAM_TOKEN or not self.CHAT_ID:
            logger.warning("⚠️ Credenciales de Telegram no configuradas")
            return False
        
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
            logger.warning(f"⚠️ Error enviando Telegram: {e}")
            # Guardar mensaje para enviar luego
            self.save_pending_message(message)
            return False
    
    def save_pending_message(self, message):
        """Guardar mensajes pendientes para enviar luego"""
        try:
            self.cursor.execute('''
                INSERT INTO alertas (tipo, nivel, mensaje, riesgo, enviada)
                VALUES (?, ?, ?, ?, ?)
            ''', ('telegram', 'pendiente', message, 0.5, False))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error guardando mensaje pendiente: {e}")
    
    def check_and_alert(self):
        """Verificar y enviar alertas"""
        data = self.get_simulated_data()
        
        # Guardar datos
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
        except Exception as e:
            logger.error(f"Error insertando datos: {e}")
            # Recrear tabla si hay error
            self.setup_database()
            return data
        
        # Verificar si hay que alertar
        if data['riesgo'] > 0.6:
            alert_type = "ALTA"
            message = f"⚠️ <b>ALERTA SOLAR SIMULADA</b>\n\n"
            message += f"• 📊 Riesgo: {data['riesgo']:.0%}\n"
            message += f"• ☀️ Llamaradas M: {data['llamaradas_m']}\n"
            message += f"• ☀️ Llamaradas X: {data['llamaradas_x']}\n"
            message += f"• 🧲 Índice Kp: {data['indice_kp']}\n"
            message += f"• 💨 Viento solar: {data['viento_velocidad']} km/s\n"
            message += f"• ⚛️ Protones >10MeV: {data['protones_10mev']}\n"
            message += f"• 📡 Fuente: {data['fuente']}\n\n"
            message += f"🌌 <i>Sistema en modo simulación - Basado en Alexander Chizhevsky</i>"
            
            try:
                self.cursor.execute('''
                    INSERT INTO alertas (tipo, nivel, mensaje, riesgo)
                    VALUES (?, ?, ?, ?)
                ''', ('solar', alert_type, message, data['riesgo']))
            except Exception as e:
                logger.error(f"Error insertando alerta: {e}")
            
            # Enviar por Telegram
            self.send_telegram_message(message)
        
        self.conn.commit()
        return data
    
    def run(self):
        """Ejecutar sistema completo"""
        logger.info("🌌 INICIANDO SISTEMA CHIZHEVSKY OFFLINE")
        
        # Mensaje de inicio
        self.send_telegram_message(
            "🚀 <b>SISTEMA CHIZHEVSKY OFFLINE ACTIVADO</b>\n\n"
            "✅ Monitoreo solar en modo simulación\n"
            "🌌 Basado en estudios de Alexander Chizhevsky\n"
            "☀️ Alertas automáticas activas\n"
            "📊 Datos simulados por ciclo diario"
        )
        
        # Bucle principal
        try:
            while True:
                data = self.check_and_alert()
                
                logger.info(
                    f"📊 Datos simulados: {data['llamaradas_m']}M {data['llamaradas_x']}X, "
                    f"Kp={data['indice_kp']}, Viento={data['viento_velocidad']}km/s, "
                    f"Riesgo={data['riesgo']:.0%}"
                )
                
                time.sleep(300)  # Esperar 5 minutos
                
        except KeyboardInterrupt:
            logger.info("🛑 Sistema detenido por usuario")
            self.send_telegram_message("🛑 <b>SISTEMA DETENIDO</b>\n\nMonitoreo solar interrumpido")
        except Exception as e:
            logger.error(f"❌ Error en bucle principal: {e}")
        finally:
            self.conn.close()

if __name__ == "__main__":
    sistema = SistemaChizhevskyOffline()
    sistema.run()
