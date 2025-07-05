#!/usr/bin/env python3
"""
Script para corrigir problemas de encoding
"""

import os

def fix_file_encoding():
    """Corrige problemas de encoding nos arquivos"""
    
    # Lista de arquivos Python para verificar
    python_files = [
        'servidor.py',
        'cliente.py',
        'run_server.py',
        'run_client.py'
    ]
    
    for filename in python_files:
        if os.path.exists(filename):
            try:
                # Ler arquivo
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Adicionar encoding no topo se não existir
                if '# -*- coding: utf-8 -*-' not in content:
                    lines = content.split('\n')
                    if lines[0].startswith('#!'):
                        lines.insert(1, '# -*- coding: utf-8 -*-')
                    else:
                        lines.insert(0, '# -*- coding: utf-8 -*-')
                    
                    # Reescrever arquivo
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(lines))
                    
                    print(f"Encoding corrigido em: {filename}")
                else:
                    print(f"Encoding já correto em: {filename}")
                    
            except Exception as e:
                print(f"Erro ao corrigir {filename}: {e}")

if __name__ == "__main__":
    fix_encoding()
    print("Correção de encoding concluída!")
