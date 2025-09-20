#!/bin/bash
# 🚀 SCRIPT DE INICIO CHIZHEVSKY AI

echo "🌌 Iniciando Sistema Chizhevsky AI..."
echo "🕒 $(date)"

# Activar entorno virtual
source venv/bin/activate

# Verificar si el servicio está activo
if sudo systemctl is-active --quiet chizhevsky-ai.service; then
    echo "✅ Servicio systemd ya está activo"
else
    echo "⚠️ Iniciando servicio..."
    sudo systemctl start chizhevsky-ai.service
fi

# Iniciar panel de control
echo "🌐 Iniciando panel de control web..."
python panel_control.py &

echo "🎉 Sistema completamente operativo!"
echo "📊 Panel web: http://localhost:5000"
echo "📋 API datos: http://localhost:5000/api/datos"
echo "📝 Logs: tail -f chizhevsky.log"
