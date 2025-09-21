import re

# Leer el archivo principal
with open('sistema_chizhevsky_completo_corregido.py', 'r') as f:
    content = f.read()

# Buscar la función setup_routes
if 'def setup_routes(self):' in content:
    # Encontrar donde termina setup_routes
    lines = content.split('\n')
    setup_routes_start = None
    setup_routes_end = None
    
    for i, line in enumerate(lines):
        if 'def setup_routes(self):' in line:
            setup_routes_start = i
        elif setup_routes_start and line.strip() and not line.startswith('    ') and not line.startswith('        ') and 'def ' in line:
            setup_routes_end = i
            break
    
    if setup_routes_start and setup_routes_end:
        # Insertar los nuevos endpoints antes del final de setup_routes
        new_endpoints = '''
        @self.app.route('/api/cosmic/health-status')
        def cosmic_health_status():
            try:
                solar_data = self.get_spaceweather_data()
                health_data = self.health_connector.get_oms_health_alerts()
                predictions = self.predictor.predict_health_impact({
                    'activity_level': solar_data.get('riesgo', 0) * 10
                })
                
                return jsonify({
                    'solar_activity': solar_data.get('riesgo', 0) * 10,
                    'health_alerts': health_data,
                    'predictions': predictions,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/hospital/metrics')
        def hospital_metrics():
            try:
                metrics = self.health_connector.get_hospital_metrics('default')
                return jsonify(metrics)
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/early-warnings')
        def early_warnings():
            try:
                warnings = self.predictor.generate_early_warnings()
                return jsonify(warnings)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
'''
        
        # Insertar antes de la siguiente función
        lines.insert(setup_routes_end, new_endpoints)
        
        # Escribir el contenido modificado
        with open('sistema_chizhevsky_completo_corregido.py', 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ Endpoints inyectados correctamente")
    else:
        print("❌ No se pudo encontrar el final de setup_routes")
else:
    print("❌ No se encontró setup_routes en el archivo")
