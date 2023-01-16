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

    # Abre o arquivo dos processos
    processes_file = open('processes.txt', 'r')
    Lines = processes_file.readlines()
    
    # Lê as linhas e cria os objetos dos processos
    for line in Lines:
    
        # Passa as informações do processo ao construtor
        new_process = Process(line)
                
        # Informar ao gerenciador de processos para adicioná-lo na fila global
        process_manager.add_new_process(new_process)

    # Fecha o arquivo
    processes_file.close()

    # Abre o arquivo que representa o estado do disco
    disk_file = open('files.txt', 'r')
    Lines = disk_file.readlines()
    
    # Primeira linha indica quantidade de blocos no disco
    disk_blocks = int(Lines[0])
    Lines.pop(0)  # Remove a linha
    
    # Linha que representa a quantidade de blocos ocupados
    occupied_blocks = int(Lines[0])
    Lines.pop(0)  # Remove a linha
    # Inicializa o sistema de arquivos
    file_manager = FileManager(disk_blocks)
    # Lê as linhas
    count = 0
    for line in Lines:
        if count < occupied_blocks:  # Caso for linha que representa um arquivo em disco
            # Criar objeto File
            file_object = File(line)
            # Passar objeto para o file_manager.files
            file_manager.add_file(file_object)
            count += 1
            continue
        else:  # Linha representa operação
            # Usa a classe ProcessOperation para salvar a instrução
            operation = ProcessOperation(line)
            # A classe FileManager vai ter uma fila de objetos ProcessOperation (FileManager.operations)
            continue
    disk_file.close()  # Fecha o arquivo
    for process in process_manager.global_queue:
        dispatcher(process, process_manager, operation)
    





def printa_fila(fila: ProcessManager):
    a = []
    for i in fila:
        a.append(i.PID)
    return a























if __name__ == "__main__":
    main()