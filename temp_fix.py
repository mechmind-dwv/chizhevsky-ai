    def get_spaceweather_data(self):
        """Obtener datos de Space Weather API desde endpoints funcionales"""
        try:
            # Usar el nuevo fetcher
            from noaa_fix import obtener_datos_noaa_actualizados
            datos = obtener_datos_noaa_actualizados()
            
            # Adaptar al formato esperado por el sistema
            return {
                'llamaradas_m': datos['llamaradas_m'],
                'llamaradas_x': datos['llamaradas_x'],
                'indice_kp': datos['indice_kp'],
                'viento_velocidad': datos['velocidad_viento_solar'],
                'viento_densidad': datos['densidad_viento_solar'],
                'protones_10mev': datos['protones_10mev'],
                'protones_100mev': datos['protones_100mev'],
                'riesgo': datos['riesgo_solar'] / 100.0,  # Convertir de porcentaje a decimal
                'fuente': datos['fuente']
            }
                
        except Exception as e:
            logger.error(f"Error obteniendo datos: {e}")
            return self.get_fallback_data()
