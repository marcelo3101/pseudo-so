from process import Process
from process_manager import ProcessManager
from process_operation import ProcessOperation

from file import File
from file_manager import FileManager

# Tratar caso em que depois das execucoes, cou fica livre (tipo None)

def dispatcher(process: Process, process_manager: ProcessManager, process_operation: ProcessOperation):
    print("dispatcher =>")
    print("PID: " + str(process.PID))
    print("    offset: " + str(1024))       # saberemos isso do módulo de memória (mudar isso quando ele estiver completo)
    print("    blocks: " + str(process.memory_blocks))
    print("    priority: " + str(process.priority))
    print("    time: " + str(process.processing_time))
    print("    printers: " + str(process.printer_code_req))
    print("    scanners: " + str(process.scanner_req))
    print("    modems: " + str(process.modem_req))
    print("    drives: " + str(False))       # não sei de onde tiramos essa informação (mudar quando soubermos)

    # Implementar resto do dispatcher

def main():
    # Quantum em milissegundos
    quantum = 1

    # Inicializa gerenciadores
    process_manager = ProcessManager()
    #memory_manager = MemoryManager.new
    #io_manager = IOManager.new
    filesystem_manager = FileManager()

    # Abre o arquivo dos processos
    with open('processes.txt', 'r') as file:
        processes_lines = [line.rstrip() for line in file]
    
    # Lê as linhas e cria os objetos dos processos
    for line in processes_lines:
        # Passa as informações do processo ao construtor
        new_process = Process(line)
        # Informar ao gerenciador de processos para adicioná-lo na fila global
        process_manager.add_new_process(new_process)

    # Abre o arquivo que representa o estado do disco
    with open('files.txt', 'r') as file:
        files_lines = [line.rstrip() for line in file]
    
    # Primeira linha indica quantidade de blocos no disco
    disk_blocks = int(files_lines.pop(0))
    # Linha que representa a quantidade de blocos ocupados
    occupied_blocks = int(files_lines.pop(0)) 

    filesystem_manager.blocks_quantity = disk_blocks
    filesystem_manager.segments_quantity = occupied_blocks

    print(f"files_lines {files_lines}")
    
    # Lê as linhas
    count = 0
    for line in files_lines: # Carrega os arquivos dentro do disco
        if count < occupied_blocks:  # Caso for linha que representa um arquivo em disco
            new_file = File(file=line) # Criar objeto File
            filesystem_manager.files.append(new_file) # guarda o File dentro da classe FileManager
            count += 1
        else:  # Linha representa operação
            # Usa a classe ProcessOperation para salvar a instrução
            operation = ProcessOperation(line)
            # A classe FileManager vai ter uma fila de objetos ProcessOperation (FileManager.operations)

    for process in process_manager.global_queue:
        dispatcher(process, process_manager, operation)
    


def printa_fila(fila: ProcessManager):
    a = []
    for i in fila:
        a.append(i.PID)
    return a


if __name__ == "__main__":
    main()