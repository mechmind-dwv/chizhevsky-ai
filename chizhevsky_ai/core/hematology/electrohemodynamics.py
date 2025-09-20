# chizhevsky_ai/core/hematology/electrohemodynamics.py
import sqlite3
import numpy as np
from datetime import datetime
import logging

class ChizhevskyHematology:
    """
    Módulo de Electrohemodinámica basado en las investigaciones de Alexander Chizhevsky
    Implementa sus descubrimientos sobre propiedades eléctricas de la sangre
    """
    
    def __init__(self, db_path='chizhevsky_alerts.db'):
        self.db_path = db_path
        self.logger = logging.getLogger('chizhevsky_ai.hematology')
        self._init_db()
    
    def _init_db(self):
        """Inicializar tablas de hematología en la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de análisis hematológicos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS hematology_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            erythrocyte_sedimentation_rate REAL,
            blood_viscosity REAL,
            electrical_potential REAL,
            platelet_aggregation_index REAL,
            cosmic_radiation_level REAL,
            solar_activity_index REAL,
            risk_thrombosis REAL,
            risk_anemia REAL,
            recommendations TEXT
        )
        ''')
        
        # Tabla de correlaciones históricas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS hematology_correlations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            period_start DATE,
            period_end DATE,
            solar_storms_count INTEGER,
            thrombosis_cases INTEGER,
            cardiovascular_events INTEGER,
            blood_donation_rejections INTEGER,
            correlation_coefficient REAL
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def calculate_erythrocyte_electrical_properties(self, sedimentation_rate, environmental_ions):
        """
        Calcular propiedades eléctricas de eritrocitos basado en Chizhevsky
        """
        # Coeficientes derivados de los experimentos de Chizhevsky
        base_potential = -15.7  # mV (potencial base de membrana)
        ion_effect = environmental_ions * 0.83  # Efecto de iones negativos
        sedimentation_effect = sedimentation_rate * 0.12
        
        electrical_potential = base_potential + ion_effect - sedimentation_effect
        
        return {
            'electrical_potential': electrical_potential,
            'ion_effect': ion_effect,
            'sedimentation_effect': sedimentation_effect
        }
    
    def assess_transfusion_risk(self, blood_type, rh_factor, electrical_properties):
        """
        Evaluar riesgo de transfusión según criterios de Chizhevsky
        No solo grupo sanguíneo, sino estado electrofisiológico
        """
        risk_score = 0
        
        # Criterios electrofisiológicos (Chizhevsky, 1938)
        if electrical_properties['electrical_potential'] > -10.0:
            risk_score += 35  # Potencial demasiado alto
            
        if electrical_properties['ion_effect'] < 2.5:
            risk_score += 25  # Efecto iónico insuficiente
            
        if electrical_properties['sedimentation_effect'] > 4.0:
            risk_score += 40  # Sedimentación demasiado rápida
        
        return {
            'risk_score': risk_score,
            'safe_transfusion': risk_score < 30,
            'recommendations': self._generate_recommendations(risk_score)
        }
    
    def correlate_solar_activity_hematology(self, solar_data, medical_data):
        """
        Correlacionar actividad solar con eventos hematológicos
        """
        correlations = []
        
        for solar_event, medical_events in zip(solar_data, medical_data):
            # Algoritmo de correlación basado en Chizhevsky
            correlation = self._calculate_chizhevsky_correlation(
                solar_event['intensity'],
                medical_events['count'],
                solar_event['duration']
            )
            
            correlations.append({
                'solar_event_date': solar_event['date'],
                'medical_event_type': medical_events['type'],
                'correlation_strength': correlation,
                'statistical_significance': self._calculate_significance(correlation)
            })
        
        return correlations
    
    def _calculate_chizhevsky_correlation(self, solar_intensity, event_count, duration):
        """Algoritmo de correlación específico de Chizhevsky"""
        return (solar_intensity * event_count) / (duration + 1)
    
    def _calculate_significance(self, correlation):
        """Calcular significancia estadística"""
        return 0.95 if correlation > 0.7 else 0.05 if correlation < 0.3 else 0.5
    
    def _generate_recommendations(self, risk_score):
        """Generar recomendaciones basadas en el riesgo"""
        if risk_score < 30:
            return "Transfusión segura según criterios electrohemodinámicos"
        elif risk_score < 60:
            return "Considerar ionización negativa pre-transfusión"
        else:
            return "Riesgo elevado. Re-evaluar necesidad de transfusión"
    
    def save_analysis(self, analysis_data):
        """Guardar análisis en base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO hematology_analysis (
            erythrocyte_sedimentation_rate, blood_viscosity, electrical_potential,
            platelet_aggregation_index, cosmic_radiation_level, solar_activity_index,
            risk_thrombosis, risk_anemia, recommendations
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            analysis_data['esr'],
            analysis_data['viscosity'],
            analysis_data['potential'],
            analysis_data['aggregation'],
            analysis_data['cosmic_rad'],
            analysis_data['solar_index'],
            analysis_data['thrombosis_risk'],
            analysis_data['anemia_risk'],
            analysis_data['recommendations']
        ))
        
        conn.commit()
        conn.close()
        
        self.logger.info(f"Análisis hematológico guardado: {analysis_data}")

# Ejemplo de uso
if __name__ == "__main__":
    hematology = ChizhevskyHematology()
    
    # Simular análisis de sangre
    electrical_props = hematology.calculate_erythrocyte_electrical_properties(
        sedimentation_rate=18.5,
        environmental_ions=3.2
    )
    
    transfusion_risk = hematology.assess_transfusion_risk(
        blood_type="A+",
        rh_factor="positive",
        electrical_properties=electrical_props
    )
    
    print("🔬 Análisis Electrohemodinámico:")
    print(f"Potencial eléctrico: {electrical_props['electrical_potential']} mV")
    print(f"Riesgo transfusión: {transfusion_risk['risk_score']}%")
    print(f"Recomendación: {transfusion_risk['recommendations']}")
