class ProcessOperation:
    def __init__(self, input) -> None:
        input = input.replace("\n", "")
        input = input.replace(" ", "")
        input = input.split(",")

        self.pid = int(input[0])
        self.opcode = int(input[1])
        self.filename = input[2]
        # Checar se for operação de criar arquivo e definir valor para o tamanho
        if self.opcode == 0: self.file_size = int(input[3])
        else: self.file_size = None
