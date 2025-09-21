import re

with open('sistema_chizhevsky_completo_corregido.py', 'r') as f:
    content = f.read()

# Buscar las importaciones existentes
if 'from chizhevsky_ai.core.hematology.integrator import HematologyIntegrator' in content:
    # Añadir las nuevas importaciones después de la existente
    new_imports = '''
from hospital_integration.oms_connector import CosmicHealthConnector
from predictive_analytics.cosmic_predictor import CosmicPredictor
'''
    
    content = content.replace(
        'from chizhevsky_ai.core.hematology.integrator import HematologyIntegrator',
        'from chizhevsky_ai.core.hematology.integrator import HematologyIntegrator\nfrom hospital_integration.oms_connector import CosmicHealthConnector\nfrom predictive_analytics.cosmic_predictor import CosmicPredictor'
    )
    
    with open('sistema_chizhevsky_completo_corregido.py', 'w') as f:
        f.write(content)
    
    print("✅ Importaciones añadidas correctamente")
else:
    print("❌ No se encontró la importación de HematologyIntegrator")
