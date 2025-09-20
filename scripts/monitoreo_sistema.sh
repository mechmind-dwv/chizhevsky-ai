#!/bin/bash
# 📊 SCRIPT DE MONITOREO DEL SISTEMA CHIZHEVSKY

echo "🔍 MONITOREO DEL SISTEMA CHIZHEVSKY AI"
echo "🕒 $(date)"
echo "========================================"

# Verificar servicio
echo "📦 Estado del servicio:"
sudo systemctl status chizhevsky-ai.service --no-pager -l

echo ""
echo "📊 Base de datos:"
sqlite3 chizhevsky_alerts.db "SELECT COUNT(*) as 'Total datos' FROM datos_solares;"
sqlite3 chizhevsky_alerts.db "SELECT COUNT(*) as 'Alertas' FROM alertas;"
sqlite3 chizhevsky_alerts.db "SELECT MAX(timestamp) as 'Último registro' FROM datos_solares;"

echo ""
echo "🌌 Últimas alertas:"
sqlite3 chizhevsky_alerts.db "SELECT timestamp, nivel, mensaje FROM alertas ORDER BY timestamp DESC LIMIT 3;"

echo ""
echo "📈 Estadísticas de riesgo:"
sqlite3 chizhevsky_alerts.db "SELECT AVG(riesgo_solar) as 'Riesgo promedio', MAX(riesgo_solar) as 'Riesgo máximo' FROM datos_solares WHERE timestamp > datetime('now', '-1 day');"

echo ""
echo "========================================"
echo "✅ Monitoreo completado"
