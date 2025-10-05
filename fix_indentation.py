# Leer el archivo
with open('sistema_chizhevsky_corregido.py', 'r') as f:
    lines = f.readlines()

# Encontrar y eliminar las líneas mal ubicadas
new_lines = []
skip_lines = False
for i, line in enumerate(lines, 1):
    if i >= 210 and i <= 220 and '@self.app.route' in line and 'if __name__' in ''.join(lines[max(0,i-5):i]):
        print(f"Línea {i} eliminada (mal ubicada): {line.strip()}")
        continue
    new_lines.append(line)

# Escribir el archivo corregido
with open('sistema_chizhevsky_corregido.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Corrección aplicada")
