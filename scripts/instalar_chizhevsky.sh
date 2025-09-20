#!/bin/bash
echo "🚀 INSTALANDO SISTEMA CHIZHEVSKY AI COMPLETO"
echo "============================================"

# Verificar Python
echo "🐍 Verificando Python..."
python --version

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install cryptography requests python-telegram-bot flask python-dotenv numpy

# Verificar instalación
echo "✅ Verificando instalación..."
python -c "
import cryptography, requests, telegram, flask, dotenv, numpy
print('✓ Cryptography:', cryptography.__version__)
print('✓ Requests:', requests.__version__)  
print('✓ Telegram bot:', telegram.__version__)
print('✓ Flask:', flask.__version__)
print('✓ Dotenv:', dotenv.__version__)
print('✓ Numpy:', numpy.__version__)
"

# Configurar entorno
echo "⚙️ Configurando entorno..."
if [ ! -f .env ]; then
    cat > .env << 'ENV'
TELEGRAM_BOT_TOKEN=8374151628:AAFLsjzpc4N30HoJRMxs3d4LvYQPhziotvU
TELEGRAM_CHAT_ID=8350588401
NASA_API_KEY=DEMO_KEY
DATA_GOV_API_KEY=EBScmUckSBriKewtpC9Oba1HIXNguUU7PqLOv3cv
ENV
    echo "✅ Archivo .env creado"
else
    echo "✓ Archivo .env ya existe"
fi

# Verificar estructura
echo "🏗️ Verificando estructura..."
if [ -d "chizhevsky_ai" ]; then
    echo "✓ Estructura de paquete correcta"
    find chizhevsky_ai -name "*.py" | head -5
else
    echo "❌ Error: No se encuentra chizhevsky_ai/"
    exit 1
fi

echo ""
echo "🎉 INSTALACIÓN COMPLETADA"
echo "Ejecuta: python -m chizhevsky_ai"
