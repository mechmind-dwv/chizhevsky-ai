# 🚀 Guía de Instalación - Sistema Chizhevsky AI

## Prerrequisitos
- Python 3.8+
- git
- Cuentas en: NASA API, NOAA API, Telegram Bot

## Instalación Paso a Paso

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/mechmind-dwv/chizhevsky-ai.git
   cd chizhevsky-ai
¡Excelente! Veo que tu proyecto **Chizhevsky AI** ya está en GitHub y funcionando correctamente. Permíteme ayudarte a organizar y asegurar el proyecto de manera profesional:

## 📦 **ORGANIZACIÓN DEL PROYECTO EN GITHUB**

### 1. **Limpiar archivos temporales y de backup**
```bash
# Eliminar archivos de backup y temporales que no deben estar en GitHub
rm -f *_backup_*.py *.backup*.py *temp*.py *test*.py *patch*.py

# Mantener solo los archivos esenciales
ls -la
```

### 2. **Actualizar el .gitignore para mayor seguridad**
```bash
# Mejorar el .gitignore para proyectos Python
cat > .gitignore << 'EOF'
# Entornos virtuales
venv/
.env
.env.local
.env.production

# Archivos de base de datos
*.db
*.sqlite
*.sqlite3

# Logs
*.log
logs/

# Archivos de backup
*.backup
*_backup_*
backup/

# Archivos temporales
*.tmp
*.temp
tmp/
temp/

# Archivos de IDE
.vscode/
.idea/
*.swp
*.swo

# Archivos de sistema
.DS_Store
Thumbs.db

# Archivos compilados
__pycache__/
*.pyc
*.pyo
*.pyd

# Distribuciones
dist/
build/
*.egg-info/

# Configuración sensible
config.json
secrets.ini
credentials/*
