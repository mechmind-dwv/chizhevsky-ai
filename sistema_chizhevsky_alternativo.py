#!/usr/bin/env python3
"""
🌌 SISTEMA CHIZHEVSKY ALTERNATIVO - Puerto 17357
"""
import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurar puerto alternativo
ALTERNATIVE_PORT = 17357
os.environ['FLASK_PORT'] = str(ALTERNATIVE_PORT)

# Importar el sistema principal
from sistema_chizhevsky_final import SistemaChizhevskyFinal

if __name__ == "__main__":
    logger.info(f"🚀 Iniciando sistema alternativo en puerto {ALTERNATIVE_PORT}")
    sistema = SistemaChizhevskyFinal()
    sistema.run()
