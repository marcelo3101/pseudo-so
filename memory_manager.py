from process import Process

REAL_TIME = 64  # Quantidade de blocos para tempo real
USER = 960  # Quantidade de blocos para processos de usuário

class MemoryManager:
    def __init__(self) -> None:
        """
            Array que representa os blocos da memória.
            Inicialmente ele possui REAL_TIME + USER elementos inicializados com o valor 0.
            0 representa que o bloco está livre e 1 representa que o bloco está ocupado
            Divisão dos blocos
                0 a 63 - Tempo real
                64 a 1023 - Processos de usuário
        """
        self.memory = [0] * (REAL_TIME + USER)

    def allocate(self, process: Process) -> bool:
        """
            Aloca um processo na memória
        """
        if process.first_block is not None:
            print(f"O processo {str(process.PID)} já está alocado")
            return False
        start = 0  # Índice em que o loop vai ser iniciado
        end = 63  # Índice em que o loop vai ser encerrado
        # Alterar os índices de referência dependendo do tipo de processo
        if process.priority != 0:
            start = REAL_TIME
            end = REAL_TIME + USER - 1
        first_free = -1  # Utilizado para salvar o índice do primeiro bloco livre encontrado
        current = start  # Utilizado para manter o acompanhamento de qual índice estamos
        available_blocks = 0  # Saber quantos blocos contíguos estão livres
        while current <= end:
            if self.memory[current] == 0:  # Achou um bloco livre
                available_blocks += 1  # Incrementa contador de blocos livres 
                if first_free == -1: 
                    first_free = current  # Caso seja o primeiro bloco livre da sequência, salvar esse índice
                    if ((end - current) + 1) < process.memory_blocks:  # Verificar se existe a possibilidade de termos blocos suficientes
                        break
            
            else: # self.memory[current] == 1, encontramos bloco ocupado
                first_free = -1
                available_blocks = 0
            if available_blocks == process.memory_blocks:  # Encontramos blocos contíguos suficientes
                process.first_block = first_free  # Indica bloco inicial em que foi alocado
                # Atualiza a memória
                for i in range(process.memory_blocks):
                    self.memory[i + first_free] = 1
                return True
            
            current += 1
        
        if process.first_block is None:
            print(f"O processo {str(process.PID)} não foi alocado por falta de espaço")
            return False
    
    def free(self, process: Process) -> None:
        """
            Libera o espaço ocupado por um processo
        """
        if process.first_block is None:
            print("Processo não está na memória")
            return
        for i in range(process.memory_blocks):
            self.memory[i + process.first_block] = 0
        process.first_block = None


                