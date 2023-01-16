# Classe que representa o arquivo
# DEVE ter um campo com o processo que a criou

class File:
    def __init__(self, name, first_block, memory_blocks, process_id = None) -> None:
        self.name = name  # Nome do arquivo
        self.first_block = first_block  # Primeiro bloco que ocupa no disco
        self.memory_blocks = memory_blocks  # Quantidade de blocos do disco que ocupa
        self.process_id = process_id  # ID do processo que criou, caso tiver