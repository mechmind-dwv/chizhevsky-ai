#!/bin/bash
echo "🔍 VERIFICACIÓN DEL SISTEMA CHIZHEVSKY"
echo "======================================"

# 1. Verificar servicio
echo "1. 🚀 ESTADO DEL SERVICIO:"
if sudo systemctl is-active chizhevsky-final.service >/dev/null; then
    echo "   ✅ Servicio activo"
else
    echo "   ❌ Servicio inactivo"
fi

# 2. Verificar puertos
echo ""
echo "2. 📡 PUERTOS:"
echo "   Flask (7357): $(netstat -tuln | grep ':7357' >/dev/null && echo '✅ Activo' || echo '❌ Inactivo')"
echo "   Heliobiologia (5000): $(netstat -tuln | grep ':5000' >/dev/null && echo '✅ Activo' || echo '❌ Inactivo')"

# 3. Verificar base de datos
echo ""
echo "3. 🗄️ BASE DE DATOS:"
if [ -f "chizhevsky_alerts.db" ]; then
    records=$(sqlite3 chizhevsky_alerts.db "SELECT COUNT(*) FROM datos_solares;")
    echo "   ✅ $records registros"
else
    echo "   ❌ No existe"
fi

# 4. Verificar APIs
echo ""
echo "4. 🌐 CONEXIÓN APIs:"
curl -s https://services.swpc.noaa.gov/json/solar_summary.json >/dev/null \
    && echo "   ✅ NOAA Space Weather API" || echo "   ❌ NOAA API offline"

echo ""
echo "======================================"
echo "✅ Verificación completada"
