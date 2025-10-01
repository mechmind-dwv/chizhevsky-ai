# chizhevsky_ai/integrator_chizhevsky.py
"""
Integrador principal del sistema Chizhevsky AI
Combina análisis histórico con monitoreo moderno
"""
import logging
from datetime import datetime
from historical_analysis import ChizhevskyCorrelator, HistoricalDatabase
from galactic_monitoring import GalacticMonitor, SolarPredictor

logger = logging.getLogger("ChizhevskyIntegrator")

class ChizhevskyIntegrator:
    def __init__(self):
        self.correlator = ChizhevskyCorrelator()
        self.historical_db = HistoricalDatabase()
        self.galactic_monitor = GalacticMonitor()
        self.solar_predictor = SolarPredictor()
        
        # Inicializar datos
        self.correlator.load_chizhevsky_data()
    
    def generate_full_report(self):
        """Generar reporte completo del sistema Chizhevsky"""
        historical_data = self.correlator.get_historical_correlations()
        current_activity = self.galactic_monitor.monitor_current_activity()
        future_predictions = self.solar_predictor.predict_future_cycles(3)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'system': 'Chizhevsky AI Integrated System',
            'historical_analysis': {
                'total_cycles_analyzed': len(historical_data),
                'average_correlation': sum(
                    d['correlation'] for d in historical_data
                ) / len(historical_data),
                'strongest_correlation': max(
                    historical_data, key=lambda x: x['correlation']
                )
            },
            'current_activity': current_activity,
            'future_predictions': future_predictions,
            'chizhevsky_quote': "El Sol no calla. Sus tormentas gritan verdades que los imperios intentaron silenciar."
        }
        
        return report
    
    def check_historical_patterns(self):
        """Verificar patrones históricos contra actividad actual"""
        historical = self.correlator.get_historical_correlations()
        current = self.galactic_monitor.monitor_current_activity()
        
        # Encontrar ciclo histórico más similar
        similar_cycle = min(
            historical,
            key=lambda x: abs(x['sunspots'] - current['sunspots'])
        )
        
        return {
            'current_activity': current,
            'most_similar_historical_cycle': similar_cycle,
            'similarity_score': 1 - (abs(similar_cycle['sunspots'] - current['sunspots']) / 200)
        }
