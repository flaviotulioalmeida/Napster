import os

# Criar estruturas de diretórios necessárias
directories = [
    "public",
    "downloads"
]

for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Diretório '{directory}' criado.")
    else:
        print(f"Diretório '{directory}' já existe.")

# Criar alguns arquivos de exemplo na pasta public
example_files = [
    ("public/exemplo1.txt", "Este é um arquivo de exemplo 1."),
    ("public/exemplo2.txt", "Este é um arquivo de exemplo 2 com mais conteúdo."),
    ("public/musica.mp3", "Dados simulados de um arquivo MP3..."),
    ("public/documento.pdf", "Dados simulados de um arquivo PDF...")
]

for filename, content in example_files:
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Arquivo '{filename}' criado.")
    else:
        print(f"Arquivo '{filename}' já existe.")

print("Setup concluído!")
