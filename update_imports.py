import re

with open('sistema_chizhevsky_completo_corregido.py', 'r') as f:
    content = f.read()

# Reemplazar las importaciones problemáticas
content = content.replace(
    'from hospital_integration.oms_connector import CosmicHealthConnector',
    'from hospital_integration.oms_connector_simple import CosmicHealthConnector'
)

content = content.replace(
    'from predictive_analytics.cosmic_predictor import CosmicPredictor',
    'from predictive_analytics.cosmic_predictor_simple import CosmicPredictor'
)

with open('sistema_chizhevsky_completo_corregido.py', 'w') as f:
    f.write(content)

print("✅ Importaciones actualizadas a versiones simplificadas")
