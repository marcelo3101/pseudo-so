from process import Process
from process_manager import ProcessManager
from process_operation import ProcessOperation

def main():
    # Quantum em milissegundos
    quantum = 1

    # Inicializa gerenciadores
    process_manager = ProcessManager()
    #memory_manager = MemoryManager.new
    #io_manager = IOManager.new
    #filesystem_manager = FileManager.new

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
    # Lê as linhas
    count = 0
    for line in Lines:
        if count < occupied_blocks:  # Caso for linha que representa um arquivo em disco
            # Criar objeto File
            # Passar objeto para o file_manager.files
            # ...
            count += 1
            continue
        else:  # Linha representa operação
            # Usa a classe ProcessOperation para salvar a instrução
            operation = ProcessOperation(line)
            # A classe FileManager vai ter uma fila de objetos ProcessOperation (FileManager.operations)
            continue
    disk_file.close()  # Fecha o arquivo


if __name__ == "__main__":
    main()