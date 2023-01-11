#armazena informacoes de cada processo

class Process:

    def __init__(self, input):
        # tratar entrada
        input = input.replace("\n", "")
        input = input.replace(",", "")
        input = input.split(" ")
        input = [int(i) for i in input]
        print(input)

        #obs: verificar se precisa especificar espaço também

        # atribuir valores:
        self.init_time =        input[0]       # tempo de inicialização
        self.priority =         input[1]       # prioridade
        self.processing_time =  input[2]       # tempo de processador
        self.memory_blocks =    input[3]       # blocos em memória
        self.printer_code_req = input[4]       # número-código da impressora requisitada
        self.scanner_req =      input[5]       # requisição do scanner
        self.modem_req =        input[6]       # requisição do modem
        self.disk_code =        input[7]       # número-código do disco
        self.PID = None                             # definido pelo process manager
        self.first_block = None
        self.instructions = []                      # instruções do processo
        self.time_in_current_queue = 0              # tempo desde chegada à fila atual (usada no aging process)
        self.time_executed = 0                      # quantas unidades de tempo passou exeutando
