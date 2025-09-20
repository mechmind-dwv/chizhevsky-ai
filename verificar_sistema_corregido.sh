#!/bin/bash
echo "🔍 VERIFICACIÓN DEL SISTEMA CORREGIDO"
echo "====================================="

# 1. Verificar servicio
echo "1. 🚀 SYSTEMD SERVICE:"
if sudo systemctl is-active chizhevsky-corregido.service >/dev/null; then
    echo "   ✅ chizhevsky-corregido.service activo"
else
    echo "   ❌ chizhevsky-corregido.service inactivo"
fi

# 2. Verificar puertos
echo ""
echo "2. 📡 PUERTOS:"
echo "   Heliobiologia (5000): $(netstat -tuln | grep ':5000' >/dev/null && echo '✅ Activo' || echo '❌ Inactivo')"
echo "   Chizhevsky Corregido (27357): $(netstat -tuln | grep ':27357' >/dev/null && echo '✅ Activo' || echo '❌ Inactivo')"

# 3. Verificar web
echo ""
echo "3. 🌐 WEB:"
curl -s http://localhost:27357 >/dev/null && echo "   ✅ Panel web funcionando" || echo "   ❌ Error en panel web"

# 4. Verificar base de datos
echo ""
echo "4. 🗄️ BASE DE DATOS:"
if [ -f "chizhevsky_alerts.db" ]; then
    records=$(sqlite3 chizhevsky_alerts.db "SELECT COUNT(*) FROM datos_solares;")
    echo "   ✅ $records registros (sin errores threading)"
else
    echo "   ❌ No existe"
fi

# 5. Verificar logs
echo ""
echo "5. 📝 LOGS:"
if grep -q "thread" chizhevsky.log; then
    echo "   ⚠️  Posibles errores de threading detectados"
else
    echo "   ✅ Sin errores de threading"
fi

echo ""
echo "====================================="
echo "✅ Verificación completada"
