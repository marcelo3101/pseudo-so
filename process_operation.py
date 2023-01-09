class ProcessOperation:
    def __init__(self, operation) -> None:
        operation = operation.split(',')
        self.pid = int(operation[0])
        self.opcode = int(operation[1])
        self.filename = operation[2]
        # Checar se for operação de criar arquivo e definir valor para o tamanho
        if self.opcode == 0: self.file_size = int(operation[3])
        else: self.file_size = None
