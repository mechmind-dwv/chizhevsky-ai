with open('sistema_chizhevsky_completo_corregido.py', 'r') as f:
    content = f.read()

# Añadir inicialización si falta
if 'self.health_connector = CosmicHealthConnector()' not in content:
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'self.hematology_integrator = HematologyIntegrator(self)' in line:
            lines.insert(i+1, '        self.health_connector = CosmicHealthConnector()')
            lines.insert(i+2, '        self.predictor = CosmicPredictor()')
            break
    
    with open('sistema_chizhevsky_completo_corregido.py', 'w') as f:
        f.write('\n'.join(lines))
    print("✅ Inicialización añadida manualmente")
else:
    print("✅ La inicialización ya existe")
