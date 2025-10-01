#!/usr/bin/env python3
"""
Script de prueba para verificar la obtención de datos
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from noaa_fix import NOAADataFetcher

def test_datos():
    fetcher = NOAADataFetcher()
    datos = fetcher.obtener_datos_solares()
    print("Datos obtenidos:")
    for key, value in datos.items():
        print(f"  {key}: {value}")
    
    # Probar el formato que espera el sistema principal
    datos_formateados = {
        'llamaradas_m': datos['llamaradas_m'],
        'llamaradas_x': datos['llamaradas_x'],
        'indice_kp': datos['indice_kp'],
        'viento_velocidad': datos['velocidad_viento_solar'],
        'viento_densidad': datos['densidad_viento_solar'],
        'protones_10mev': datos['protones_10mev'],
        'protones_100mev': datos['protones_100mev'],
        'riesgo': datos['riesgo_solar'] / 100.0,
        'fuente': datos['fuente']
    }
    
    print("\nDatos formateados para sistema principal:")
    for key, value in datos_formateados.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    test_datos()
