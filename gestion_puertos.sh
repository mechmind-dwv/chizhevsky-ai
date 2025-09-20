#!/bin/bash
# Script para gestionar puertos automáticamente

find_available_port() {
    local base_port=$1
    local port=$base_port
    
    while netstat -tuln | grep ":$port " > /dev/null; do
        port=$((port + 1000))
        if [ $port -gt 20000 ]; then
            port=$((30000 + RANDOM % 10000))
        fi
    done
    
    echo $port
}

# Encontrar puerto disponible
AVAILABLE_PORT=$(find_available_port 7357)
echo "🚀 Usando puerto disponible: $AVAILABLE_PORT"

# Ejecutar con puerto disponible
FLASK_PORT=$AVAILABLE_PORT python sistema_chizhevsky_final.py
