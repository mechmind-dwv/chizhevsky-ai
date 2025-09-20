#!/usr/bin/env python3
"""
📊 REPORTE DIARIO CHIZHEVSKY AI
"""
import sqlite3
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

def generar_reporte_diario():
    """Generar reporte diario de actividad solar"""
    conn = sqlite3.connect('chizhevsky_alerts.db')
    cursor = conn.cursor()
    
    # Datos de las últimas 24 horas
    cursor.execute('''
        SELECT COUNT(*) as total_registros,
               AVG(llamaradas_m) as avg_m,
               AVG(llamaradas_x) as avg_x,
               MAX(riesgo_solar) as max_riesgo,
               COUNT(CASE WHEN riesgo_solar > 0.6 THEN 1 END) as alertas_altas
        FROM datos_solares 
        WHERE timestamp > datetime('now', '-1 day')
    ''')
    
    stats = cursor.fetchone()
    
    # Última alerta
    cursor.execute('''
        SELECT mensaje, timestamp 
        FROM alertas 
        ORDER BY timestamp DESC 
        LIMIT 1
    ''')
    
    ultima_alerta = cursor.fetchone()
    
    # Generar mensaje
    mensaje = f"📊 <b>REPORTE DIARIO CHIZHEVSKY AI</b>\n\n"
    mensaje += f"🕒 Período: Últimas 24 horas\n"
    mensaje += f"📈 Registros: {stats[0]}\n"
    mensaje += f"☀️ Llamaradas M promedio: {stats[1]:.1f}\n"
    mensaje += f"☀️ Llamaradas X promedio: {stats[2]:.1f}\n"
    mensaje += f"⚠️ Máximo riesgo: {stats[3]:.0%}\n"
    mensaje += f"🚨 Alertas de alta: {stats[4]}\n\n"
    
    if ultima_alerta:
        mensaje += f"⏰ <b>Última alerta:</b>\n{ultima_alerta[0]}\n"
        mensaje += f"🕒 {ultima_alerta[1]}\n"
    
    mensaje += f"\n🌌 <i>Sistema basado en estudios de Alexander Chizhevsky</i>"
    
    # Enviar por Telegram
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': mensaje,
        'parse_mode': 'HTML'
    }
    
    response = requests.post(url, json=payload)
    print(f"✅ Reporte enviado: {response.status_code}")

if __name__ == "__main__":
    generar_reporte_diario()
