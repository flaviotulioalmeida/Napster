#!/usr/bin/env python3
"""
Script para executar o servidor Napster
"""

from servidor import NapsterServer

if __name__ == "__main__":
    print("=== Servidor Napster ===")
    print("Iniciando servidor na porta 1234...")
    print("Pressione Ctrl+C para parar o servidor")
    
    server = NapsterServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nParando servidor...")
        server.stop()
        print("Servidor parado.")
