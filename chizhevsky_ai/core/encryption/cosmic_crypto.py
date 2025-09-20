"""
🔒 Cifrado cósmico basado en teorías de Chizhevsky
Sistema de encriptación inspirado en ciclos solares
"""
import base64
import hashlib
from datetime import datetime

class CosmicCrypto:
    def __init__(self):
        self.solar_cycle = 11  # años del ciclo solar
    
    def generate_cosmic_key(self):
        """Generar clave basada en ciclo solar actual"""
        current_year = datetime.now().year
        cycle_position = current_year % self.solar_cycle
        base_key = f"CHIZHEVSKY_{cycle_position}"
        return hashlib.sha256(base_key.encode()).hexdigest()
    
    def encrypt(self, message):
        """Encriptar mensaje usando cifrado cósmico"""
        key = self.generate_cosmic_key()
        # Simulación simple de encriptación
        encoded = base64.b64encode(message.encode()).decode()
        return f"🌌{encoded}🔭"
    
    def decrypt(self, encrypted_message):
        """Desencriptar mensaje"""
        if encrypted_message.startswith('🌌') and encrypted_message.endswith('🔭'):
            encoded = encrypted_message[1:-1]
            return base64.b64decode(encoded).decode()
        return encrypted_message

# Ejemplo de uso
if __name__ == "__main__":
    crypto = CosmicCrypto()
    msg = "Alexander Chizhevsky"
    enc = crypto.encrypt(msg)
    dec = crypto.decrypt(enc)
    print("Original:", msg)
    print("Encriptado:", enc)
    print("Desencriptado:", dec)
    print("Clave cósmica:", crypto.generate_cosmic_key()[:20] + "...")
