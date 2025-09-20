#!/usr/bin/env python3
"""
🌐 PANEL DE CONTROL WEB CHIZHEVSKY AI
"""
from flask import Flask, render_template, jsonify
import sqlite3
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)

def get_db_data():
    """Obtener datos de la base de datos"""
    conn = sqlite3.connect('chizhevsky_alerts.db')
    cursor = conn.cursor()
    
    # Últimos datos solares
    cursor.execute('SELECT * FROM datos_solares ORDER BY timestamp DESC LIMIT 10')
    datos_solares = cursor.fetchall()
    
    # Estadísticas
    cursor.execute('''
        SELECT COUNT(*), 
               AVG(riesgo_solar), 
               MAX(riesgo_solar),
               COUNT(CASE WHEN riesgo_solar > 0.6 THEN 1 END)
        FROM datos_solares 
        WHERE timestamp > datetime('now', '-1 day')
    ''')
    stats = cursor.fetchone()
    
    # Últimas alertas
    cursor.execute('SELECT * FROM alertas ORDER BY timestamp DESC LIMIT 5')
    alertas = cursor.fetchall()
    
    conn.close()
    
    return {
        'datos_solares': datos_solares,
        'estadisticas': {
            'total_registros': stats[0],
            'riesgo_promedio': stats[1],
            'riesgo_maximo': stats[2],
            'alertas_altas': stats[3]
        },
        'alertas': alertas
    }

@app.route('/')
def index():
    """Página principal del panel de control"""
    data = get_db_data()
    return render_template('index.html', data=data)

@app.route('/api/datos')
def api_datos():
    """API para datos JSON"""
    return jsonify(get_db_data())

@app.route('/api/estado')
def api_estado():
    """API de estado del sistema"""
    return jsonify({
        'estado': 'activo',
        'ultima_actualizacion': datetime.now().isoformat(),
        'sistema': 'Chizhevsky AI NOAA',
        'version': '2.0'
    })

def run_flask():
    """Ejecutar servidor Flask"""
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    # Ejecutar en segundo plano
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    print("🌐 Panel de control web iniciado: http://localhost:5000")
    print("📊 API disponible: http://localhost:5000/api/datos")
    
    # Mantener el script vivo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Panel detenido")
