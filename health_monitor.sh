#!/bin/bash
echo "🔬 MONITOR DE SALUD CHIZHEVSKY - TIEMPO REAL"
echo "==========================================="

while true; do
    echo ""
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Leyendo métricas..."
    
    # Obtener datos y parsear con Python para mayor robustez
    METRICS=$(curl -s http://localhost:27779/cosmic-api/hospital/metrics)
    HEALTH=$(curl -s http://localhost:27779/cosmic-api/health-status)
    
    # Usar Python para extraer valores (más robusto que grep)
    SOLAR=$(python3 -c "import json, sys; data=json.loads('$HEALTH'); print(data.get('solar_activity', 0))")
    EMERGENCY=$(python3 -c "import json, sys; data=json.loads('$HEALTH'); print(data.get('emergency_level', 'UNKNOWN'))")
    BEDS=$(python3 -c "import json, sys; data=json.loads('$METRICS'); print(data.get('bed_occupancy', 0))")
    CRITICAL=$(python3 -c "import json, sys; data=json.loads('$METRICS'); print(data.get('critical_cases', 0))")
    
    echo "🌞 Actividad solar: $SOLAR"
    echo "🚨 Nivel emergencia: $EMERGENCY"
    echo "🏥 Ocupación camas: $BEDS%"
    echo "💔 Casos críticos: $CRITICAL"
    
    # Alertas basadas en umbrales (usando awk para comparaciones decimales)
    if (( $(echo "$SOLAR > 7.0" | awk '{print ($1 > $2)}') )); then
        echo "⚠️  ALERTA: Alta actividad solar detectada!"
        echo "   📈 Esperados $((SOLAR * 8)) casos de emergencia"
        echo "   🩸 Necesarios $((SOLAR * 15 + 80)) unidades de sangre"
    fi
    
    if (( $(echo "$BEDS > 85.0" | awk '{print ($1 > $2)}') )); then
        echo "⚠️  ALERTA: Alta ocupación hospitalaria!"
    fi
    
    if (( $(echo "$SOLAR > 7.0" | awk '{print ($1 > $2)}') )) && (( $(echo "$BEDS > 80.0" | awk '{print ($1 > $2)}') )); then
        echo "🚨🚨 DOBLE ALERTA: Actividad solar alta + ocupación elevada"
        echo "   🚑 Activar protocolos de emergencia"
        echo "   📞 Notificar personal adicional"
    fi
    
    sleep 30
done
