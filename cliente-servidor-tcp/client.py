import socket
import os
import time
import csv

def client():
    server_ip = input("Digite o IP do servidor: ")
    server_port = int(input("Digite a porta do servidor: "))  # suportar a escolha de porta

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    
    startTime = time.time()
    bytesSent = 0
    bytesReceived = 0

    while True:
        rawCommand = input("Digite um comando (LIST, PUT <arquivo>, QUIT): ")
        command = rawCommand.upper()

        if command.startswith('LIST'):
            client_socket.send(b'LIST')
            bytesSent += len(b'LIST')
            files = client_socket.recv(1024).decode()
            print(f"Arquivos no servidor:\n{files}")
        
        elif command.startswith('PUT'):
            filename = rawCommand.split(' ')[1]
            if os.path.exists(filename):
                client_socket.send(f'PUT {filename}'.encode())  # Envia o comando PUT para o servidor
                bytesSent += len(f'PUT {filename}')
                with open(filename, 'rb') as f:
                    while (file_data := f.read(1024)):
                        client_socket.send(file_data)  # Envia os dados em blocos de 1024 bytes
                        bytesSent += len(file_data)
                        print(f"Enviando dados do arquivo {filename}...")

                # Após terminar de enviar o arquivo, envia uma mensagem para o servidor indicar o fim
                client_socket.send(b'EOF')  # Sinalizando o fim do arquivo
                bytesSent += len(b'EOF')
                print(f"Arquivo {filename} terminou de ser enviado.")
         
                # Recebe a resposta do servidor após o PUT
                response = client_socket.recv(1024).decode()
                bytesReceived += len(response)
                print(f"Resposta do servidor: {response}")

            else:
                print(f"Arquivo {filename} não encontrado.")
                client_socket.send('ERRO: Arquivo não encontrado'.encode())
                bytesSent += len(f"ERRO: Arquivo não encontrado")
        
        elif command == 'QUIT':
            client_socket.send(b'QUIT')
            bytesSent += len(b'QUIT')
            print("Conexão encerrada.")
            break

    endTime = time.time()
    logs(startTime, endTime, bytesSent, bytesReceived)
    client_socket.close()
    print("Logs salvos em logs.csv")
    
def logs(startTime, endTime, bytesSent, bytesReceived):
    
    fullTime = endTime - startTime
    bytes = bytesSent + bytesReceived
    logsFile = "logs/logs.csv"
    fileExists = os.path.exists(logsFile)
        
    with open(logsFile, "a", newline='') as file:
        writer = csv.writer(file)
        if not fileExists:
            writer.writerow(["Tempo total (s)", "Bytes enviados", "Bytes recebidos", "Bytes totais"])
        writer.writerow([f"{fullTime:.2f}", bytesSent, bytesReceived, f"{bytes:.2f}"])

if __name__ == "__main__":
    client()
