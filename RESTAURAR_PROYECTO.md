# 🚀 RESTAURACIÓN RÁPIDA - Sistema Chizhevsky AI

## 📦 Recuperar proyecto completo:

```bash
# 1. Clonar repositorio
git clone https://github.com/mechmind-dwv/chizhevsky-ai.git
cd chizhevsky-ai

# 2. Restaurar entorno virtual
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp config/.env.example .env
# Editar .env con tus API keys reales

# 4. Iniciar servicios
# Servidor principal:
sudo systemctl start chizhevsky.service

# Servidor de salud (opcional):
python cosmic_health_server.py &

# Monitor (opcional):
python health_monitor.py
¡Perfecto! **Voy a guardar y asegurar todo el proyecto Chizhevsky AI**. Primero vamos a limpiar los archivos temporales y asegurar que todo esté commitado correctamente en GitHub.

```bash
# Detener todos los servicios primero
pkill -f "cosmic_health_server.py" 2>/dev/null || true
pkill -f "health_monitor.py" 2>/dev/null || true
sudo systemctl stop chizhevsky.service 2>/dev/null || true

# Limpiar archivos temporales y de prueba que no deben estar en GitHub
echo "🧹 Limpiando archivos temporales..."
rm -f json logging requests sqlite3 time *.pyc *.pyo __pycache__/* .*.swp .*.swo

# Verificar estado actual de git
echo "📊 Estado actual de Git:"
git status

# Quitar archivos no deseados del staging
git reset -- json logging requests sqlite3 time 2>/dev/null || true

# Añadir los archivos importantes que sí queremos guardar
echo "📦 Añadiendo archivos al repositorio..."
git add .
git reset -- sistema_chizhevsky_completo_corregido.backup.py 2>/dev/null || true

# Verificar qué se va a commitear
echo "📋 Cambios que se commitearán:"
git status --porcelain

# Hacer commit con todos los cambios
echo "💾 Haciendo commit de todo el proyecto..."
git commit -m "💫 Guardado completo del sistema Chizhevsky AI - Incluye módulo de electrohemodinámica, servidor de salud cósmica y dashboard"

# Subir a GitHub
echo "🚀 Subiendo a GitHub..."
git push origin main

# Crear tag para esta versión estable
echo "🏷️ Creando tag de versión..."
git tag v1.1.0
git push origin v1.1.0

# Verificar que todo está guardado
echo "✅ Verificación final:"
git log --oneline -3
git tag -l

# Crear script de restauración rápida
cat > RESTAURAR_PROYECTO.md << 'EOF'
# 🚀 RESTAURACIÓN RÁPIDA - Sistema Chizhevsky AI

## 📦 Recuperar proyecto completo:

```bash
# 1. Clonar repositorio
git clone https://github.com/mechmind-dwv/chizhevsky-ai.git
cd chizhevsky-ai

# 2. Restaurar entorno virtual
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp config/.env.example .env
# Editar .env con tus API keys reales

# 4. Iniciar servicios
# Servidor principal:
sudo systemctl start chizhevsky.service

# Servidor de salud (opcional):
python cosmic_health_server.py &

# Monitor (opcional):
python health_monitor.py
```

## 🌐 URLs de acceso:

- **Dashboard Principal:** http://localhost:27777/
- **Dashboard Salud:** http://localhost:27779/
- **API Principal:** http://localhost:27777/api/datos
- **API Salud:** http://localhost:27779/cosmic-api/health-status

## 🔧 Comandos útiles:

```bash
# Ver estado del servicio principal
sudo systemctl status chizhevsky.service

# Ver logs en tiempo real
sudo journalctl -u chizhevsky.service -f

# Probar endpoints
curl http://localhost:27777/
curl http://localhost:27779/cosmic-api/health-status
```

## 📋 Estructura guardada:

- ✅ Sistema principal con electrohemodinámica
- ✅ Servidor de salud cósmica independiente  
- ✅ Dashboard web funcional
- ✅ Monitor en tiempo real
- ✅ Base de datos con datos históricos
- ✅ Configuración de seguridad
