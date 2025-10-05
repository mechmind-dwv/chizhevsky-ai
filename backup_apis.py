BACKUP_APIS = {
    'spaceweather_live': 'https://www.spaceweatherlive.com/en/scripts/json/activity-data.php',
    'iswa_ccmc': 'https://iswa.ccmc.gsfc.nasa.gov/IswaSystemWebApp/',
    'esa_spaceweather': 'https://swe.ssa.esa.int/'
}

print("APIs de respaldo configuradas:")
for nombre, url in BACKUP_APIS.items():
    print(f" - {nombre}: {url}")
