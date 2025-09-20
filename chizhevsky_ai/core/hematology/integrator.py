# chizhevsky_ai/core/hematology/integrator.py
from .electrohemodynamics import ChizhevskyHematology
import requests
import json
from datetime import datetime
import logging

class HematologyIntegrator:
    """
    Integrador de datos hematológicos con el sistema principal de Chizhevsky AI
    """
    
    def __init__(self, main_system):
        self.main_system = main_system
        self.hematology = ChizhevskyHematology()
        # Usar el logger del módulo en lugar del sistema principal
        self.logger = logging.getLogger('chizhevsky_ai.hematology')
    
    def generate_hematology_alert(self, solar_activity_level):
        """Generar alertas hematológicas basadas en actividad solar"""
        risk_level = self._calculate_hematology_risk(solar_activity_level)
        
        alert = {
            'timestamp': datetime.now().isoformat(),
            'solar_activity': solar_activity_level,
            'hematology_risk': risk_level,
            'recommendations': self._generate_risk_recommendations(risk_level),
            'affected_systems': self._get_affected_biological_systems(risk_level)
        }
        
        return alert
    
    def _calculate_hematology_risk(self, solar_activity):
        """Calcular riesgo hematológico basado en actividad solar"""
        # Algoritmo basado en investigaciones de Chizhevsky
        if solar_activity > 8.0:
            return "CRÍTICO"
        elif solar_activity > 6.0:
            return "ALTO"
        elif solar_activity > 4.0:
            return "MODERADO"
        else:
            return "BAJO"
    
    def _generate_risk_recommendations(self, risk_level):
        """Generar recomendaciones basadas en el nivel de riesgo"""
        recommendations = {
            'CRÍTICO': [
                "Evitar procedimientos quirúrgicos electivos",
                "Aumentar monitorización de pacientes cardiovasculares",
                "Alertar bancos de sangre sobre posible aumento de rechazos"
            ],
            'ALTO': [
                "Monitorizar pacientes con historial de trombosis",
                "Considerar terapia de iones negativos en hospitales",
                "Revisar stocks de anticoagulantes"
            ],
            'MODERADO': [
                "Monitorizar sedimentación globular en pacientes sensibles",
                "Mantener alerta por posibles complicaciones hematológicas"
            ],
            'BAJO': [
                "Situación hematológica estable",
                "Continuar protocolos normales"
            ]
        }
        
        return recommendations.get(risk_level, [])
    
    def _get_affected_biological_systems(self, risk_level):
        """Obtener sistemas biológicos afectados según riesgo"""
        systems = {
            'CRÍTICO': ['Sistema cardiovascular', 'Coagulación sanguínea', 'Presión arterial'],
            'ALTO': ['Coagulación sanguínea', 'Viscosidad sanguínea'],
            'MODERADO': ['Sedimentación eritrocitaria', 'Potencial eléctrico sanguíneo'],
            'BAJO': ['Ninguno significativo']
        }
        
        return systems.get(risk_level, [])
    
    def update_hematological_correlations(self):
        """Actualizar correlaciones con datos solares actuales"""
        try:
            # Obtener datos solares actuales
            solar_data = self.main_system.get_solar_data()
            
            # Obtener datos médicos (simulado - integrar con API médica real)
            medical_data = self._fetch_medical_data()
            
            # Calcular correlaciones
            correlations = self.hematology.correlate_solar_activity_hematology(
                solar_data, medical_data
            )
            
            self.logger.info(f"Correlaciones actualizadas: {len(correlations)} registros")
            return correlations
            
        except Exception as e:
            self.logger.error(f"Error actualizando correlaciones: {str(e)}")
            return []
    
    def _fetch_medical_data(self):
        """Obtener datos médicos (simulado - implementar conexión real)"""
        # En implementación real, conectar con sistemas hospitalarios
        # o bases de datos de salud pública
        
        return [
            {'date': '2025-09-21', 'type': 'thrombosis', 'count': 12},
            {'date': '2025-09-20', 'type': 'cardiovascular', 'count': 8},
            {'date': '2025-09-19', 'type': 'transfusion_rejection', 'count': 3}
        ]
