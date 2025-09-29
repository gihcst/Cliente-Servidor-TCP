# Aplicação Cliente-Servidor

Passo a passo para executar a aplicação. Vamos usar múltiplas janelas de terminal: uma para o **Servidor**, uma para o **Cliente** e outras para comandos de rede.

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
  * **IMPORTANTE:** Este terminal agora é o console do seu servidor. Ele está ocupado e esperando por clientes. **Não feche esta janela\!** Apenas minimize-a e deixe-a rodando.

### **Passo 6: Abra um SEGUNDO Terminal para o Cliente**

  * Agora, você precisa abrir uma **NOVA JANELA DE TERMINAL**.
      * Repita o Passo 2: Abra um novo PowerShell ou Terminal.
  * Este será o nosso **Terminal 2**. Usaremos ele exclusivamente para o cliente.

### **Passo 7: Inicie o Contêiner do Cliente (No Terminal 2)**

  * Neste **Terminal 2**, execute o comando abaixo para iniciar o contêiner do cliente.
      * **Atenção:** Substitua `"C:\caminho\completo\para\logs\clienteA"` pelo caminho real da pasta onde você quer salvar os logs no seu computador.
    <!-- end list -->
    ```bash
    docker run --rm -it --name cliente --network minha_rede -v "C:\caminho\completo\para\logs\clienteA:/app/logs" --cap-add NET_ADMIN cliente-servidor-tcp
    ```
  * **Por que `--cap-add NET_ADMIN`?** Esta flag concede ao contêiner permissões elevadas para modificar suas próprias configurações de rede. Isso é necessário para rodar os comandos de simulação de rede na Fase 4.
  * **Resultado:** O seu prompt de comando vai mudar para algo como `root@xxxxxxxxxxxx:/app#`. Isso significa que você está **dentro do shell do contêiner do cliente**.

## **Fase 3: Interagindo com a Aplicação**

Todos os comandos a seguir são executados no **Terminal 2**, dentro do contêiner do cliente.

### **Passo 8: Crie Arquivos e Execute o Cliente (No Terminal 2)**

1.  **Crie um arquivo de teste** para enviar ao servidor.
    ```bash
    echo "este eh um arquivo de teste" > teste.txt
    ```
2.  **Inicie o script do cliente** para se conectar ao servidor:
    ```bash
    python3 client.py
    ```
3.  **Siga o diálogo da aplicação:**
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

## **Fase 4: Experimentos de Rede**

Com o servidor e o cliente rodando, você pode usar um **terceiro terminal** no seu computador para executar os comandos abaixo e observar o comportamento da aplicação sob diferentes condições de rede.

### **Passo 9: Simule Condições de Rede com `tc`**

Os comandos a seguir usam `docker exec` para rodar o utilitário `tc` (traffic control) **dentro do contêiner do cliente**, modificando sua interface de rede (`eth0`).

  * **Para adicionar um atraso (latência) de 50ms com variação de 10ms:**
    ```bash
    docker exec -it cliente bash -lc "tc qdisc del dev eth0 root 2>/dev/null || true; tc qdisc add dev eth0 root netem delay 50ms 10ms distribution normal"
    ```
  * **Para simular uma perda de 0.5% dos pacotes:**
    ```bash
    docker exec -it cliente bash -lc "tc qdisc del dev eth0 root 2>/dev/null || true; tc qdisc add dev eth0 root netem loss 0.5%"
    ```
  * **Para remover todas as modificações e voltar ao normal:**
    ```bash
    docker exec -it cliente bash -lc "tc qdisc del dev eth0 root"
    ```

### **Passo 10: Capture o Tráfego de Rede para Análise (Wireshark)**

Você pode capturar toda a comunicação entre cliente e servidor para analisá-la posteriormente no Wireshark.

  * Abra um **novo terminal** (pode ser o Terminal 3) e execute o comando abaixo.

  * **Atenção:** Substitua `"C:\caminho\para\suas\capturas"` pelo caminho real da pasta onde você quer salvar o arquivo de captura.

    ```bash
    docker run --rm -it --name sniff-server --net container:servidor -v "C:\caminho\para\suas\capturas:/pcaps" nicolaka/netshoot tshark -i any -f "tcp port 12345" -w /pcaps/exp1.pcapng
    ```

  * **Entendendo o comando:**

      * `--net container:servidor`: Executa este contêiner no mesmo "espaço" de rede que o contêiner `servidor`, permitindo que ele veja todo o seu tráfego.
      * `-v "C:\...:/pcaps"`: Mapeia uma pasta do seu computador para dentro do contêiner, para que o arquivo de captura seja salvo na sua máquina.
      * `nicolaka/netshoot`: É uma imagem Docker cheia de ferramentas de rede, incluindo o `tshark`.
      * `tshark -i any -f "tcp port 12345" -w /pcaps/exp1.pcapng`: Inicia a captura (`tshark`) em qualquer interface (`-i any`), filtrando apenas pacotes da porta TCP 12345, e salva o resultado no arquivo `/pcaps/exp1.pcapng`.

  * Deixe este comando rodando enquanto você interage com o cliente. Quando terminar, volte a este terminal e pressione `Ctrl + C` para parar a captura. O arquivo `.pcapng` estará na pasta que você especificou, pronto para ser aberto no Wireshark.

## **Fase 5: Finalização**

### **Passo 11: Encerre Tudo**

1.  **No Terminal 2 (Cliente):** Após digitar `QUIT`, o script `client.py` terminará. Para sair do contêiner do cliente e voltar ao seu computador, digite `exit` e pressione Enter. A janela do Terminal 2 pode ser fechada.
2.  **No Terminal 1 (Servidor):** Volte para a janela do primeiro terminal. Para parar o servidor, pressione as teclas `Ctrl + C`.
3.  **Limpeza:** Como usamos a flag `--rm` nos comandos `docker run`, os contêineres (`cliente`, `servidor`, `sniff-server`) serão automaticamente removidos assim que forem parados. Não há mais nada a fazer.
