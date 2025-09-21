#!/bin/bash
echo "🔧 Instalando dependencias en entorno virtual..."

# Asegurar que el entorno virtual está activo
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Entorno virtual no activo. Activando..."
    source venv/bin/activate
fi

# Instalar dependencias esenciales
pip install --upgrade pip
pip install requests==2.31.0
pip install pandas==2.0.3
pip install numpy==1.24.3
pip install scikit-learn==1.3.0
pip install Flask==2.3.3
pip install flask-cors==4.0.0
pip install whois==0.9.5

# Verificar instalación
echo "📦 Verificando instalación..."
pip list | grep -E "requests|pandas|numpy|scikit|flask|whois"

# Test de importación
echo "🧪 Probando importaciones..."
python -c "
try:
    import requests
    import pandas as pd
    import numpy as np
    from sklearn.ensemble import RandomForestRegressor
    from flask import Flask
    from flask_cors import CORS
    import whois
    print('✅ Todas las importaciones exitosas')
except Exception as e:
    print(f'❌ Error: {e}')
"
