# install_chizhevsky_modules.sh
#!/bin/bash
echo "🌌 Instalando módulos Chizhevsky AI..."
echo "📁 Creando estructura de directorios..."

# Crear directorios necesarios
mkdir -p chizhevsky_ai/historical_analysis
mkdir -p chizhevsky_ai/galactic_monitoring
mkdir -p data logs

echo "📦 Instalando dependencias..."
pip install numpy scikit-learn requests python-dotenv

echo "✅ Módulos Chizhevsky AI instalados correctamente"
echo "🚀 Ejecutar: python ejecutar_chizhevsky_ai.py"
