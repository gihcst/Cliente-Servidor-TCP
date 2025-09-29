import socket
import os
import threading

# Função principal para manipular as requisições de cada cliente conectado
def handle_client(client_socket):
    try:
        # Loop principal para processar comandos do cliente
        while True:
            # Recebe e decodifica o comando enviado pelo cliente
            data = client_socket.recv(1024).decode()

            # Se recv retorna vazio, o cliente desconectou
            if not data:
                break

            # Comando LIST: envia lista de arquivos do servidor para o cliente
            if data.startswith('LIST'):
                print("comando LIST recebido.")
                files = os.listdir('./')
                print("Enviando lista de arquivos para o cliente.")
                client_socket.send("\n".join(files).encode())
                print("Lista de arquivos enviada.")
            
            # Comando PUT: recebe um arquivo enviado pelo cliente
            elif data.startswith('PUT'):
                print("comando PUT recebido.")
                try:
                    filename = data.split(' ', 1)[1]
                except IndexError:
                    print("Erro: comando PUT recebido sem nome de arquivo.")
                    continue

                print(f"Preparando para receber o arquivo: {filename}")
                client_socket.send(b'OK_PUT')
                
                with open(filename, 'wb') as f:
                    while True:
                        chunk = client_socket.recv(1024)  # Recebe chunks de 1024 bytes
                        if not chunk:
                            break  # Conexão fechada pelo cliente
                        
                        # Procura pelo marcador EOF em qualquer parte do chunk recebido
                        if b'EOF' in chunk:
                            print("EOF")
                            # Separa o conteúdo do arquivo do marcador EOF
                            file_content, _, _ = chunk.partition(b'EOF')
                            f.write(file_content)
                            break  # Fim da transferência
                        else:
                            # Escreve o chunk completo (dados do arquivo)
                            f.write(chunk)

                print(f"Arquivo {filename} salvo com sucesso")
                client_socket.send(f'Arquivo {filename} recebido com sucesso'.encode())
            
            # Comando QUIT: encerra a conexão com o cliente
            elif data == 'QUIT':
                print("comando QUIT recebido")
                client_socket.send('Conexão encerrada'.encode())
                break

    except Exception as e:
        print(f"Erro no servidor: {e}")
    finally:
        # Garante que a conexão seja fechada corretamente
        print(f"Fechando conexão.")
        client_socket.close()

# Função principal para configurar e inicializar o servidor TCP
def server():
    # Solicita a porta de conexão ao usuário
    server_port = int(input("Digite a porta que o server vai escutar: "))  
    
    # Cria socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', server_port))  # Vincula a todas as interfaces de rede
    server_socket.listen(5)  # Permite até 5 conexões pendentes
    print(f"[+] Servidor iniciado na porta {server_port}, aguardando conexões...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[+] Conexão estabelecida com {addr}")
        
        # Cria thread separada para cada cliente (suporte a múltiplos clientes)
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    server()