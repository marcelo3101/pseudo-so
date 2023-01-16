# Gerencia os arquivos e aas operações dos arquivos
# deve ter uma lista com os objetos da classe File (de fioe.py)
# deve ter uma lista com as operações qe foram feitas (são dadas na entrada)
from file import File

class FileManager:
    def __init__(self, blocks) -> None:
        self.disk_blocks = blocks  # Quantidade de blocos que o disco possui
        self.disk = []  # Representação dos blocos do disco
        self.operations = []  # Operações de arquivo recebidas do .txt 
        self.files = {}  #  Lista com objetos dos arquivos para controle Será que é melhor um dicionário devido a busca mais rápida?

    def add_file(self, file: File):
        self.files[file.name] = [file.first_block, file.memory_blocks, file.process_id]

    def init_disk(self) -> None:
        """
            Inicializa o disco alocando os arquivos recebidos no arquivo txt em seus respectivos segmentos
        """
