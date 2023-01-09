# administra as filas, escalona os process, cria processos, etc.
from process import Process

class ProcessManager:
    MAX = 1000  # Número máximo de processos

    def __init__(self) -> None:
        self.global_queue = []
        self.real_time_queue = []
        self.user_queue = []
        self.first_queue = []
        self.second_queue = []
        self.third_queue = []
        self.in_cpu = None  # Processo que está na CPU
        self.pid_tracker = 0  # Variável usada para definir a pid

    def add_new_process(self, process: Process) -> None:  # Adiciona um novo proceso a fila global
        # if self.pid_tracker > 1000: return ERROR
        process.PID = self.pid_tracker  # Define uma ID para o processo
        self.pid_tracker += 1
        self.global_queue.append(process)  # Adiciona o processo a fila global

