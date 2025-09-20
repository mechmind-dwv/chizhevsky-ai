#!/bin/bash
# Script de inicio para entorno de producción

echo "🚀 Iniciando Sistema Chizhevsky AI en modo producción..."
echo "📅 $(date)"
echo ""

# Verificar que el entorno virtual esté activado
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Activando entorno virtual..."
    source venv/bin/activate
fi

# Verificar que el archivo .env exista
if [ ! -f .env ]; then
    echo "❌ Error: Archivo .env no encontrado"
    echo "💡 Copie config/.env.example a .env y configure sus API keys"
    exit 1
fi

# Verificar que la base de datos existe
if [ ! -f "chizhevsky_alerts.db" ]; then
    echo "⚠️  Base de datos no encontrada, verificando en data/..."
    if [ -f "data/chizhevsky_alerts.db" ]; then
        echo "📦 Moviendo base de datos a ubicación principal..."
        mv data/chizhevsky_alerts.db .
    else
        echo "💡 La base de datos se creará automáticamente al iniciar"
    fi
fi

# Verificar dependencias
echo "🔍 Verificando dependencias..."
pip install -r requirements.txt

# Iniciar el sistema
echo "🌌 Iniciando Sistema Chizhevsky AI..."
python sistema_chizhevsky_completo_corregido.py
