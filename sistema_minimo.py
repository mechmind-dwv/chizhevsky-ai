#!/usr/bin/env python3
"""
🌌 SISTEMA MÍNIMO CHIZHEVSKY - Versión simplificada
"""
import os
import requests
import time
from dotenv import load_dotenv

# Cargar configuración
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def enviar_mensaje(texto):
    """Enviar mensaje por Telegram"""
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': texto,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except:
        return False

def main():
    print("🌌 Iniciando sistema mínimo Chizhevsky...")
    
    # Mensaje de inicio
    enviar_mensaje('🚀 <b>SISTEMA CHIZHEVSKY ACTIVADO</b>\n\nMonitoreo solar y oceánico iniciado.')
    
    # Bucle principal
    while True:
        # Simular datos (en producción se conectaría a APIs reales)
        mensaje = f'🌞 <b>Reporte Chizhevsky</b>\n\n✅ Sistema funcionando\n🕒 {time.ctime()}\n\n<code>Modo: Monitoreo activo</code>'
        
        if enviar_mensaje(mensaje):
            print('✅ Mensaje enviado')
        else:
            print('❌ Error enviando mensaje')
        
        time.sleep(300)  # Esperar 5 minutos

if __name__ == "__main__":
    main()
