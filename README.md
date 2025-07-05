# 🚀 Sistema de Compartilhamento de Arquivos - Napster

Um sistema completo de compartilhamento de arquivos P2P baseado no protocolo Napster, implementado em Python usando sockets.

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Arquitetura](#-arquitetura)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Como Executar](#-como-executar)
- [Protocolo de Comunicação](#-protocolo-de-comunicação)
- [Comandos do Cliente](#-comandos-do-cliente)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Solução de Problemas](#-solução-de-problemas)
- [Limitações](#-limitações)

## 🎯 Visão Geral

Este sistema implementa um compartilhador de arquivos similar ao Napster original, onde:

- **Servidor Central**: Mantém um índice de todos os arquivos compartilhados
- **Clientes P2P**: Compartilham arquivos diretamente entre si
- **Busca Centralizada**: Pesquisa por arquivos através do servidor
- **Download Direto**: Transferência P2P sem passar pelo servidor

## 🏗️ Arquitetura

\`\`\`
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cliente A     │    │   Servidor      │    │   Cliente B     │
│   (porta 1235)  │    │   (porta 1234)  │    │   (porta 1235)  │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Compartilha   │◄──►│ • Índice de     │◄──►│ • Compartilha   │
│   arquivos      │    │   arquivos      │    │   arquivos      │
│ • Busca         │    │ • Busca         │    │ • Busca         │
│ • Download P2P  │    │ • Gerencia      │    │ • Download P2P  │
└─────────────────┘    │   usuários      │    └─────────────────┘
         │              └─────────────────┘              │
         └──────────── Download Direto P2P ──────────────┘
\`\`\`

## 📦 Requisitos

- **Python 3.7+**
- **Sistema Operacional**: Windows, Linux, macOS
- **Rede**: Conectividade TCP/IP
- **Portas**: 1234 (servidor), 1235 (clientes)

## 🔧 Instalação

### 1. Clone ou baixe o projeto

\`\`\`bash
# Se usando git
git clone <url-do-repositorio>
cd file-sharing-napster

# Ou extraia os arquivos baixados
\`\`\`

### 2. Verifique o Python

\`\`\`bash
python --version
# ou
python3 --version
\`\`\`

### 3. Execute o setup inicial

\`\`\`bash
python scripts/setup.py
\`\`\`

Este comando irá:
- Criar as pastas `public/` e `downloads/`
- Gerar arquivos de exemplo para teste
- Configurar a estrutura necessária

## 🚀 Como Executar

### Passo 1: Iniciar o Servidor

**Terminal 1:**
\`\`\`bash
python run_server.py
\`\`\`

**Saída esperada:**
\`\`\`
=== Servidor Napster ===
Iniciando servidor na porta 1234...
Pressione Ctrl+C para parar o servidor
Servidor iniciado em localhost:1234
\`\`\`

### Passo 2: Executar Cliente(s)

**Terminal 2 (Cliente 1):**
\`\`\`bash
python run_client.py
\`\`\`

**Terminal 3 (Cliente 2):**
\`\`\`bash
python run_client.py
\`\`\`

**Saída esperada do cliente:**
\`\`\`
=== Cliente Napster ===
Conectando ao servidor...
Conectado ao servidor como 192.168.1.100
Servidor de arquivos iniciado em 192.168.1.100:1235
Arquivo exemplo1.txt registrado: CONFIRMCREATEFILE exemplo1.txt
Arquivo exemplo2.txt registrado: CONFIRMCREATEFILE exemplo2.txt

=== Cliente Napster ===
Comandos disponíveis:
1. search <padrão> - Buscar arquivos
2. download <filename> <ip> - Baixar arquivo
3. list - Listar meus arquivos
4. quit - Sair

> 
\`\`\`

### Passo 3: Testar o Sistema

**Terminal 4 (Opcional - Teste):**
\`\`\`bash
python test_system.py
\`\`\`

## 📡 Protocolo de Comunicação

### Cliente → Servidor

| Comando | Formato | Descrição |
|---------|---------|-----------|
| `JOIN` | `JOIN {IP-ADDRESS}` | Entrar na rede |
| `CREATEFILE` | `CREATEFILE {FILENAME} {SIZE}` | Registrar arquivo |
| `DELETEFILE` | `DELETEFILE {FILENAME}` | Remover arquivo |
| `SEARCH` | `SEARCH {PATTERN}` | Buscar arquivos |
| `LEAVE` | `LEAVE` | Sair da rede |

### Servidor → Cliente

| Resposta | Formato | Descrição |
|----------|---------|-----------|
| `CONFIRMJOIN` | `CONFIRMJOIN` | Confirmar entrada |
| `CONFIRMCREATEFILE` | `CONFIRMCREATEFILE {FILENAME}` | Confirmar registro |
| `CONFIRMDELETEFILE` | `CONFIRMDELETEFILE {FILENAME}` | Confirmar remoção |
| `CONFIRMLEAVE` | `CONFIRMLEAVE` | Confirmar saída |
| `FILE` | `FILE {FILENAME} {IP} {SIZE}` | Resultado da busca |

### Cliente → Cliente (P2P)

| Comando | Formato | Descrição |
|---------|---------|-----------|
| `GET` | `GET {FILENAME} {OFFSET_START}-[OFFSET_END]` | Baixar arquivo |

## 💻 Comandos do Cliente

### 1. Buscar Arquivos
\`\`\`bash
> search mp3
Encontrados 2 arquivo(s):
1. musica_teste.mp3 (1024 bytes) - 192.168.1.101
2. song.mp3 (2048 bytes) - 192.168.1.102
\`\`\`

### 2. Baixar Arquivo
\`\`\`bash
> download musica_teste.mp3 192.168.1.101
Arquivo musica_teste.mp3 baixado com sucesso (1024 bytes) para downloads/musica_teste.mp3
\`\`\`

### 3. Listar Meus Arquivos
\`\`\`bash
> list
Meus arquivos públicos:
- exemplo1.txt (29 bytes)
- exemplo2.txt (45 bytes)
- musica_teste.mp3 (1024 bytes)
\`\`\`

### 4. Sair
\`\`\`bash
> quit
Desconectado: CONFIRMLEAVE
\`\`\`

## 📁 Estrutura do Projeto

\`\`\`
file-sharing-napster/
├── 📄 README.md                 # Este arquivo
├── 🐍 servidor.py              # Servidor central
├── 🐍 cliente.py               # Cliente P2P
├── 🐍 run_server.py            # Script para executar servidor
├── 🐍 run_client.py            # Script para executar cliente
├── 🐍 test_system.py           # Testes do sistema
├── 🐍 fix_encoding.py          # Correção de encoding
├── 📁 scripts/                 # Scripts auxiliares
│   └── 🐍 setup.py            # Configuração inicial
├── 📁 public/                  # Arquivos compartilhados
│   ├── 📄 exemplo1.txt
│   ├── 📄 exemplo2.txt
│   ├── 🎵 musica_teste.mp3
│   └── 📄 documento_teste.pdf
└── 📁 downloads/               # Arquivos baixados
\`\`\`

## 🎮 Exemplos de Uso

### Cenário 1: Compartilhar um arquivo

1. **Adicione arquivo à pasta public:**
\`\`\`bash
cp minha_musica.mp3 public/
\`\`\`

2. **Reinicie o cliente** para registrar o novo arquivo

3. **Outros usuários podem buscar:**
\`\`\`bash
> search musica
\`\`\`

### Cenário 2: Buscar e baixar

1. **Cliente A busca:**
\`\`\`bash
> search documento
Encontrados 1 arquivo(s):
1. relatorio.pdf (5120 bytes) - 192.168.1.102
\`\`\`

2. **Cliente A baixa:**
\`\`\`bash
> download relatorio.pdf 192.168.1.102
Arquivo relatorio.pdf baixado com sucesso para downloads/relatorio.pdf
\`\`\`

### Cenário 3: Múltiplos clientes

1. **Execute vários clientes simultaneamente**
2. **Cada um compartilha arquivos diferentes**
3. **Todos podem buscar e baixar entre si**

## 🔧 Solução de Problemas

### Problema: "Erro ao conectar ao servidor"

**Solução:**
\`\`\`bash
# Verifique se o servidor está rodando
python run_server.py

# Verifique se a porta 1234 está livre
netstat -an | grep 1234
\`\`\`

### Problema: "Erro no servidor de arquivos"

**Solução:**
\`\`\`bash
# Verifique se a porta 1235 está livre
netstat -an | grep 1235

# Execute como administrador se necessário (Windows)
# Use sudo se necessário (Linux/Mac)
\`\`\`

### Problema: "FILE NOT FOUND" no download

**Possíveis causas:**
- Arquivo não existe na pasta `public/` do cliente
- Cliente que possui o arquivo desconectou
- IP incorreto

**Solução:**
\`\`\`bash
# Verifique se o arquivo existe
ls public/

# Faça nova busca para IP atualizado
> search nome_do_arquivo
\`\`\`

### Problema: Encoding de caracteres

**Solução:**
\`\`\`bash
python fix_encoding.py
\`\`\`

### Problema: Firewall bloqueando conexões

**Windows:**
\`\`\`bash
# Execute como administrador
netsh advfirewall firewall add rule name="Napster Server" dir=in action=allow protocol=TCP localport=1234
netsh advfirewall firewall add rule name="Napster Client" dir=in action=allow protocol=TCP localport=1235
\`\`\`

**Linux:**
\`\`\`bash
sudo ufw allow 1234
sudo ufw allow 1235
\`\`\`

## ⚠️ Limitações

### Técnicas
- **Rede Local**: Funciona melhor em redes locais
- **NAT/Firewall**: Pode ter problemas com NAT e firewalls
- **Sem Autenticação**: Não há sistema de login
- **Sem Criptografia**: Transferências não são criptografadas

### Funcionais
- **Busca Simples**: Apenas busca por substring no nome
- **Sem Resumo**: Downloads não podem ser resumidos
- **Sem Verificação**: Não verifica integridade dos arquivos
- **Memória**: Servidor mantém tudo em memória

## 🧪 Testes Avançados

### Teste de Carga
\`\`\`bash
# Execute múltiplos clientes
for i in {1..5}; do
    python run_client.py &
done
\`\`\`

### Teste de Protocolo
\`\`\`bash
python test_system.py
\`\`\`

### Teste Manual
\`\`\`bash
# Terminal 1: Servidor
python run_server.py

# Terminal 2: Cliente 1
python run_client.py

# Terminal 3: Cliente 2  
python run_client.py

# No Cliente 1:
> search teste

# No Cliente 2:
> download arquivo.txt 192.168.1.100
\`\`\`

## 🔄 Fluxo Completo de Execução

### 1. Preparação
\`\`\`bash
# Passo 1: Setup inicial
python scripts/setup.py

# Passo 2: Correção de encoding (se necessário)
python fix_encoding.py

# Passo 3: Teste básico (opcional)
python test_system.py
\`\`\`

### 2. Execução
\`\`\`bash
# Terminal 1: Servidor
python run_server.py

# Terminal 2: Cliente 1
python run_client.py

# Terminal 3: Cliente 2
python run_client.py
\`\`\`

### 3. Uso
\`\`\`bash
# No Cliente 1:
> list                    # Ver meus arquivos
> search mp3             # Buscar arquivos
> download song.mp3 192.168.1.102  # Baixar arquivo

# No Cliente 2:
> search documento       # Buscar outros arquivos
> quit                   # Sair
\`\`\`

## 📞 Suporte

Se encontrar problemas:

1. **Verifique os logs** do servidor e cliente
2. **Execute os testes** com `python test_system.py`
3. **Verifique as portas** 1234 e 1235
4. **Confirme o firewall** não está bloqueando
5. **Teste em rede local** primeiro

---

**🎉 Agora você está pronto para usar o sistema de compartilhamento de arquivos Napster!**

Para começar rapidamente:
\`\`\`bash
python scripts/setup.py && python run_server.py
\`\`\`

Em outro terminal:
\`\`\`bash
python run_client.py
#   N a p s t e r  
 