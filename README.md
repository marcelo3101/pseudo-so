# pseudo-so

## Introdução

Implementação de um pseudo-SO multiprogramado, composto por um Gerenciador de Processos, por um Gerenciador de Memória, por um Gerenciador de E/S e por um Gerenciador de Arquivos. O gerenciador de processos deve ser capaz de agrupar os processos em quatro níveis de prioridades. O gerenciador de memória deve garantir que um processo não acesse as regiões de memória de um outro processo. O gerenciador de E/S deve ser responsável por administrar a alocação e a liberação de todos os recursos disponíveis, garantindo uso exclusivo dos mesmos. E o gerenciador de arquivos deve permitir que os processos possam criar e deletar arquivos, de acordo com o modelo de alocação determinado. Os detalhes para a implementação desse pseudo-SO são descritos nas próximas seções.

## Integrantes


- Antônio Vinicius de Moura - 190084502

- Luca Delpino Barbabella - 180125559

- Marcelo Aiache Postiglione - 180126652

## Instalação

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

## Uso

1. Com o prompt de comando aberto, navegue até a pasta onde está o arquivo *main.py*. Você pode usar os comandos "cd" para mudar de diretório.

2. Agora, para executar o arquivo *main.py*, digite o seguinte comando: "python3 main.py" **(sem as aspas)**.

3. Se o arquivo *main.py* estiver escrito corretamente, o prompt de comando exibirá o resultado da execução.