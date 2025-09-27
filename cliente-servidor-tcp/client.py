import socket
import os

def client():
    server_ip = input("Digite o IP do servidor: ")
    server_port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    while True:
        command = input("Digite um comando (LIST, PUT <arquivo>, QUIT): ")
        client_socket.send(command.encode())

        if command.startswith('LIST'):
            files = client_socket.recv(1024).decode()
            print(f"Arquivos no servidor:\n{files}")
        
        elif command.startswith('PUT'):
            filename = command.split(' ')[1]
            if os.path.exists(filename):
                client_socket.send(command.encode())  # Envia o comando PUT para o servidor
                with open(filename, 'rb') as f:
                    while (file_data := f.read(1024)):
                        client_socket.send(file_data)  # Envia os dados em blocos de 1024 bytes
                        print(f"Enviando dados do arquivo {filename}...")

                # Após terminar de enviar o arquivo, envia uma mensagem para o servidor indicar o fim
                client_socket.send(b'EOF')  # Sinalizando o fim do arquivo
                print(f"Arquivo {filename} terminou de ser enviado.")
         
                # Recebe a resposta do servidor após o PUT
                response = client_socket.recv(1024).decode()
                print(f"Resposta do servidor: {response}")

            else:
                print(f"Arquivo {filename} não encontrado.")
                client_socket.send('ERRO: Arquivo não encontrado'.encode())
        
        elif command == 'QUIT':
            print("Conexão encerrada.")
            break

    client_socket.close()

if __name__ == "__main__":
    client()
