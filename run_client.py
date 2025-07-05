#!/usr/bin/env python3
"""
Script para executar o cliente Napster
"""

from cliente import NapsterClient

if __name__ == "__main__":
    print("=== Cliente Napster ===")
    print("Conectando ao servidor...")
    
    client = NapsterClient()
    try:
        client.start()
    except KeyboardInterrupt:
        print("\nDesconectando...")
        client.disconnect()
