import socket
import os
import threading

# Função para manipular o upload de arquivos
def handle_client(client_socket):
    try:
        while True:
            # Recebe o comando do cliente
            data = client_socket.recv(1024).decode()

            if data.startswith('LIST'):
                # Retorna lista de arquivos do servidor
                print("LIST command received")
                files = os.listdir('./')
                print("Sending file list to client")
                client_socket.send("\n".join(files).encode())
                print("File list sent")
            
            elif data.startswith('PUT'):
                print("PUT command received")
                # Envia o nome do arquivo e faz upload
                filename = data.split(' ')[1]
                print(f"Receiving file: {filename}")
                with open(filename, 'wb') as f:
                    while True:
                        print("Waiting for file data...")
                        file_data = client_socket.recv(1024)
                        if b'EOF' in file_data:
                            file_data = file_data.replace(b'EOF', b'')
                            print(f"Writing data to {filename}")
                            f.write(file_data)
                            break  # Fim do arquivo
                        if file_data == b'EOF':
                            break  # Fim do arquivo
                        print(f"Writing data to {filename}")
                        f.write(file_data)
                print(f"File {filename} saved successfully")
                client_socket.send(f'Arquivo {filename} recebido com sucesso'.encode())
            
            elif data == 'QUIT':
                print("QUIT command received")
                client_socket.send('Conexão encerrada'.encode())
                break

    except Exception as e:
        print(f"Erro no servidor: {e}")
    finally:
        client_socket.close()

# Configuração do servidor
def server():

    server_port = int(input("Digite a porta que o server vai escutar: "))  # suportar a escolha de porta
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', server_port))
    server_socket.listen(5)
    print("[+] Servidor iniciado, aguardando conexões...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[+] Conexão estabelecida com {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    server()
