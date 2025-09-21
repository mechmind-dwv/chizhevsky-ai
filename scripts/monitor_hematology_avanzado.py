#!/usr/bin/env python3
"""
🔥 MONITOR DE HEMATOLOGÍA AVANZADO - Sistema Chizhevsky AI
Monitoreo en tiempo real de correlaciones solares-hematológicas con alertas
"""

import time
import logging
import requests
from datetime import datetime
import json

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hematology_advanced.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('hematology_advanced')

class HematologyMonitorAvanzado:
    def __init__(self, api_url="http://localhost:27777"):
        self.api_url = api_url
        self.alert_threshold = 7.0  # Umbral para alertas CRÍTICAS
        
    def get_hematology_risk(self):
        """Obtener evaluación de riesgo actual"""
        try:
            response = requests.get(f"{self.api_url}/api/hematology/risk", timeout=10)
            return response.json()
        except Exception as e:
            logger.error(f"❌ Error obteniendo riesgo: {e}")
            return None
    
    def analyze_blood_sample(self, sedimentation_rate, environmental_ions):
        """Analizar muestra sanguínea"""
        try:
            payload = {
                "sedimentation_rate": sedimentation_rate,
                "environmental_ions": environmental_ions
            }
            response = requests.post(
                f"{self.api_url}/api/hematology/analysis",
                json=payload,
                timeout=10
            )
            return response.json()
        except Exception as e:
            logger.error(f"❌ Error en análisis: {e}")
            return None
    
    def check_system_health(self):
        """Verificar salud del sistema"""
        try:
            response = requests.get(f"{self.api_url}/status", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_alert(self, risk_data):
        """Generar alerta basada en datos de riesgo"""
        if risk_data['solar_activity'] >= self.alert_threshold:
            alert_msg = (
                f"🚨 ALERTA HEMATOLÓGICA CRÍTICA\n"
                f"• Actividad solar: {risk_data['solar_activity']}\n"
                f"• Riesgo: {risk_data['hematology_risk']}\n"
                f"• Sistemas afectados: {', '.join(risk_data['affected_systems'])}\n"
                f"• Recomendaciones: {risk_data['recommendations'][0]}"
            )
            logger.warning(alert_msg)
            return True
        return False
    
    def continuous_monitoring(self):
        """Monitoreo continuo"""
        logger.info("🔥 INICIANDO MONITOR AVANZADO DE HEMATOLOGÍA")
        
        sample_count = 0
        while True:
            try:
                # Verificar que el sistema esté vivo
                if not self.check_system_health():
                    logger.error("❌ Sistema no responde - Reintentando en 30s")
                    time.sleep(30)
                    continue
                
                # Obtener riesgo actual
                risk_data = self.get_hematology_risk()
                if risk_data:
                    logger.info(
                        f"📈 Riesgo: {risk_data['hematology_risk']} | "
                        f"Solar: {risk_data['solar_activity']} | "
                        f"Hora: {datetime.now().strftime('%H:%M:%S')}"
                    )
                    
                    # Generar alerta si es necesario
                    self.generate_alert(risk_data)
                
                # Cada 10 muestras, hacer análisis completo
                if sample_count % 10 == 0:
                    analysis = self.analyze_blood_sample(
                        sedimentation_rate=18.0 + (sample_count % 10),
                        environmental_ions=3.0 + (sample_count % 5) * 0.5
                    )
                    if analysis:
                        logger.info(
                            f"🔬 Análisis: Potencial={analysis['electrical_potential']:.2f}mV | "
                            f"Iones={analysis['ion_effect']:.2f} | "
                            f"Sedimentación={analysis['sedimentation_effect']:.2f}"
                        )
                
                sample_count += 1
                time.sleep(300)  # 5 minutos entre chequeos
                
            except KeyboardInterrupt:
                logger.info("⏹️ Monitor detenido por usuario")
                break
            except Exception as e:
                logger.error(f"💥 Error en monitor: {e}")
                time.sleep(60)

def main():
    monitor = HematologyMonitorAvanzado()
    monitor.continuous_monitoring()

if __name__ == "__main__":
    main()
