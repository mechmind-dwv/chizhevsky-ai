# Leer archivo
with open('sistema_chizhevsky_corregido.py', 'r') as f:
    content = f.read()

# Encontrar donde termina la clase y comienza el if __name__
if "if __name__ == \"__main__\":" in content:
    parts = content.split("if __name__ == \"__main__\":")
    
    # Las rutas deben estar ANTES del if __name__, dentro de la clase
    main_part = parts[1]
    class_part = parts[0]
    
    # Buscar y remover @app.route mal ubicadas del main_part
    lines = main_part.split('\n')
    new_main_lines = []
    routes_to_move = []
    
    for line in lines:
        if '@app.route' in line or 'def api_datos' in line or 'def api_estado' in line:
            routes_to_move.append(line)
        else:
            new_main_lines.append(line)
    
    # Reconstruir el contenido
    new_content = class_part + '\n'.join(new_main_lines)
    
    with open('sistema_chizhevsky_corregido.py', 'w') as f:
        f.write(new_content)
    
    print(f"✅ Eliminadas {len(routes_to_move)} rutas mal ubicadas")
    for route in routes_to_move:
        print(f"   - {route.strip()}")
else:
    print("❌ No se encontró el patrón if __name__")
