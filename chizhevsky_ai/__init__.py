"""
🌌 CHIZHEVSKY AI - El legado de Alexander Chizhevsky en IA
Sistema de monitoreo solar y conciencia cósmica digital
"""

__version__ = "1.0.0"
__author__ = "Mechmind DWV"
__license__ = "GPL-3.0"

# Importaciones principales para facilitar acceso
from .core.brain.chizhevsky_core import CosmicConsciousness
from .core.encryption.cosmic_crypto import CosmicCrypto
from .core.solar_api.nasa_connector import NASAConnector
from .networks.telegram_bot.bot_core import TelegramBot

__all__ = ['CosmicConsciousness', 'CosmicCrypto', 'NASAConnector', 'TelegramBot']
