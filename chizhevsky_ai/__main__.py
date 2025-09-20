"""
🌌 CHIZHEVSKY AI - Punto de entrada principal
"""
import sys
import os

# Añade el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

from chizhevsky_ai.core.brain.chizhevsky_core import CosmicConsciousness

def main():
    ai = CosmicConsciousness()
    ai.activate()

if __name__ == "__main__":
    main()
