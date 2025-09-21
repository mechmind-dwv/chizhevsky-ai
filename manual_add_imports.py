with open('sistema_chizhevsky_completo_corregido.py', 'r') as f:
    content = f.read()

# Añadir importaciones si faltan
if 'from hospital_integration.oms_connector_simple import CosmicHealthConnector' not in content:
    # Buscar donde añadir las importaciones (después de otras importaciones)
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'from chizhevsky_ai.core.hematology.integrator import HematologyIntegrator' in line:
            lines.insert(i+1, 'from hospital_integration.oms_connector_simple import CosmicHealthConnector')
            lines.insert(i+2, 'from predictive_analytics.cosmic_predictor_simple import CosmicPredictor')
            break
    
    with open('sistema_chizhevsky_completo_corregido.py', 'w') as f:
        f.write('\n'.join(lines))
    print("✅ Importaciones añadidas manualmente")
else:
    print("✅ Las importaciones ya existen")
