from process import Process
from process_manager import ProcessManager
from process_operation import ProcessOperation
from file import File
from file_manager import FileManager
from memory_manager import MemoryManager
from resource_manager import ResourceManager

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
    memory_manager = MemoryManager()
    resource_manager = ResourceManager()
    file_system_manager = FileManager()

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
    file_system_manager.blocks_quantity = int(Lines[0])
    Lines.pop(0)  # Remove a linha
    
    # Linha que representa a quantidade de blocos ocupados
    occupied_blocks = int(Lines[0])
    Lines.pop(0)  # Remove a linha
    
    # Lê as linhas
    count = 0
    for line in Lines:
        if count < occupied_blocks:  # Caso for linha que representa um arquivo em disco
            # Criar objeto File
            fileObj = File(line)
            # Passar objeto para o file_manager.files
            file_system_manager.files[fileObj.name] = {
                "first_block": fileObj.first_block,
                "memory_blocks": fileObj.memory_blocks,
                "process_id": fileObj.process_id
            }
            count += 1
        else:  # Linha representa operação
            # Usa a classe ProcessOperation para salvar a instrução
            operation = ProcessOperation(line)
            # A classe FileManager vai ter uma fila de objetos ProcessOperation (FileManager.operations)
            file_system_manager.operations.append(operation)
    disk_file.close()  # Fecha o arquivo

    # Inicializa o file system com os arquivos criados
    file_system_manager.initialize_disc()

    # Sort na global queue pelo init_time dos processos
    process_manager.global_queue = sorted(process_manager.global_queue, key=lambda x: x.init_time)
    time = 0  # Marca o tempo atual

    for i in process_manager.global_queue:
        print("Init time do processo " + str(i.PID) + ": " + str(i.init_time))



    while(process_manager.process_left() or process_manager.in_cpu):
        
        
        # Adiciona novos processos que chegaram no tempo atual a suas determinadas filas
        process_manager.add_by_time(time, memory_manager)

        print("Time = " + str(time))

        # Método que faz escalonamento de processos
        process_manager.process_preemption(memory_manager)
        process_manager.age_process()

        if process_manager.in_cpu:
            print("PID do processo atual:............." + str(process_manager.in_cpu.PID))
            print("Prioridade do processo atual:......" + str(process_manager.in_cpu.priority))
            print("Executed time in CPU:.............." + str(process_manager.in_cpu.time_executed + 1))
            print("Processing time:..................." + str(process_manager.in_cpu.processing_time) + "\n")
            file_system_manager.operate_process(process_manager.in_cpu)  # Realiza uma operação do processo

        # Aumenta tempo de execução antes de virar o while
        time += 1
    
        #if time == 30:
        #    break
    
    # Print do log do file system manager
    print("Sistema de arquivos =>")
    for i, log in enumerate(file_system_manager.log):
        print(f"Operação {i} => " + log["status"] + "\n" + log["mensagem"] + "\n")
    # Print do mapa de ocupação do disco
    print("Mapa de ocupação do disco")
    file_system_manager.print_map()


def printa_fila(fila: ProcessManager):
    a = []
    for i in fila:
        a.append(i.PID)
    return 


if __name__ == "__main__":
    main()