# **pseudo-so**

## - **Introdução**

Implementação de um pseudo-SO multiprogramado, composto por um Gerenciador de Processos, por um Gerenciador de Memória, por um Gerenciador de E/S e por um Gerenciador de Arquivos. O gerenciador de processos deve ser capaz de agrupar os processos em quatro níveis de prioridades. O gerenciador de memória deve garantir que um processo não acesse as regiões de memória de um outro processo. O gerenciador de E/S deve ser responsável por administrar a alocação e a liberação de todos os recursos disponíveis, garantindo uso exclusivo dos mesmos. E o gerenciador de arquivos deve permitir que os processos possam criar e deletar arquivos, de acordo com o modelo de alocação determinado. Os detalhes para a implementação desse pseudo-SO são descritos nas próximas seções.

## - **Integrantes**


- Antônio Vinicius de Moura - 190084502

- Luca Delpino Barbabella - 180125559

- Marcelo Aiache Postiglione - 180126652

## - **Instalação**

Para executar o **pseudo-so** é preciso instalar o **Python 3.10**, para isso, basta seguir o tutorial abaixo:

### Windows:

1. Abra seu navegador e vá até a página de download do Python 3.10. Clique no botão "Download Python 3.10" para baixar o instalador.

2. Uma vez que o download seja concluído, execute o instalador que você baixou. Uma janela de instalação será aberta.

3. Na janela de instalação, você verá uma opção para instalar o Python. Certifique-se de que esta opção esteja marcada.

4. Clique no botão "Instalar". O instalador vai começar a instalar o Python 3.10 no seu computador.

5. Quando a instalação for concluída, você pode começar a usar o Python. Para isso, abra o Prompt de Comando e execute o comando "python".

### Mac:

1. Abra seu navegador e vá até a página de download do Python 3.10. Clique no botão "Download Python 3.10" para baixar o arquivo ".dmg" do instalador.

2. Uma vez que o download seja concluído, abra o arquivo ".dmg" e selecione o instalador.

3. Na janela de instalação, você verá uma opção para instalar o Python. Certifique-se de que esta opção esteja marcada.

4. Clique no botão "Instalar". O instalador vai começar a instalar o Python 3.10 no seu computador.

5. Quando a instalação for concluída, você pode começar a usar o Python. Para isso, abra o Terminal e execute o comando "python".

### Linux:

1. Abra seu terminal e execute o comando "sudo apt-get install python3". Isto irá instalar o Python 3 no seu sistema.

2. Uma vez que a instalação for concluída, você pode começar a usar o Python. Para isso, abra o Terminal e execute o comando "python3".

## -**Uso**

1. Com o prompt de comando aberto, navegue até a pasta onde está o arquivo *main.py*.

2. Nesse mesmo caminho, é preciso ter um arquivo chamado *processes.txt*, onde é especificado em cada linha as informações sobre o processo que sera executado. As linhas desse arquivo segue a seguinte estrutura: 

```
<tempo de inicialização>,<prioridade>,<tempo de processador>,<blocos em memória>,<número-código da impressora requisitada>,<requisição do scanner>,<requisição do modem>,<número-código do disco>
```

Exemplo:

```
2, 0, 3, 64, 0, 0, 0, 0
8, 0, 2, 64, 0, 0, 0, 0
```

3. É necessário também, um arquivo chamado *files.txt* que contém a representação do estado do disco. Esse arquivo segue a seguinte estrutura:

```
Primeira linha: <quantidade de blocos do disco>
Segunda linha: <quantidade de segmentos ocupados no disco>
Demais linhas: <arquivo>,<número do primeiro>,<bloco gravado>,<quantidade de blocos ocupados por este arquivo>
```

Exemplo:

```
10
3
X, 0, 2
Y, 3, 1
Z, 5, 3
0, 0, A, 5
0, 1, X
2, 0, B, 2
0, 0, D, 3
1, 0, E, 2
```

4. Com esses arquivos configurados, é preciso executar o arquivo *main.py*, para isso, basta digitar o seguinte comando no caminho onde estão localizados os arquivos: "python3 main.py" **(sem as aspas)**.

5. Se os arquivos *main.py*, *processes.txt* e *files.txt* estiverem corretos, o prompt de comando exibirá o resultado da execução.