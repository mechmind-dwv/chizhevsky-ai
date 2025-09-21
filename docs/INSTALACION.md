# 🚀 Guía de Instalación - Sistema Chizhevsky AI

## Prerrequisitos
- Python 3.8+
- git
- Cuentas en: NASA API, NOAA API, Telegram Bot

## Instalación Paso a Paso

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/mechmind-dwv/chizhevsky-ai.git
   cd chizhevsky-ai
   ```

2. **Configurar entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno**
   ```bash
   cp config/.env.example .env
   # Editar .env con tus API keys reales
   nano .env
   ```

4. **Iniciar el sistema**
   ```bash
   python sistema_chizhevsky_completo_corregido.py
   ```

5. **Verificar instalación**
   ```bash
   ./scripts/verificar_sistema_completo.sh
   ```
