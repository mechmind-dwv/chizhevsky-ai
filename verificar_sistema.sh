#!/bin/bash
echo "🔍 Verificando el sistema Chizhevsky AI..."
echo "📋 Estado del servicio:"
sudo systemctl status chizhevsky.service --no-pager -l

echo ""
echo "🌐 Probando conectividad con NOAA..."
python -c "
import requests
try:
    response = requests.get('https://services.swpc.noaa.gov/products/alerts.json', timeout=10)
    print('✅ Conexión a alerts.json: OK' if response.status_code == 200 else '❌ Error en alerts.json')
    
    response = requests.get('https://services.swpc.noaa.gov/json/planetary_k_index_1m.json', timeout=10)
    print('✅ Conexión a planetary_k_index: OK' if response.status_code == 200 else '❌ Error en planetary_k_index')
    
except Exception as e:
    print(f'❌ Error de conexión: {e}')
"

echo ""
echo "📊 Probando obtención de datos..."
python -c "
from parche_noaa_fix import obtener_datos_noaa
datos = obtener_datos_noaa()
print(f'✅ Datos obtenidos: {len(datos)} campos')
print(f'   Último Kp: {datos.get(\"indice_kp\", \"N/A\")}')
print(f'   Riesgo solar: {datos.get(\"riesgo_solar\", \"N/A\")}%')
"

echo ""
echo "📝 Logs recientes del servicio:"
sudo journalctl -u chizhevsky.service -n 10 --no-pager
