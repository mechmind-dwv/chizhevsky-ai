import re

with open('sistema_chizhevsky_completo_corregido.py', 'r') as f:
    content = f.read()

# Buscar el __init__ y añadir la inicialización
if 'self.hematology_integrator = HematologyIntegrator(self)' in content:
    # Añadir después de hematology_integrator
    new_init_code = '''
        self.health_connector = CosmicHealthConnector()
        self.predictor = CosmicPredictor()'''
    
    content = content.replace(
        '        self.hematology_integrator = HematologyIntegrator(self)',
        '        self.hematology_integrator = HematologyIntegrator(self)\n        self.health_connector = CosmicHealthConnector()\n        self.predictor = CosmicPredictor()'
    )
    
    with open('sistema_chizhevsky_completo_corregido.py', 'w') as f:
        f.write(content)
    
    print("✅ Inicialización añadida correctamente")
else:
    print("❌ No se encontró la inicialización de hematology_integrator")
