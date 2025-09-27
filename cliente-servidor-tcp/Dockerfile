# Usar a imagem base do Ubuntu 22.04
FROM ubuntu:22.04

# Definir variáveis de ambiente para evitar interações durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Atualizar o sistema e instalar pacotes necessários
RUN apt update && apt upgrade -y && \
    apt install -y \
    build-essential \
    curl \
    iproute2 \
    iputils-ping \
    net-tools \
    iperf3 \
    tcpdump \
    wireshark \
    netcat \
    python3 \
    python3-pip \
    && apt clean

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o código do cliente e servidor para o contêiner
COPY . /app

# Expor portas para TCP
EXPOSE 12345

# Comando padrão
CMD ["bash"]
