import socket
import threading
import os
import time
from typing import List, Dict

class NapsterClient:
    def __init__(self, server_host='localhost', server_port=1234, client_port=1235):
        self.server_host = server_host
        self.server_port = server_port
        self.client_port = client_port
        self.my_ip = self.get_local_ip()
        self.server_socket = None
        self.file_server_socket = None
        self.public_folder = "public"
        self.downloads_folder = "downloads"
        
        # Criar pastas se não existirem
        os.makedirs(self.public_folder, exist_ok=True)
        os.makedirs(self.downloads_folder, exist_ok=True)
    
    def get_local_ip(self) -> str:
        """Obtém o IP local da máquina"""
        try:
            # Conecta a um endereço externo para descobrir o IP local
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def start(self):
        """Inicia o cliente"""
        # Conectar ao servidor
        if not self.connect_to_server():
            return
        
        # Iniciar servidor de arquivos
        self.start_file_server()
        
        # Enviar lista de arquivos
        self.send_file_list()
        
        # Interface do usuário
        self.user_interface()
    
    def start_server_listener(self):
        """Thread para escutar respostas do servidor"""
        def listen_server():
            try:
                while True:
                    response = self.server_socket.recv(4096).decode('utf-8')
                    if not response:
                        break
                    print(f"Servidor: {response}")
            except Exception as e:
                print(f"Conexão com servidor perdida: {e}")
    
        listener_thread = threading.Thread(target=listen_server)
        listener_thread.daemon = True
        listener_thread.start()
    
    def connect_to_server(self) -> bool:
        """Conecta ao servidor central"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.connect((self.server_host, self.server_port))
            
            # Enviar comando JOIN
            join_message = f"JOIN {self.my_ip}"
            self.server_socket.send(join_message.encode('utf-8'))
            
            # Aguardar confirmação
            response = self.server_socket.recv(1024).decode('utf-8')
            if response == "CONFIRMJOIN":
                print(f"Conectado ao servidor como {self.my_ip}")
                # Iniciar thread para escutar servidor
                self.start_server_listener()
                return True
            else:
                print(f"Erro ao conectar: {response}")
                return False
            
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")
        return False
    
    def start_file_server(self):
        """Inicia servidor para compartilhar arquivos"""
        def file_server():
            try:
                self.file_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.file_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.file_server_socket.bind((self.my_ip, self.client_port))
                self.file_server_socket.listen(5)
                print(f"Servidor de arquivos iniciado em {self.my_ip}:{self.client_port}")
                
                while True:
                    client_socket, client_address = self.file_server_socket.accept()
                    print(f"Solicitação de download de {client_address}")
                    
                    # Criar thread para lidar com o download
                    download_thread = threading.Thread(
                        target=self.handle_download_request,
                        args=(client_socket,)
                    )
                    download_thread.daemon = True
                    download_thread.start()
                    
            except Exception as e:
                print(f"Erro no servidor de arquivos: {e}")
        
        server_thread = threading.Thread(target=file_server)
        server_thread.daemon = True
        server_thread.start()
    
    def handle_download_request(self, client_socket: socket.socket):
        """Lida com solicitações de download"""
        try:
            request = client_socket.recv(1024).decode('utf-8').strip()
            print(f"Solicitação recebida: {request}")
            
            if request.startswith('GET'):
                parts = request.split()
                filename = parts[1]
                
                # Verificar se há offset
                offset_start = 0
                offset_end = None
                
                if len(parts) > 2:
                    offset_range = parts[2]
                    if '-' in offset_range:
                        start, end = offset_range.split('-')
                        offset_start = int(start)
                        if end:
                            offset_end = int(end)
                
                self.send_file(client_socket, filename, offset_start, offset_end)
                
        except Exception as e:
            print(f"Erro ao processar download: {e}")
        finally:
            client_socket.close()
    
    def send_file(self, client_socket: socket.socket, filename: str, 
                  offset_start: int = 0, offset_end: int = None):
        """Envia arquivo para outro cliente"""
        file_path = os.path.join(self.public_folder, filename)
        
        if not os.path.exists(file_path):
            client_socket.send(b"FILE NOT FOUND")
            return
        
        try:
            with open(file_path, 'rb') as f:
                f.seek(offset_start)
                
                if offset_end is None:
                    # Enviar arquivo inteiro a partir do offset
                    while True:
                        chunk = f.read(1024)
                        if not chunk:
                            break
                        client_socket.send(chunk)
                else:
                    # Enviar apenas o range especificado
                    bytes_to_send = offset_end - offset_start + 1
                    while bytes_to_send > 0:
                        chunk_size = min(1024, bytes_to_send)
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        client_socket.send(chunk)
                        bytes_to_send -= len(chunk)
                        
            print(f"Arquivo {filename} enviado com sucesso")
            
        except Exception as e:
            print(f"Erro ao enviar arquivo: {e}")
    
    def send_file_list(self):
        """Envia lista de arquivos públicos para o servidor"""
        if not os.path.exists(self.public_folder):
            return
        
        for filename in os.listdir(self.public_folder):
            file_path = os.path.join(self.public_folder, filename)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                message = f"CREATEFILE {filename} {size}"
                
                self.server_socket.send(message.encode('utf-8'))
                response = self.server_socket.recv(1024).decode('utf-8')
                print(f"Arquivo {filename} registrado: {response}")
    
    def search_files(self, pattern: str) -> List[Dict]:
        """Busca arquivos no servidor"""
        try:
            message = f"SEARCH {pattern}"
            self.server_socket.send(message.encode('utf-8'))
        
            # Aguardar resposta específica para busca
            response = self.server_socket.recv(4096).decode('utf-8')
        
            if response == "NO FILES FOUND":
                return []
        
            files = []
            for line in response.split('\n'):
                if line.startswith('FILE'):
                    parts = line.split(' ', 3)  # Limitar splits para lidar com nomes com espaços
                    if len(parts) >= 4:
                        files.append({
                            'filename': parts[1],
                            'ip_address': parts[2],
                            'size': int(parts[3])
                        })
        
            return files
        
        except Exception as e:
            print(f"Erro na busca: {e}")
            return []
    
    def download_file(self, filename: str, ip_address: str):
        """Baixa arquivo de outro cliente"""
        try:
            # Conectar ao cliente que possui o arquivo
            download_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            download_socket.settimeout(30)  # Timeout de 30 segundos
            download_socket.connect((ip_address, self.client_port))
        
            # Solicitar arquivo
            request = f"GET {filename}"
            download_socket.send(request.encode('utf-8'))
        
            # Receber arquivo
            download_path = os.path.join(self.downloads_folder, filename)
            bytes_received = 0
        
            with open(download_path, 'wb') as f:
                while True:
                    chunk = download_socket.recv(4096)
                    if not chunk:
                        break
                    f.write(chunk)
                    bytes_received += len(chunk)
        
            download_socket.close()
            print(f"Arquivo {filename} baixado com sucesso ({bytes_received} bytes) para {download_path}")
        
        except Exception as e:
            print(f"Erro ao baixar arquivo: {e}")
    
    def user_interface(self):
        """Interface do usuário"""
        print("\n=== Cliente Napster ===")
        print("Comandos disponíveis:")
        print("1. search <padrão> - Buscar arquivos")
        print("2. download <filename> <ip> - Baixar arquivo")
        print("3. list - Listar meus arquivos")
        print("4. quit - Sair")
        
        while True:
            try:
                command = input("\n> ").strip().split()
                
                if not command:
                    continue
                
                if command[0] == 'search':
                    if len(command) > 1:
                        pattern = ' '.join(command[1:])
                        files = self.search_files(pattern)
                        
                        if files:
                            print(f"\nEncontrados {len(files)} arquivo(s):")
                            for i, file in enumerate(files, 1):
                                print(f"{i}. {file['filename']} ({file['size']} bytes) - {file['ip_address']}")
                        else:
                            print("Nenhum arquivo encontrado.")
                    else:
                        print("Uso: search <padrão>")
                
                elif command[0] == 'download':
                    if len(command) == 3:
                        filename, ip_address = command[1], command[2]
                        self.download_file(filename, ip_address)
                    else:
                        print("Uso: download <filename> <ip>")
                
                elif command[0] == 'list':
                    print("\nMeus arquivos públicos:")
                    if os.path.exists(self.public_folder):
                        for filename in os.listdir(self.public_folder):
                            file_path = os.path.join(self.public_folder, filename)
                            if os.path.isfile(file_path):
                                size = os.path.getsize(file_path)
                                print(f"- {filename} ({size} bytes)")
                
                elif command[0] == 'quit':
                    break
                
                else:
                    print("Comando não reconhecido.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Erro: {e}")
        
        self.disconnect()
    
    def disconnect(self):
        """Desconecta do servidor"""
        try:
            if self.server_socket:
                self.server_socket.send(b"LEAVE")
                response = self.server_socket.recv(1024).decode('utf-8')
                print(f"Desconectado: {response}")
                self.server_socket.close()
            
            if self.file_server_socket:
                self.file_server_socket.close()
                
        except Exception as e:
            print(f"Erro ao desconectar: {e}")

if __name__ == "__main__":
    client = NapsterClient()
    try:
        client.start()
    except KeyboardInterrupt:
        print("\nDesconectando...")
        client.disconnect()
