import socket
import os
import time
import csv

def client():
    # Solicita informações de conexão ao usuário
    server_ip = input("Digite o IP do servidor: ")
    server_port = int(input("Digite a porta do servidor: "))

    # Cria socket TCP e estabelece conexão com o servidor
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    
    startTime = time.time()
    bytesSent = 0
    bytesReceived = 0

    # Loop principal - processa comandos do usuário
    while True:
        rawCommand = input("Digite um comando (LIST, PUT <arquivo>, QUIT): ")
        command = rawCommand.upper()

        # Comando LIST: solicita lista de arquivos do servidor
        if command.startswith('LIST'):
            client_socket.send(b'LIST')
            bytesSent += len(b'LIST')
            files = client_socket.recv(1024).decode()
            print(f"Arquivos no servidor:\n{files}")
        
        # Comando PUT: envia um arquivo para o servidor
        elif command.startswith('PUT'):
            filename = rawCommand.split(' ')[1]
            if os.path.exists(filename):
                # Envia comando PUT com nome do arquivo
                client_socket.send(f'PUT {filename}'.encode())
                bytesSent += len(f'PUT {filename}')
                
                # Abre e envia arquivo em chunks de 1024 bytes
                with open(filename, 'rb') as f:
                    while (file_data := f.read(1024)):
                        client_socket.send(file_data)
                        bytesSent += len(file_data)
                        print(f"Enviando dados do arquivo {filename}...")

                # Envia marcador EOF para sinalizar fim da transferência
                client_socket.send(b'EOF')
                bytesSent += len(b'EOF')
                print(f"Arquivo {filename} terminou de ser enviado.")
         
                # Aguarda confirmação do servidor
                response = client_socket.recv(1024).decode()
                bytesReceived += len(response)
                print(f"Resposta do servidor: {response}")

            else:
                print(f"Arquivo {filename} não encontrado.")
                client_socket.send('ERRO: Arquivo não encontrado'.encode())
                bytesSent += len(f"ERRO: Arquivo não encontrado")
        
        # Comando QUIT: encerra a conexão
        elif command == 'QUIT':
            client_socket.send(b'QUIT')
            bytesSent += len(b'QUIT')
            print("Conexão encerrada.")
            break

    # Finaliza sessão e gera logs de desempenho
    endTime = time.time()
    logs(startTime, endTime, bytesSent, bytesReceived)
    client_socket.close()
    print("Logs salvos em logs.csv")

# Função para gerar arquivo de log com métricas da sessão
def logs(startTime, endTime, bytesSent, bytesReceived):
    
    fullTime = endTime - startTime
    bytes = bytesSent + bytesReceived
    logsFile = "logs/logs.csv"
    fileExists = os.path.exists(logsFile)
    
    # Cria/atualiza arquivo CSV com logs
    with open(logsFile, "a", newline='') as file:
        writer = csv.writer(file)
        if not fileExists:
            writer.writerow(["Tempo total (s)", "Bytes enviados", "Bytes recebidos", "Bytes totais"])
        writer.writerow([f"{fullTime:.2f}", bytesSent, bytesReceived, f"{bytes:.2f}"])

if __name__ == "__main__":
    client()
