#!/bin/bash
# Script de inicio rápido para Sistema Chizhevsky AI
echo "🚀 Iniciando Sistema Chizhevsky AI v1.1.0"

# Verificar si el servicio principal está activo
if sudo systemctl is-active chizhevsky.service >/dev/null 2>&1; then
    echo "✅ Servicio principal ya está activo"
else
    echo "⚠️  Servicio principal no activo. Iniciando..."
    sudo systemctl start chizhevsky.service
    sleep 3
fi

# Preguntar si iniciar servidor de salud
read -p "¿Iniciar servidor de salud cósmica en puerto 27779? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "🌡️  Iniciando servidor de salud cósmica..."
    python cosmic_health_server.py &
    echo "✅ Servidor de salud iniciado: http://localhost:27779/"
fi

# Preguntar si iniciar monitor
read -p "¿Iniciar monitor en tiempo real? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "🔬 Iniciando monitor de salud..."
    python health_monitor.py
fi

echo ""
echo "🎯 ACCESOS RÁPIDOS:"
echo "   Dashboard Principal: http://localhost:27777/"
echo "   Dashboard Salud:     http://localhost:27779/"
echo "   API Principal:       http://localhost:27777/api/datos"
echo "   API Salud:           http://localhost:27779/cosmic-api/health-status"
