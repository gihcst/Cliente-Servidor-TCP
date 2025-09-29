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

    while True:
        rawCommand = input("Digite um comando (LIST, PUT <arquivo>, QUIT): ")
        command = rawCommand.upper()

        # Comando LIST: solicita lista de arquivos do servidor
        if command.startswith('LIST'):
            client_socket.send(b'LIST')
            bytesSent += len(b'LIST')
            files = client_socket.recv(1024).decode()
            bytesReceived += len(files.encode())
            print(f"Arquivos no servidor:\n{files}")
        
        # Comando PUT: envia um arquivo para o servidor
        elif command.startswith('PUT'):
            try:
                filename = rawCommand.split(' ', 1)[1]
            except IndexError:
                print("Comando inválido. Use: PUT <nome_do_arquivo>")
                continue
            
            if os.path.exists(filename):
                client_socket.send(f'PUT {filename}'.encode())
                bytesSent += len(f'PUT {filename}'.encode())
                
                # Aguarda confirmação do servidor antes de iniciar transferência
                response = client_socket.recv(1024)
                bytesReceived += len(response)

                # Verifica se servidor confirmou que está pronto para receber
                if response == b'OK_PUT':
                    print(f"Servidor pronto. Enviando arquivo {filename}...")
                    # Abre arquivo e envia em chunks de 1024 bytes
                    with open(filename, 'rb') as f:
                        while (file_data := f.read(1024)):
                            client_socket.send(file_data)
                            bytesSent += len(file_data)

                    # Envia marcador EOF para sinalizar fim da transferência
                    client_socket.send(b'EOF')
                    bytesSent += len(b'EOF')
                    print(f"Arquivo {filename} terminou de ser enviado.")
            
                    # Aguarda confirmação final do servidor
                    final_response = client_socket.recv(1024).decode()
                    bytesReceived += len(final_response.encode())
                    print(f"Resposta do servidor: {final_response}")
                else:
                    print(f"O servidor não confirmou o recebimento. Resposta: {response.decode()}")

            else:
                print(f"Arquivo {filename} não encontrado.")
        
        # Comando QUIT: encerra a conexão
        elif command == 'QUIT':
            client_socket.send(b'QUIT')
            bytesSent += len(b'QUIT')
            response = client_socket.recv(1024).decode()
            bytesReceived += len(response.encode())
            print(f"Resposta do servidor: {response}")
            break
        
        else:
            print("Comando inválido.")

    # Finaliza sessão e gera logs de desempenho
    endTime = time.time()
    logs(startTime, endTime, bytesSent, bytesReceived)
    client_socket.close()
    print("Conexão encerrada. Logs salvos em logs/logs.csv")

# Função para gerar arquivo de log com métricas da sessão
def logs(startTime, endTime, bytesSent, bytesReceived):
    
    fullTime = endTime - startTime
    bytesTotal = bytesSent + bytesReceived
    logsFile = "logs/logs.csv"
    
    # Garante que o diretório 'logs' exista
    os.makedirs(os.path.dirname(logsFile), exist_ok=True)
    
    fileExists = os.path.exists(logsFile)
        
    with open(logsFile, "a", newline='') as file:
        writer = csv.writer(file)
        if not fileExists:
            writer.writerow(["Tempo total (s)", "Bytes enviados", "Bytes recebidos", "Bytes totais"])
        writer.writerow([f"{fullTime:.2f}", bytesSent, bytesReceived, f"{bytesTotal}"])

if __name__ == "__main__":
    client()