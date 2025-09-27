
# Aplicação Cliente-Servidor

Passo a passo para executar a aplicação. Vamos usar duas janelas de terminal: uma para atuar como o **Servidor** e outra para o **Cliente**.

## **Fase 1: Preparação do Ambiente**

Nesta fase, vamos organizar os arquivos e preparar nosso computador.

### **Passo 1: Organize os Arquivos do Projeto**

  * Crie uma pasta em um local de fácil acesso no seu computador. Por exemplo: `C:\Projetos\AppClienteServidor`.
  * Coloque os três arquivos (`Dockerfile`, `client.py`, `server.py`) dentro desta pasta.

### **Passo 2: Abra o Terminal Principal**

  * Você precisa de uma interface de linha de comando.
      * **No Windows:** Abra o menu Iniciar e digite `PowerShell`. Abra o **Windows PowerShell**.
      * **No macOS ou Linux:** Abra o aplicativo chamado `Terminal`.
  * Este será o nosso **Terminal 1**. Usaremos ele para construir a imagem e rodar o servidor.

### **Passo 3: Navegue até a Pasta do Projeto (No Terminal 1)**

  * No terminal que você acabou de abrir, use o comando `cd` (change directory) para entrar na pasta que você criou no Passo 1.
  * **Exemplo para Windows:**
    ```powershell
    cd C:\Projetos\AppClienteServidor
    ```
  * **Exemplo para macOS ou Linux:**
    ```bash
    cd ~/Projetos/AppClienteServidor
    ```
  * **Resultado:** Seu prompt de comando agora deve indicar que você está dentro da pasta correta.

## **Fase 2: Construção e Execução com Docker**

Agora que estamos no lugar certo, vamos usar o Docker para criar e rodar a aplicação.

### **Passo 4: Crie a Rede e a Imagem Docker (No Terminal 1)**

  * Ainda no **Terminal 1**, execute os dois comandos abaixo, um após o outro.
  * **Primeiro, crie a rede virtual** para que os contêineres possam se comunicar pelo nome:
    ```bash
    docker network create minha_rede
    ```
  * **Segundo, construa a imagem Docker.** Este comando lê o arquivo `Dockerfile` e cria um "molde" para nossos contêineres:
    ```bash
    docker build -t cliente-servidor-tcp .
    ```
  * **Resultado:** O Docker fará o download do Ubuntu e instalará os pacotes necessários, criando uma imagem chamada `cliente-servidor-tcp`. Isso pode demorar alguns minutos na primeira vez.

### **Passo 5: Inicie o Servidor (No Terminal 1)**

  * No mesmo **Terminal 1**, execute o comando abaixo. Ele vai usar a imagem que acabamos de criar para iniciar o contêiner do servidor.
    ```bash
    docker run --rm -it --name servidor --network minha_rede -p 12345:12345 cliente-servidor-tcp python3 server.py
    ```
  * **Resultado:** Você verá a mensagem `[+] Servidor iniciado, aguardando conexões...`.
  * **IMPORTANTE:** Este terminal agora é o console do seu servidor. Ele está ocupado e esperando por clientes. **Não feche esta janela!** Apenas minimize-a e deixe-a rodando.

### **Passo 6: Abra um SEGUNDO Terminal para o Cliente**

  * Agora, você precisa abrir uma **NOVA JANELA DE TERMINAL**.
      * Repita o Passo 2: Abra um novo PowerShell ou Terminal.
  * Este será o nosso **Terminal 2**. Usaremos ele exclusivamente para o cliente. Ter duas janelas abertas permite ver o servidor e o cliente funcionando ao mesmo tempo.

### **Passo 7: Inicie o Contêiner do Cliente (No Terminal 2)**

  * Neste **Terminal 2**, execute o comando abaixo para iniciar o contêiner do cliente:
    ```bash
    docker run --rm -it --name cliente --network minha_rede cliente-servidor-tcp
    ```
  * **Resultado:** O seu prompt de comando vai mudar para algo como `root@xxxxxxxxxxxx:/app#`. Isso significa que você não está mais no seu computador, mas sim **dentro do shell do contêiner do cliente**. É neste ambiente que vamos executar os próximos comandos.

## **Fase 3: Interagindo com a Aplicação**

Todos os comandos a seguir são executados no **Terminal 2**, dentro do contêiner do cliente.

### **Passo 8: Crie Arquivos e Execute o Cliente (No Terminal 2)**

1. **Crie um arquivo de teste** para enviar ao servidor. Digite o seguinte comando e pressione Enter:
    ```bash
    echo "este eh um arquivo de teste" > teste.txt
    ```
2. **Inicie o script do cliente** para se conectar ao servidor:
    ```bash
    python3 client.py
    ```
3. **Siga o diálogo da aplicação:**
      * O programa pedirá o IP. Digite `servidor` e pressione Enter.

          * *Por que "servidor"?* Porque os dois contêineres estão na mesma rede (`minha_rede`), e o Docker permite que eles se encontrem usando o nome que definimos (`--name servidor`).

      * Teste os comandos da aplicação (`LIST`, `PUT`, `QUIT`):

        ```
        # Digite "servidor" quando solicitado
        Digite o IP do servidor: servidor

        # Peça a lista de arquivos no servidor
        Digite um comando (LIST, PUT <arquivo>, QUIT): LIST

        # Envie o arquivo que criamos
        Digite um comando (LIST, PUT <arquivo>, QUIT): PUT teste.txt

        # Peça a lista novamente para ver se o arquivo chegou
        Digite um comando (LIST, PUT <arquivo>, QUIT): LIST

        # Encerre a aplicação
        Digite um comando (LIST, PUT <arquivo>, QUIT): QUIT
        ```

## **Fase 4: Finalização**

### **Passo 9: Encerre Tudo**

1. **No Terminal 2 (Cliente):** Após digitar `QUIT`, o script `client.py` terminará. Para sair do contêiner do cliente e voltar ao seu computador, digite `exit` e pressione Enter. A janela do Terminal 2 pode ser fechada.
2. **No Terminal 1 (Servidor):** Volte para a janela do primeiro terminal. Para parar o servidor, pressione as teclas `Ctrl + C`.
3. **Limpeza:** Como usamos a flag `--rm` nos comandos `docker run`, os contêineres do cliente e do servidor serão automaticamente removidos assim que forem parados. Não há mais nada a fazer.

