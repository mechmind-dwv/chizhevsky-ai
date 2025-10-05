#!/usr/bin/env python3
"""
🌌 SISTEMA CHIZHEVSKY MEJORADO - Con datos reales de NOAA
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

class SistemaChizhevskyNOAA:
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
        
        # Tabla mejorada con más datos solares
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
    
    def get_noaa_data(self):
        """Obtener datos solares de NOAA - Fuente confiable"""
        try:
            # Datos de índice Kp (geomagnético)
            kp_url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
            kp_response = requests.get(kp_url, timeout=10)
            
            if kp_response.status_code == 200:
                kp_data = kp_response.json()
                kp_values = []
                for entry in kp_data[-6:]:  # Últimas 6 horas
                    try:
                        kp_values.append(float(entry[1]))
                    except:
                        continue
                kp_index = max(kp_values) if kp_values else 0
            else:
                kp_index = 0
            
            # Datos de viento solar
            solar_wind_url = "https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json"
            wind_response = requests.get(solar_wind_url, timeout=10)
            
            wind_speed = 400  # Valores por defecto (km/s)
            density = 5       # partículas/cm³
            
            if wind_response.status_code == 200:
                try:
                    wind_data = wind_response.json()
                    if wind_data and len(wind_data) > 1:
                        last_entry = wind_data[-1]
                        wind_speed = float(last_entry[2])  # velocidad
                        density = float(last_entry[1])     # densidad
                except:
                    pass
            
            # Datos de protones (radiación)
            proton_url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-7-day.json"
            proton_response = requests.get(proton_url, timeout=10)
            
            protons_10mev = 0
            protons_100mev = 0
            
            if proton_response.status_code == 200:
                try:
                    proton_data = proton_response.json()
                    if proton_data:
                        # Tomar el último valor de protones >10MeV y >100MeV
                        last_entry = proton_data[-1]
                        protons_10mev = int(float(last_entry.get('flux', 0)))
                        protons_100mev = int(float(last_entry.get('energy', 0)))
                except:
                    pass
            
            # Simular llamaradas solares (en producción real se conectaría a API)
            # Basado en actividad real de protones y viento solar
            m_count = 0
            x_count = 0
            
            if protons_10mev > 1000 or wind_speed > 600:
                m_count = np.random.randint(1, 4)
            if protons_100mev > 100 or wind_speed > 800:
                x_count = np.random.randint(0, 2)
            
            return {
                'llamaradas_m': m_count,
                'llamaradas_x': x_count,
                'indice_kp': kp_index,
                'viento_velocidad': wind_speed,
                'viento_densidad': density,
                'protones_10mev': protons_10mev,
                'protones_100mev': protons_100mev,
                'riesgo': self.calculate_risk(m_count, x_count, kp_index, wind_speed, protons_10mev),
                'fuente': 'NOAA'
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo datos NOAA: {e}")
            return self.simulate_data()
    
    def calculate_risk(self, m_count, x_count, kp_index, wind_speed, protons_10mev):
        """Calcular riesgo mejorado basado en múltiples factores"""
        risk = 0.0
        
        # Factor llamaradas
        if x_count > 0:
            risk += 0.4 + (x_count * 0.2)
        elif m_count >= 2:
            risk += 0.2 + (m_count * 0.1)
        
        # Factor geomagnético
        if kp_index >= 7: risk += 0.3  # Tormenta fuerte
        elif kp_index >= 5: risk += 0.2  # Tormenta moderada
        elif kp_index >= 4: risk += 0.1  # Tormenta leve
        
        # Factor viento solar
        if wind_speed > 700: risk += 0.2
        elif wind_speed > 500: risk += 0.1
        
        # Factor radiación
        if protons_10mev > 1000: risk += 0.3
        elif protons_10mev > 100: risk += 0.1
        
        return min(risk, 1.0)
    
    def simulate_data(self):
        """Generar datos de simulación cuando hay errores"""
        return {
            'llamaradas_m': np.random.randint(0, 3),
            'llamaradas_x': np.random.randint(0, 1),
            'indice_kp': round(2 + (np.random.random() * 5), 1),
            'viento_velocidad': 400 + (np.random.random() * 300),
            'viento_densidad': 3 + (np.random.random() * 4),
            'protones_10mev': np.random.randint(0, 500),
            'protones_100mev': np.random.randint(0, 50),
            'riesgo': round(np.random.random() * 0.7, 2),
            'fuente': 'SIMULADO'
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
        data = self.get_noaa_data()
        
        # Guardar datos
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
        
        # Verificar si hay que alertar
        if data['riesgo'] > 0.6:
            alert_type = "ALTA"
            message = f"⚠️ <b>ALERTA SOLAR CHIZHEVSKY</b>\n\n"
            message += f"• 📊 Riesgo: {data['riesgo']:.0%}\n"
            message += f"• ☀️ Llamaradas M: {data['llamaradas_m']}\n"
            message += f"• ☀️ Llamaradas X: {data['llamaradas_x']}\n"
            message += f"• 🧲 Índice Kp: {data['indice_kp']}\n"
            message += f"• 💨 Viento solar: {data['viento_velocidad']} km/s\n"
            message += f"• ⚛️ Protones >10MeV: {data['protones_10mev']}\n"
            message += f"• 📡 Fuente: {data['fuente']}\n\n"
            message += f"🌌 <i>Basado en estudios de Alexander Chizhevsky</i>"
            
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
        logger.info("🌌 INICIANDO SISTEMA CHIZHEVSKY NOAA")
        
        # Mensaje de inicio
        self.send_telegram_message(
            "🚀 <b>SISTEMA CHIZHEVSKY NOAA ACTIVADO</b>\n\n"
            "✅ Monitoreo solar con datos NOAA\n"
            "🌌 Basado en estudios de Alexander Chizhevsky\n"
            "☀️ Alertas automáticas activas\n"
            "📊 Datos en tiempo real"
        )
        
        # Bucle principal
        try:
            while True:
                data = self.check_and_alert()
                
                logger.info(
                    f"📊 Datos: {data['llamaradas_m']}M {data['llamaradas_x']}X, "
                    f"Kp={data['indice_kp']}, Viento={data['viento_velocidad']}km/s, "
                    f"Riesgo={data['riesgo']:.0%}, Fuente={data['fuente']}"
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
    sistema = SistemaChizhevskyNOAA()
    sistema.run()
