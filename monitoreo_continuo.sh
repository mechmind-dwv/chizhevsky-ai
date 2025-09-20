#!/bin/bash
echo "🔭 Monitorización continua del Sistema Chizhevsky AI"
echo "Presiona Ctrl+C para detener"
echo ""

while true; do
    echo "=== $(date) ==="
    # Verificar estado del servicio
    if systemctl is-active --quiet chizhevsky.service; then
        echo "✅ Servicio activo"
        
        # Verificar última entrada en la base de datos
        ultimo_dato=$(sqlite3 chizhevsky_alerts.db "SELECT timestamp, fuente, indice_kp, riesgo_solar FROM datos_solares ORDER BY id DESC LIMIT 1")
        echo "📊 Último dato: $ultimo_dato"
        
        # Verificar conectividad rápida
        if curl -s --head https://services.swpc.noaa.gov/products/alerts.json | head -1 | grep -q "200"; then
            echo "🌐 Conexión NOAA: ✅"
        else
            echo "🌐 Conexión NOAA: ❌"
        fi
        
    else
        echo "❌ Servicio inactivo"
    fi
    
    echo ""
    sleep 60  # Verificar cada minuto
done
