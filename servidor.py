import socket
import threading
import json
import os
from typing import Dict, List

class NapsterServer:
    def __init__(self, host='localhost', port=1234):
        self.host = host
        self.port = port
        self.all_files: Dict[str, List[Dict]] = {}
        self.clients: Dict[str, socket.socket] = {}
        self.server_socket = None
        
    def start(self):
        """Inicia o servidor"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Servidor iniciado em {self.host}:{self.port}")
            
            while True:
                client_socket, client_address = self.server_socket.accept()
                client_socket.settimeout(60)  # Timeout de 60 segundos
                print(f"Nova conexão de {client_address}")
                
                # Criar thread para lidar com o cliente
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except Exception as e:
            print(f"Erro no servidor: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()
    
    def handle_client(self, client_socket: socket.socket, client_address):
        """Lida com as mensagens de um cliente específico"""
        ip_address = None
        
        try:
            while True:
                try:
                    data = client_socket.recv(1024).decode('utf-8').strip()
                    if not data:
                        break
                    
                    print(f"Recebido de {client_address}: {data}")
                    response = self.process_message(data, client_address[0])
                    
                    if response:
                        client_socket.send(response.encode('utf-8'))
                    
                    # Se for comando JOIN, guardar referência do cliente
                    if data.startswith('JOIN'):
                        ip_address = data.split()[1]
                        self.clients[ip_address] = client_socket
                    
                    # Se for comando LEAVE, sair do loop
                    if data == 'LEAVE':
                        break
                        
                except socket.timeout:
                    continue
                except ConnectionResetError:
                    print(f"Cliente {client_address} desconectou abruptamente")
                    break
                
        except Exception as e:
            print(f"Erro ao lidar com cliente {client_address}: {e}")
        finally:
            # Limpar dados do cliente ao desconectar
            if ip_address:
                self.user_leave(ip_address)
                print(f"Cliente {ip_address} removido da rede")
            try:
                client_socket.close()
            except:
                pass
    
    def process_message(self, message: str, client_ip: str) -> str:
        """Processa mensagens recebidas dos clientes"""
        parts = message.split()
        command = parts[0]
        
        if command == 'JOIN':
            ip_address = parts[1]
            return self.handle_join(ip_address)
            
        elif command == 'CREATEFILE':
            filename = parts[1]
            size = int(parts[2])
            return self.handle_create_file(client_ip, filename, size)
            
        elif command == 'DELETEFILE':
            filename = parts[1]
            return self.handle_delete_file(client_ip, filename)
            
        elif command == 'SEARCH':
            pattern = ' '.join(parts[1:])
            return self.handle_search(pattern)
            
        elif command == 'LEAVE':
            return self.handle_leave(client_ip)
            
        return "UNKNOWN COMMAND"
    
    def handle_join(self, ip_address: str) -> str:
        """Processa comando JOIN"""
        if ip_address not in self.all_files:
            self.all_files[ip_address] = []
        print(f"Usuário {ip_address} entrou na rede")
        return "CONFIRMJOIN"
    
    def handle_create_file(self, ip_address: str, filename: str, size: int) -> str:
        """Processa comando CREATEFILE"""
        self.add_file(ip_address, {"filename": filename, "size": size})
        print(f"Arquivo {filename} adicionado para {ip_address}")
        return f"CONFIRMCREATEFILE {filename}"
    
    def handle_delete_file(self, ip_address: str, filename: str) -> str:
        """Processa comando DELETEFILE"""
        if ip_address in self.all_files:
            self.all_files[ip_address] = [
                f for f in self.all_files[ip_address] 
                if f["filename"] != filename
            ]
        print(f"Arquivo {filename} removido de {ip_address}")
        return f"CONFIRMDELETEFILE {filename}"
    
    def handle_search(self, pattern: str) -> str:
        """Processa comando SEARCH"""
        results = self.search(pattern)
        if not results:
            return "NO FILES FOUND"
        
        response_lines = []
        for result in results:
            response_lines.append(
                f"FILE {result['filename']} {result['ip_address']} {result['size']}"
            )
        return '\n'.join(response_lines)
    
    def handle_leave(self, ip_address: str) -> str:
        """Processa comando LEAVE"""
        self.user_leave(ip_address)
        print(f"Usuário {ip_address} saiu da rede")
        return "CONFIRMLEAVE"
    
    def add_file(self, ip_address: str, file: dict):
        """Adiciona arquivo à lista de um usuário"""
        if ip_address not in self.all_files:
            self.all_files[ip_address] = []
        self.all_files[ip_address].append(file)
    
    def user_leave(self, ip_address: str):
        """Remove usuário e seus arquivos"""
        if ip_address in self.all_files:
            del self.all_files[ip_address]
        if ip_address in self.clients:
            del self.clients[ip_address]
    
    def search(self, pattern: str) -> List[Dict]:
        """Busca arquivos que contenham o padrão especificado"""
        result = []
        for ip_address in self.all_files.keys():
            for file in self.all_files[ip_address]:
                if pattern.lower() in file["filename"].lower():
                    result.append({
                        "ip_address": ip_address,
                        "filename": file["filename"],
                        "size": file["size"]
                    })
        return result
    
    def stop(self):
        """Para o servidor"""
        if self.server_socket:
            self.server_socket.close()

if __name__ == "__main__":
    server = NapsterServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nParando servidor...")
        server.stop()
