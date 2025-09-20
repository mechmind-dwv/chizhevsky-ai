#!/bin/bash
echo "🔍 Verificación completa del Sistema Chizhevsky AI"
echo "================================================"

# 1. Verificar servicio
echo "1. 📋 Estado del servicio:"
sudo systemctl status chizhevsky.service --no-pager -l | head -10

# 2. Verificar conectividad
echo ""
echo "2. 🌐 Conectividad con NOAA:"
python3 -c "
import requests
endpoints = {
    'planetary_k_index': 'https://services.swpc.noaa.gov/json/planetary_k_index_1m.json',
    'alerts': 'https://services.swpc.noaa.gov/products/alerts.json'
}

for name, url in endpoints.items():
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Chizhevsky-AI-Test'})
        status = '✅ OK' if response.status_code == 200 else f'❌ Error {response.status_code}'
        print(f'   {name}: {status}')
        if response.status_code == 200:
            data = response.json()
            record_count = len(data) if isinstance(data, list) else 'dict'
            print(f'      Registros: {record_count}')
    except Exception as e:
        print(f'   {name}: ❌ Error - {str(e)[:50]}')
"

# 3. Verificar datos obtenidos
echo ""
echo "3. 📊 Prueba de obtención de datos:"
python3 -c "
from noaa_fix import NOAADataFetcher
fetcher = NOAADataFetcher()
datos = fetcher.obtener_datos_solares()
print(f'   Fuente: {datos[\"fuente\"]}')
print(f'   Kp index: {datos[\"indice_kp\"]}')
print(f'   Riesgo solar: {datos[\"riesgo_solar\"]}%')
print(f'   Alertas activas: {datos[\"alertas_activas\"]}')
"

# 4. Verificar base de datos
echo ""
echo "4. 🗄️ Estado de la base de datos:"
if [ -f "chizhevsky_alerts.db" ]; then
    sqlite3 chizhevsky_alerts.db "SELECT COUNT(*) as total, MAX(timestamp) as ultimo, fuente FROM datos_solares GROUP BY fuente;"
else
    echo "❌ Base de datos no encontrada en ubicación esperada"
    echo "💡 Buscando en otras ubicaciones..."
    find . -name "*.db" -o -name "*.sqlite" 2>/dev/null || echo "⚠️  No se encontraron bases de datos"
fi

# 5. Verificar logs recientes
echo ""
echo "5. 📝 Logs recientes:"
sudo journalctl -u chizhevsky.service -n 5 --no-pager --no-hostname
