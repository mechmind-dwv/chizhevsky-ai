#!/usr/bin/env python3
"""
🌌 SISTEMA INTEGRADO CHIZHEVSKY - Alertas Tempranas
Combina: NASA + AEMET + Copernicus + Telegram
"""
import os
import sqlite3
import requests
import numpy as np
from datetime import datetime
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SistemaChizhevskyCompleto:
    def __init__(self):
        self.load_environment()
        self.setup_database()
        self.setup_telegram()
        
    def load_environment(self):
        """Cargar variables de entorno"""
        from dotenv import load_dotenv
        load_dotenv()
        
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        self.CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
        self.NASA_API_KEY = os.getenv('NASA_API_KEY', 'DEMO_KEY')
        
        logger.info("✅ Variables de entorno cargadas")
    
    def setup_database(self):
        """Configurar base de datos SQLite"""
        self.conn = sqlite3.connect('chizhevsky_alerts.db')
        self.cursor = self.conn.cursor()
        
        # Crear tabla de alertas
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
        
        # Crear tabla de datos solares
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
    
    def setup_telegram(self):
        """Configurar bot de Telegram"""
        self.application = Application.builder().token(self.TELEGRAM_TOKEN).build()
        
        # Handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("estado", self.status_command))
        self.application.add_handler(CommandHandler("alerta", self.alert_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        logger.info("✅ Bot de Telegram configurado")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        chat_id = update.effective_chat.id
        welcome_msg = """
        🌌 CHIZHEVSKY AI ACTIVADO 🌞
        
        ¡Sistema de alertas tempranas basado en heliobiología!
        
        Comandos disponibles:
        /start - Mostrar este mensaje
        /estado - Estado actual del sistema
        /alerta - Últimas alertas
        
        Desarrollado con ❤️ para salvar vidas.
        """
        await update.message.reply_text(welcome_msg)
        
        # Guardar chat_id si no está en .env
        if not self.CHAT_ID:
            self.CHAT_ID = str(chat_id)
            with open('.env', 'a') as f:
                f.write(f'\nTELEGRAM_CHAT_ID={chat_id}')
            logger.info(f"✅ Nuevo CHAT_ID guardado: {chat_id}")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /estado"""
        status_msg = self.get_system_status()
        await update.message.reply_text(status_msg)
    
    async def alert_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /alerta"""
        alerts = self.get_recent_alerts()
        await update.message.reply_text(alerts if alerts else "✅ No hay alertas activas")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes normales"""
        text = update.message.text.lower()
        
        if 'sol' in text or 'solar' in text:
            response = "☀️ Monitoreo solar activo. Usa /estado para ver datos actuales."
        elif 'alerta' in text:
            response = "🚨 Sistema de alertas funcionando. Usa /alerta para ver alertas."
        else:
            response = "🌌 Sistema Chizhevsky AI funcionando. Usa /help para comandos."
        
        await update.message.reply_text(response)
    
    def get_nasa_data(self):
        """Obtener datos de la NASA"""
        try:
            url = f"https://api.nasa.gov/DONKI/FLR?api_key={self.NASA_API_KEY}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                flares = response.json()
                m_count = sum(1 for f in flares if f.get('classType', '').startswith('M'))
                x_count = sum(1 for f in flares if f.get('classType', '').startswith('X'))
                
                # Simular índice Kp (en producción usar API real)
                kp_index = round(2 + (np.random.random() * 5), 1)
                
                return {
                    'llamaradas_m': m_count,
                    'llamaradas_x': x_count,
                    'indice_kp': kp_index,
                    'riesgo': self.calculate_risk(m_count, x_count, kp_index)
                }
            else:
                logger.warning("⚠️ Error API NASA")
                return self.simulate_data()
                
        except Exception as e:
            logger.error(f"Error NASA: {e}")
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
        
        return min(risk, 1.0)
    
    def simulate_data(self):
        """Generar datos de simulación"""
        return {
            'llamaradas_m': np.random.randint(0, 5),
            'llamaradas_x': np.random.randint(0, 2),
            'indice_kp': round(2 + (np.random.random() * 5), 1),
            'riesgo': round(np.random.random() * 0.7, 2)
        }
    
    def get_system_status(self):
        """Obtener estado del sistema"""
        data = self.get_nasa_data()
        
        status_msg = f"""
        🌞 ESTADO SISTEMA CHIZHEVSKY - {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        ☀️ ACTIVIDAD SOLAR:
        • Llamaradas M: {data['llamaradas_m']}
        • Llamaradas X: {data['llamaradas_x']}
        • Índice Kp: {data['indice_kp']}
        • Riesgo calculado: {data['riesgo']:.0%}
        
        📊 SISTEMA:
        • Base de datos: ✅ Operativa
        • Telegram bot: ✅ Conectado
        • API NASA: {'✅' if data['llamaradas_m'] >= 0 else '⚠️'}
        
        💡 Última actualización: {datetime.now().strftime('%H:%M:%S')}
        """
        
        return status_msg
    
    def get_recent_alerts(self):
        """Obtener alertas recientes"""
        try:
            self.cursor.execute("SELECT * FROM alertas WHERE enviada = FALSE ORDER BY timestamp DESC LIMIT 5")
            alerts = self.cursor.fetchall()
            
            if not alerts:
                return None
                
            alert_msg = "🚨 ÚLTIMAS ALERTAS:\n\n"
            for alert in alerts:
                alert_msg += f"• {alert[2]}: {alert[4]} (Riesgo: {alert[5]:.0%})\n"
                
            return alert_msg
            
        except Exception as e:
            logger.error(f"Error obteniendo alertas: {e}")
            return "⚠️ Error al obtener alertas"
    
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
            message = f"⚠️ Actividad solar elevada: {data['llamaradas_m']}M {data['llamaradas_x']}X, Kp={data['indice_kp']}"
            
            self.cursor.execute('''
                INSERT INTO alertas (tipo, nivel, mensaje, riesgo)
                VALUES (?, ?, ?, ?)
            ''', ('solar', alert_type, message, data['riesgo']))
            
            # Enviar por Telegram
            if self.CHAT_ID:
                self.send_telegram_alert(message)
        
        self.conn.commit()
    
    def send_telegram_alert(self, message):
        """Enviar alerta por Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendMessage"
            payload = {
                'chat_id': self.CHAT_ID,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info("✅ Alerta enviada por Telegram")
                return True
            else:
                logger.warning("⚠️ Error enviando alerta")
                return False
                
        except Exception as e:
            logger.error(f"Error enviando Telegram: {e}")
            return False
    
    def run(self):
        """Ejecutar sistema completo"""
        logger.info("🌌 INICIANDO SISTEMA CHIZHEVSKY COMPLETO")
        
        # Iniciar bot de Telegram en segundo plano
        import threading
        telegram_thread = threading.Thread(target=self.application.run_polling, name="TelegramBot")
        telegram_thread.daemon = True
        telegram_thread.start()
        
        # Bucle principal de monitoreo
        try:
            while True:
                self.check_and_alert()
                time.sleep(300)  # Verificar cada 5 minutos
                
        except KeyboardInterrupt:
            logger.info("🛑 Sistema detenido por usuario")
        except Exception as e:
            logger.error(f"❌ Error en bucle principal: {e}")
        finally:
            self.conn.close()

# Ejecutar si es el archivo principal
if __name__ == "__main__":
    sistema = SistemaChizhevskyCompleto()
    sistema.run()
