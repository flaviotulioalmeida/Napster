#!/usr/bin/env python3
"""
Script de teste para verificar o funcionamento do sistema
"""

import os
import time
import subprocess
import threading

def create_test_files():
    """Cria arquivos de teste"""
    test_files = [
        ("public/teste1.txt", "Conteúdo do arquivo de teste 1"),
        ("public/musica_teste.mp3", "Dados simulados de MP3 para teste"),
        ("public/documento_teste.pdf", "Dados simulados de PDF para teste"),
        ("public/imagem_teste.jpg", "Dados simulados de imagem para teste")
    ]
    
    os.makedirs("public", exist_ok=True)
    
    for filename, content in test_files:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Arquivo de teste criado: {filename}")

def test_protocol():
    """Testa o protocolo básico"""
    import socket
    
    print("Testando conexão com servidor...")
    
    try:
        # Testar conexão com servidor
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 1234))
        
        # Testar comando JOIN
        client.send(b"JOIN 127.0.0.1")
        response = client.recv(1024).decode('utf-8')
        print(f"Resposta JOIN: {response}")
        
        # Testar comando SEARCH
        client.send(b"SEARCH teste")
        response = client.recv(1024).decode('utf-8')
        print(f"Resposta SEARCH: {response}")
        
        # Testar comando LEAVE
        client.send(b"LEAVE")
        response = client.recv(1024).decode('utf-8')
        print(f"Resposta LEAVE: {response}")
        
        client.close()
        print("Teste de protocolo concluído com sucesso!")
        
    except Exception as e:
        print(f"Erro no teste: {e}")

if __name__ == "__main__":
    print("=== Teste do Sistema Napster ===")
    
    # Criar arquivos de teste
    create_test_files()
    
    print("\nPara testar completamente:")
    print("1. Execute: python run_server.py")
    print("2. Execute: python run_client.py (em outro terminal)")
    print("3. Execute: python test_system.py (para testar protocolo)")
    
    # Testar protocolo se servidor estiver rodando
    try:
        test_protocol()
    except:
        print("\nServidor não está rodando. Execute run_server.py primeiro.")
