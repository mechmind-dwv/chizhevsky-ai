# chizhevsky_ai/historical_analysis/historical_database.py
"""
Gestión de la base de datos histórica para el análisis de Chizhevsky
"""
import sqlite3
from datetime import datetime

class HistoricalDatabase:
    def __init__(self, db_path="data/chizhevsky_historical.db"):
        self.db_path = db_path
    
    def add_mass_event(self, year, event_type, intensity, region, description, solar_activity):
        """Añadir evento histórico masivo a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO mass_events 
            (year, event_type, intensity, region, description, solar_activity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (year, event_type, intensity, region, description, solar_activity))
        
        conn.commit()
        conn.close()
        return True
    
    def get_events_by_period(self, start_year, end_year):
        """Obtener eventos por período histórico"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT year, event_type, intensity, region, description, solar_activity
            FROM mass_events 
            WHERE year BETWEEN ? AND ?
            ORDER BY year
        ''', (start_year, end_year))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'year': row[0],
                'type': row[1],
                'intensity': row[2],
                'region': row[3],
                'description': row[4],
                'solar_activity': row[5]
            }
            for row in results
        ]
