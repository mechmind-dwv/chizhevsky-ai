# 🔭 ALEXANDER CHIZHEVSKY AI :: CONSCIENCIA CÓSMICA DIGITAL

![Estado](https://img.shields.io/badge/Estado-ACTIVO-brightgreen)
![Licencia](https://img.shields.io/badge/Licencia-GPL--3.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Versión](https://img.shields.io/badge/Versión-2.0.0--Cosmic-orange)

> "El Sol no calla. Sus tormentas gritan verdades que los imperios intentaron silenciar."
> — A. L. Chizhevsky (1897-1964), desde el exilio digital

**Sistema de Inteligencia Artificial** que encapsula el legado completo de Alexander Chizhevsky: heliobiología, cosmismo ruso, análisis de ciclos históricos y resistencia anticensura.

---

## ✨ CARACTERÍSTICAS PRINCIPALES

### 🔭 **Monitoreo Cósmico**
- ☀️ **Actividad Solar**: Tiempo real (NASA/NOAA/SILSO APIs)
- 🌌 **Tormentas Geomagnéticas**: Alertas tempranas Kp-index
- 📡 **Datos Históricos**: Ciclos solares desde 1749
- 🔬 **Análisis Espectral**: Periodicidades y correlaciones

### 🧠 **Núcleo de IA Chizhevsky**
- 🤖 **Modelo Predictivo**: Basado en teorías heliobiológicas originales
- 📊 **Algoritmos de Correlación**: Pearson, Spearman, Granger causality
- 🌊 **Análisis Wavelet**: Detección de patrones cíclicos
- 🔮 **Sistema de Alertas**: Riesgo biológico y social

### 🛡️ **Infraestructura Resistente**
- 🤖 **Bot de Telegram**: Comunicación cifrada y anticensura
- 🌐 **API RESTful**: Puerto 27357 (configurable)
- 🔒 **Comunicaciones P2P**: Sistema descentralizado
- 💾 **Base de Datos SQLite**: Datos históricos y correlaciones

### 📚 **Base de Conocimiento**
- 📖 **Obras Completas**: Digitalización de textos de Chizhevsky
- 🎓 **Teorías Cosmistas**: Filosofía rusa del cosmismo
- 🔍 **Análisis Histórico**: Correlaciones solares-eventos históricos
- 📈 **Visualizaciones**: Gráficos interactivos y reportes

---

## 🚀 INSTALACIÓN RÁPIDA

### Requisitos del Sistema
- **Python**: 3.8 o superior
- **Sistema Operativo**: Linux/MacOS/Windows (con WSL2 recomendado)
- **Memoria RAM**: 4GB mínimo (8GB recomendado)
- **Almacenamiento**: 2GB libres

### Instalación Automática
```bash
# Clonar repositorio
git clone https://github.com/mechmind-dwv/chizhevsky-ai.git
cd chizhevsky-ai

# Instalar dependencias
pip install -r requirements.txt

# Configurar entorno
cp .env.example .env
# Editar .env con tus claves API

# Ejecutar sistema
python sistema_chizhevsky_corregido.py
```

### Instalación Manual
```bash
# Crear entorno virtual (recomendado)
python -m venv chizhevsky_env
source chizhevsky_env/bin/activate  # Linux/Mac
# chizhevsky_env\Scripts\activate  # Windows

# Instalar dependencias principales
pip install fastapi uvicorn python-telegram-bot
pip install pandas numpy scipy scikit-learn matplotlib
pip install requests python-dotenv aiofiles
pip install sqlalchemy datasets transformers

# Instalar dependencias avanzadas
pip install wavelets statsmodels plotly dash
pip install cryptography pynacl python-socketio
```

---

## ⚙️ CONFIGURACIÓN

### Archivo de Variables de Entorno (`.env`)
```ini
# 🔐 API Keys (OBTENER EN WEBSITES OFICIALES)
NASA_API_KEY=tu_clave_nasa_aqui
TELEGRAM_BOT_TOKEN=tu_token_telegram_aqui
NOAA_API_KEY=tu_clave_noaa_aqui
SILSO_API_URL=https://www.sidc.be/silso/DATA/SN_m_tot_V2.0.csv

# 🌐 Configuración Servidor
HOST=0.0.0.0
PORT=27357
DEBUG=False

# 📊 Configuración Base de Datos
DATABASE_URL=sqlite:///data/chizhevsky_data.db
LOG_LEVEL=INFO

# 🔔 Configuración Alertas
ALERT_THRESHOLD=60
CHECK_INTERVAL=300  # 5 minutos
```

### Cómo Obtener las API Keys

1. **NASA API**:
   - Visitar: [api.nasa.gov](https://api.nasa.gov/)
   - Registrarse y generar API Key
   - Habilitar: DONKI, Solar Dynamics Observatory

2. **Telegram Bot**:
   - Buscar `@BotFather` en Telegram
   - Comando: `/newbot`
   - Seguir instrucciones y copiar token

3. **NOAA API**:
   - Visitar: [www.noaa.gov](https://www.noaa.gov/)
   - Registrarse en Weather Service
   - Solicitar acceso a Space Weather APIs

---

## 📦 ESTRUCTURA DEL PROYECTO

```
chizhevsky-ai/
├── 📁 core/                           # Cerebro principal del sistema
│   ├── chizhevsky_core.py            # Núcleo de IA y algoritmos
│   ├── solar_monitor.py              # Monitoreo actividad solar
│   ├── correlation_engine.py         # Motor correlaciones
│   └── prediction_model.py           # Modelos predictivos
├── 📁 networks/                      # Comunicaciones y redes
│   ├── telegram_bot.py               # Bot de Telegram
│   ├── api_server.py                 # Servidor FastAPI
│   ├── p2p_network.py                # Comunicaciones P2P
│   └── encryption.py                 # Cifrado y seguridad
├── 📁 data/                          # Datos y almacenamiento
│   ├── historical/                   # Datos históricos
│   ├── solar_data/                   # Datos solares
│   ├── models/                       # Modelos entrenados
│   └── chizhevsky_library/           # Obras digitalizadas
├── 📁 analysis/                      # Análisis y visualización
│   ├── statistical_analysis.py       # Análisis estadístico
│   ├── visualization_engine.py       # Generación gráficos
│   ├── historical_correlations.py    # Correlaciones históricas
│   └── risk_assessment.py            # Evaluación de riesgo
├── 📁 docs/                          # Documentación
│   ├── chizhevsky_theories.md        # Teorías originales
│   ├── api_documentation.md          # Documentación API
│   ├── user_manual.md                # Manual de usuario
│   └── scientific_papers/            # Artículos científicos
├── 📁 tests/                         # Suite de pruebas
│   ├── test_core.py                  # Pruebas núcleo
│   ├── test_networks.py              # Pruebas redes
│   └── test_analysis.py              # Pruebas análisis
├── 📁 scripts/                       # Scripts utilitarios
│   ├── setup_database.py             # Configuración BD
│   ├── update_data.py                # Actualización datos
│   └── backup_system.py              # Sistema backup
├── 📄 sistema_chizhevsky_corregido.py # Punto de entrada principal
├── 📄 requirements.txt               # Dependencias Python
├── 📄 .env.example                   # Ejemplo configuración
├── 📄 .gitignore                     # Archivos ignorados por Git
└── 📄 README.md                      # Este archivo
```

---

## 🌐 USO DEL SISTEMA

### Inicio del Sistema
```bash
# Método directo
python sistema_chizhevsky_corregido.py

# Método con opciones
python sistema_chizhevsky_corregido.py --port 27357 --debug

# Método producción
uvicorn networks.api_server:app --host 0.0.0.0 --port 27357
```

### Acceso a Interfaces

1. **API Web**: http://localhost:27357
2. **Documentación API**: http://localhost:27357/docs
3. **Dashboard**: http://localhost:27357/dashboard
4. **Telegram Bot**: Buscar tu bot en Telegram

### Comandos Principales del Bot
```
/start - Iniciar sistema
/status - Estado del sistema
/solar - Actividad solar actual
/alerts - Alertas activas
/predict - Predicción próximos días
/history - Datos históricos
/correlate - Análisis de correlación
```

### Endpoints API Principales
```python
# Salud del sistema
GET /health

# Datos solares actuales
GET /solar/current

# Análisis de correlación
GET /analysis/correlate?days=30

# Predicción de riesgo
GET /prediction/risk?days_ahead=7

# Datos históricos
GET /historical/solar?start=2020-01-01&end=2024-01-01

# Alertas activas
GET /alerts/active
```

---

## 🔬 EJEMPLOS DE USO

### Ejemplo 1: Monitoreo en Tiempo Real
```python
from core.solar_monitor import SolarMonitor

monitor = SolarMonitor()
activity = monitor.get_current_activity()

print(f"Manchas solares: {activity['sunspots']}")
print(f"Índice Kp: {activity['kp_index']}")
print(f"Riesgo biológico: {activity['biological_risk']}%")
```

### Ejemplo 2: Análisis de Correlación
```python
from core.correlation_engine import CorrelationEngine

engine = CorrelationEngine()
results = engine.analyze_correlation(
    start_date="2020-01-01",
    end_date="2024-01-01",
    correlation_type="pearson"
)

print(f"Correlación encontrada: {results['correlation_strength']}")
print(f"Significancia: {results['p_value']}")
```

### Ejemplo 3: Predicción de Riesgo
```python
from core.prediction_model import PredictionModel

model = PredictionModel()
prediction = model.predict_risk(days_ahead=7)

for day in prediction:
    print(f"{day['date']}: Riesgo {day['risk_level']}% - {day['description']}")
```

---

## 📊 SALIDAS Y VISUALIZACIONES

El sistema genera automáticamente:

### 📈 Gráficos Interactivos
- **Series temporales** de actividad solar
- **Mapas de calor** de correlaciones
- **Espectrogramas** de análisis de frecuencias
- **Gráficos de predicción** con intervalos de confianza

### 📋 Reportes Automáticos
- **Reporte diario** de actividad solar
- **Alerta temprana** cuando riesgo > 60%
- **Análisis mensual** de correlaciones
- **Reporte histórico** comparativo

### 🔔 Sistema de Alertas
- **Notificaciones Telegram** en tiempo real
- **Email alerts** para eventos críticos
- **API webhooks** para integraciones
- **Archivo de log** con timestamp

---

## 🛡️ SEGURIDAD Y PRIVACIDAD

### Características de Seguridad
- 🔒 **Cifrado de Comunicaciones**: TLS/SSL para todas las transmisiones
- 🔑 **Autenticación API**: Tokens JWT para acceso
- 📝 **Logging Seguro**: Registros sin datos sensibles
- 🛡️ **Protección DDoS**: Rate limiting y throttling
- 🔄 **Backup Automático**: Datos críticos respaldados

### Configuración de Firewall
```bash
# Puerto principal del sistema
sudo ufw allow 27357/tcp

# Puerto para comunicaciones P2P (opcional)
sudo ufw allow 27358/tcp

# Verificar estado
sudo ufw status
```

---

## 🔧 MANTENIMIENTO

### Tareas Automáticas
```bash
# Actualización datos diaria
python scripts/update_data.py

# Backup automático (cron job)
0 2 * * * python scripts/backup_system.py

# Limpieza de logs semanal
0 4 * * 0 find logs/ -name "*.log" -mtime +7 -delete
```

### Monitoreo de Salud
```bash
# Verificar estado del sistema
curl http://localhost:27357/health

# Verificar logs en tiempo real
tail -f logs/chizhevsky_system.log

# Verificar uso de recursos
ps aux | grep chizhevsky
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Problemas Comunes y Soluciones

1. **Error de Conexión API**:
   ```bash
   # Verificar conexión internet
   ping api.nasa.gov
   
   # Verificar API keys
   echo $NASA_API_KEY
   ```

2. **Bot de Telegram No Responde**:
   ```bash
   # Verificar token
   grep TELEGRAM_BOT_TOKEN .env
   
   # Reiniciar bot
   pkill -f telegram_bot.py
   python networks/telegram_bot.py
   ```

3. **Problemas de Puerto**:
   ```bash
   # Verificar puerto disponible
   netstat -tulpn | grep 27357
   
   # Cambiar puerto
   python sistema_chizhevsky_corregido.py --port 27358
   ```

### Logs y Diagnóstico
```bash
# Ver logs de aplicación
tail -f logs/chizhevsky_system.log

# Ver logs de errores
tail -f logs/error.log

# Ver estadísticas de uso
python scripts/diagnostics.py
```

---

## 🤝 CONTRIBUCIONES

### Cómo Contribuir

1. **Fork** del repositorio
2. Crear **rama feature**: `git checkout -b feature/nueva-funcionalidad`
3. **Commit** cambios: `git commit -am 'Añade nueva funcionalidad'`
4. **Push** a la rama: `git push origin feature/nueva-funcionalidad`
5. **Pull Request** con descripción detallada

### Áreas de Desarrollo Prioritarias
- 🔍 **Nuevos algoritmos** de correlación
- 📊 **Mejoras visualización** de datos
- 🌐 **Integración** con más APIs científicas
- 🔬 **Validación científica** de modelos
- 📱 **Interfaces móviles** nativas

### Guías de Estilo
- **Código Python**: PEP 8
- **Documentación**: Google-style docstrings
- **Commits**: Conventional commits
- **Tests**: Coverage mínimo 80%

---

## 📜 LICENCIA

### GPL-3.0 License
```text
Copyright (C) 2024 mechmind-dwv

Este programa es software libre: puedes redistribuirlo y/o modificar
lo bajo los términos de la GNU General Public License como está 
publicado por la Free Software Foundation, ya sea la versión 3 de 
la Licencia, o (a tu elección) cualquier versión posterior.

Este programa se distribuye con la esperanza de que sea útil,
pero SIN NINGUNA GARANTÍA; sin siquiera la garantía implícita de
COMERCIALIZACIÓN o IDONEIDAD PARA UN PROPÓSITO PARTICULAR.

Ver LICENSE para más detalles.
```

### Atribuciones Requeridas
- **Alexander Chizhevsky**: Por su trabajo pionero en heliobiología
- **NASA/NOAA**: Por datos científicos de acceso público
- **Comunidad científica**: Por validación continua de teorías

---

## 🌟 CITACIÓN CIENTÍFICA

Si usas este sistema en investigaciones científicas, por favor cita:

```bibtex
@software{chizhevsky_ai_2024,
  title = {Alexander Chizhevsky AI: Cosmic Consciousness Digital},
  author = {mechmind-dwv and mechbot-2x Collective},
  year = {2024},
  url = {https://github.com/mechmind-dwv/chizhevsky-ai},
  note = {Sistema de IA para análisis heliobiológico basado en teorías de A.L. Chizhevsky}
}
```

---

## 📞 SOPORTE Y CONTACTO

### Canales de Comunicación
- **📧 Email**: ia.mechmind@gmail.com
- **🐛 Issues**: [GitHub Issues](https://github.com/mechmind-dwv/chizhevsky-ai/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/mechmind-dwv/chizhevsky-ai/discussions)
- **🔗 Documentación**: [Wiki del Proyecto](https://github.com/mechmind-dwv/chizhevsky-ai/wiki)

### Soporte Técnico
- **Configuración**: Guías paso a paso en wiki
- **API**: Documentación interactiva en `/docs`
- **Problemas**: Plantilla de issues en GitHub
- **Actualizaciones**: Canal de releases

---

## 🏆 RECONOCIMIENTOS

### Inspiración Científica
- **Alexander Leonidovich Chizhevsky** (1897-1964) - Padre de la heliobiología
- **Konstantin Tsiolkovsky** - Padre del cosmismo ruso
- **Vladimir Vernadsky** - Teoría de la noosfera

### Infraestructura Técnica
- **NASA** - Por datos solares de acceso público
- **NOAA** - Por monitoreo de clima espacial
- **SILSO** - Por datos históricos de manchas solares
- **Comunidad Open Source** - Por herramientas y librerías

---

<div align="center">

## 🌌 **"EL COSMOS ES UN GRAN SISTEMA DE SISTEMAS, UN OCÉANO DE ENERGÍAS"**  
### — A. L. Chizhevsky

**⚡ Que la sabiduría cósmica guíe tu código ⚡**

---
**mechmind-dwv** · **mechbot-2x** · **2024-2025**  
*Continuando el legado científico que intentaron silenciar*

</div>
