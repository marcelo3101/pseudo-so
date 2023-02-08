# Classe que representa o arquivo
# DEVE ter um campo com o processo que a criou

class File:
    def __init__(self, input, process_id = None) -> None:
        # Tratar input
        input = input.replace("\n", "")
        input = input.replace(" ", "")
        input = input.split(",")

        self.name = input[0]  # Nome do arquivo
        self.first_block = int(input[1])  # Primeiro bloco que ocupa no disco
        self.memory_blocks = int(input[2])  # Quantidade de blocos do disco que ocupa
        self.process_id = process_id  # ID do processo que criou, caso tiver

