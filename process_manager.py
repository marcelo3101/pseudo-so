# administra as filas, escalona os process, cria processos, etc.
from process import Process

# IMPLEMENTAR FUNCIONALIDADE QUE VERIFICA SE PODE INERIR NOVO PROCESSO (NO MÁXIMO 100)
# IMPLEMENTAR FUNCIONALIDADE QUE VERIFICA SE RECURSOS DE E/S DESEJADOS PELOS PROCESSOS ESTÃO DISPONÍVEIS (SE NÃO ESTIVEREM, ROTACIONA FILA)

class ProcessManager:
    MAX = 1000  # Número máximo de processos

    def __init__(self) -> None:
        self.global_queue = []
        self.real_time_queue = []
        # self.user_queue = []
        self.first_queue = []
        self.second_queue = []
        self.third_queue = []
        self.in_cpu = None                      # Processo que está na CPU
        self.pid_tracker = 0                    # Variável usada para definir a pid
        #self.current_processes_priority = 0     # Prioridade do processo presente em CPU

    # Ordenar na global de acordo com o tempo de chegada e só depois adicionar nas filas de prioridade
    def add_new_process(self, process: Process) -> None:  # Adiciona um novo proceso a fila global
        # if self.pid_tracker > 1000: return ERROR
        process.PID = self.pid_tracker  # Define uma ID para o processo
        self.pid_tracker += 1
        self.global_queue.append(process)  # Adiciona o processo a fila global
        
    # Verifica processos com init_time igual ao tempo atual e os adiciona na fila adequada
    def add_by_time(self, current_time):
        for process in self.global_queue:
            if process.init_time == current_time:
                match process.priority:            # Adiciona o processo a fila de prioridade adequada
                    case 0:
                        self.real_time_queue.append(process)
                    case 1:
                        self.first_queue.append(process)
                    case 2:
                        self.second_queue.append(process)
                    case 3:
                        self.third_queue.append(process)
                self.global_queue.remove(process)  # Remove processo da fila global
            # Como a lista está ordenada, ir até o primeiro processo com init_time > current_time
            if process.init_time > current_time:
                break
    
    # Checa se exite algum processo restante
    def process_left(self):
        if (len(self.global_queue) or
            len(self.real_time_queue) or
            len(self.first_queue) or
            len(self.second_queue) or
            len(self.third_queue)):
            return True

    # Verifica se processo finalizou (retorna verdadeiro ou falso)
    def check_process_finish(self) -> None:
        if(self.in_cpu.processing_time == self.in_cpu.time_executed):
            return True
        else:
            return False

    # Verifica se há um processo de maior prioridade para ser executado (retorna [(V ou F para existencia), (Qual a prioridade da nova fila (mais alta))])
    def check_higher_priority(self) -> None:
        queue_check = []
        queue_check.append(self.real_time_queue)
        queue_check.append(self.first_queue)
        queue_check.append(self.second_queue)
        queue_check.append(self.third_queue)
        
        new_list = None # Variavel que indica nova fila a ser executada, começa em None pois a principio não iremos trocar

        # Verifica se as filas de prioridade maior estão vazias. Se não estiverem, determina a nova fila a ser executada
        for i in range(4):
            if (i < self.in_cpu.priority and len(queue_check[i]) > 0):
                new_list = i
                break
            else:
                break

        # Se houver processo de prioridade maior, bota novo processo na cpu
        if(new_list != None):
            return [True, new_list]
        else:
            return [False, new_list]

    # Verifica se há um processo de menor prioridade para ser executado (retorna [(V ou F para existencia), (Qual a prioridade da nova fila (mais alta))])
    def check_lower_priority(self) -> None:
        queue_check = []
        queue_check.append(self.real_time_queue)
        queue_check.append(self.first_queue)
        queue_check.append(self.second_queue)
        queue_check.append(self.third_queue)

        new_list = None # Variavel que indica nova fila a ser executada, começa em None pois a principio não iremos trocar

        # Verifica se as filas de prioridade menor estão vazias. Se não estiverem, determina a nova fila a ser executada
        for i in range(self.in_cpu.priority,4):
            if (i > self.in_cpu.priority and len(queue_check[i]) > 0):
                new_list = i
                break
            else:
                break

        # Se houver processo de prioridade menor, bota novo processo na cpu
        if(new_list):
            return [True, new_list]
        else:
            return [False, new_list]

    # Carrega processo a ser executado na cpu, e remove de sua fila. Também devolve processo que ocupa a cpu se ele não tiver sido finalizado
    def load_process(self, queue_priority) -> None:
        
        # Se a CPU estiver vazia, carrega imediatamente
        if(self.in_cpu == None):
            self.in_cpu = queue_priority[0]
            queue_priority.pop(0)
            return
        
        finished = self.check_process_finish()
        
        # Devolve processo à fila caso não finalizado
        if(not finished):
            match self.in_cpu.priority:
                case 0:
                    return      # Se o processo não terminou e é prioridade 0, ele deve continuar na CPU
                case 1:
                    self.first_queue.append(self.in_cpu)
                case 2:
                    self.second_queue.append(self.in_cpu)
                case 3:
                    self.third_queue.append(self.in_cpu)
        
        # Bota novo processo na cpu (se finalizou, descarta processo (funciona ate pra prioridade 0), se não, descarta também)
        self.in_cpu = queue_priority[0]
        queue_priority.pop(0)

    # Executa o processo selecionado para ser executado
    # Talvez a funcionalidade abaixo seja implementada na main, conferir com o grupo
    #def execute_process(self) -> None:
        #x = 1 # placeholder

    #Aplica aging nos processos para evitar starvation
    def age_process(self, process: Process) -> None:
        # Só aplicará aging se o processo atualmente na cpu não é processo de tempo real
        if(self.in_cpu.priority != 0):
            # Função arbitrária usada para aumentar prioridade de processos e evitar starvation (sujeita a mudanças)
            if((process.time_in_current_queue >= process.processing_time * 10) and (process.priority != 0)):
                process.priority -= 1

    # Função que garante rotação dos processos dentro das filas obedecendo o quantum
    def process_queue_rotation(self) -> None:
        # Realimenta CPU com processo da mesma fila do processo que está nela
        # self.load_process(self.in_cpu.priority)
       
       # Rotaciona fila somente se elas possuirem pelo menos um processo
        match self.in_cpu.priority:
            # Caso 0 só ocorre quando o na CPU acabar (FIFO). Avaliar necessidade de manter case 0
            case 0:
                if(len(self.real_time_queue) >= 1):
                    self.load_process(self.real_time_queue)
            case 1:
                if(len(self.first_queue) >= 1):
                    self.load_process(self.first_queue)
            case 2:
                if(len(self.second_queue) >= 1):
                    self.load_process(self.second_queue)
            case 3:
                if(len(self.third_queue) >= 1):
                    self.load_process(self.third_queue)

    # Função que executa preempção de acordo com o estado atual dos processos
    def process_preemption(self, time) -> None:
        
        # Se não há processo na cpu e não há processo para ser escalonado, simplesmente retorna
        #if (not self.in_cpu) and (not len(self.global_queue)):
        #    return

        # Aumenta tracker de tempo de execução do processo
        if self.in_cpu:
            self.in_cpu.time_executed += 1

            # Se processo acabou, remove da CPU
            if self.check_process_finish():
                self.in_cpu = None


        # Se não há processo na CPU e há processo para ser escalonado, carrega o de maior prioridade.
        # Se não houver processo para ser escalonado, simplemente deixa passar
        if self.in_cpu == None:
            if len(self.real_time_queue) > 0:
                self.load_process(self.real_time_queue)
            elif len(self.first_queue) > 0:
                self.load_process(self.first_queue)
            elif len(self.second_queue) > 0:
                self.load_process(self.second_queue)
            elif len(self.third_queue) > 0:
                self.load_process(self.third_queue)
            return

        # Não realiza preempção se o processo for de tempo real e ele não tiver acabado
        if self.in_cpu.priority == 0 and (not self.check_process_finish()):
            return
        
        # Checa se há processo de prioridade maior
        check_high = self.check_higher_priority()
        if(check_high[0]):
            match check_high[1]:
                case 0:
                    nova_fila_prioridade = self.real_time_queue
                case 1:
                    nova_fila_prioridade = self.first_queue
                case 2:
                    nova_fila_prioridade = self.second_queue
                case 3:
                    nova_fila_prioridade = self.third_queue

            self.load_process(nova_fila_prioridade)    # Carrega processo de maior prioridade
            return

        # Verifica se a fila atual tem mais membros
        current_queue = self.in_cpu.priority
        match current_queue:
            case 0:
                tamanho_fila_atual = len(self.real_time_queue)
            case 1:
                tamanho_fila_atual = len(self.first_queue)
            case 2:
                tamanho_fila_atual = len(self.second_queue)
            case 3:
                tamanho_fila_atual = len(self.third_queue)

        #Se tiver mais membros na fila atual, rotaciona
        if tamanho_fila_atual >= 1:
            self.process_queue_rotation()   # rotaciona
            return
        
        else:
            # verifica se o processo atual finalizou
            if self.check_process_finish():                # se finalizou
                check_low = self.check_lower_priority()

                if(check_low[0]):
                    match check_low[1]:
                        case 0:
                            nova_fila_prioridade = self.real_time_queue
                        case 1:
                            nova_fila_prioridade = self.first_queue
                        case 2:
                            nova_fila_prioridade = self.second_queue
                        case 3:
                            nova_fila_prioridade = self.third_queue

                    self.load_process(nova_fila_prioridade)    # Carrega nova fila de prioridade
                    return
            else:        # Se não finalizou
                return   # Continua no processo atual






