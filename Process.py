#armazena informacoes de cada processo

class Proccess:

    def __init__(self, input):

        # tratar entrada
        input = input.split(',')
        #obs: verificar se precisa especificar espaço também
        
        # atribuir valores:

        self.init_time =        int(input[0])       # tempo de inicialização
        self.priority =         int(input[1])       # prioridade
        self.processing_time =  int(input[2])       # tempo de processador
        self.memory_blocks =    int(input[3])       # blocos em memória
        self.printer_code_req = int(input[4])       # número-código da impressora requisitada
        self.scanner_req =      int(input[5])       # requisição do scanner
        self.modem_req =        int(input[6])       # requisição do modem
        self.disk_code =        int(input[7])       # número-código do disco
        self.PID = None                             # definido pelo process manager
        self.instructions = []                      # instruções do processo

    def add_instruction(self, instruction):
        
        # tratar a entrada
        # . . . 
        # adiciona instrucoes (organizadas em lista)
        self.instructions.append(instruction)
