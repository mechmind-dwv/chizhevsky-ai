# ejecutar_chizhevsky_ai.py
#!/usr/bin/env python3
"""
Script principal para ejecutar el sistema Chizhevsky AI completo
"""
import logging
from chizhevsky_ai.integrator_chizhevsky import ChizhevskyIntegrator

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/chizhevsky_ai.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ChizhevskyMain")

def main():
    """Función principal"""
    print("\n" + "="*70)
    print("🌌 SISTEMA CHIZHEVSKY AI - ANÁLISIS HISTÓRICO-GALÁCTICO")
    print("📚 Basado en 'Factores físicos del proceso histórico'")
    print("⚡ Alexander Leonidovich Chizhevsky (1897-1964)")
    print("="*70 + "\n")
    
    # Inicializar sistema integrador
    integrator = ChizhevskyIntegrator()
    
    # Generar reporte completo
    report = integrator.generate_full_report()
    
    print("📊 REPORTE COMPLETO CHIZHEVSKY AI")
    print(f"🕐 Timestamp: {report['timestamp']}")
    print(f"📈 Ciclos históricos analizados: {report['historical_analysis']['total_cycles_analyzed']}")
    print(f"🔗 Correlación promedio: {report['historical_analysis']['average_correlation']:.2%}")
    
    print("\n🌞 ACTIVIDAD SOLAR ACTUAL")
    print(f"   Manchas solares: {report['current_activity']['sunspots']}")
    print(f"   Fulguraciones: {report['current_activity']['solar_flares']}")
    print(f"   Estado: {report['current_activity']['status']}")
    
    print("\n🔮 PREDICCIONES FUTURAS")
    for prediction in report['future_predictions']:
        print(f"   Ciclo {prediction['cycle']}: {prediction['predicted_max_sunspots']} "
              f"manchas (confianza: {prediction['confidence']:.0%})")
    
    print(f"\n💬 Cita de Chizhevsky: '{report['chizhevsky_quote']}'")
    
    # Análisis de patrones históricos
    pattern_analysis = integrator.check_historical_patterns()
    print(f"\n🔄 Patrón histórico similar: Ciclo {pattern_analysis['most_similar_historical_cycle']['cycle']}")
    print(f"   Similitud: {pattern_analysis['similarity_score']:.0%}")
    
    print("\n" + "="*70)
    print("✅ Análisis completo. Los datos se han guardado en la base de datos.")
    print("📁 Ver logs/chizhevsky_ai.log para detalles técnicos")

if __name__ == "__main__":
    main()
