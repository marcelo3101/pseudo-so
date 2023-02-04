# Gerencia os arquivos e aas operações dos arquivos
# deve ter uma lista com os objetos da classe File (de fioe.py)
# deve ter uma lista com as operações qe foram feitas (são dadas na entrada)

from file import File
from process import Process

class FileManager:
    def __init__(self):
        self.blocks_quantity = 0
        self.files = {}
        self.operations = []
        self.disc = []
        self.log = []
    
    def initialize_disc(self):
        self.disc = [0] * self.blocks_quantity  # Inicializa o mapa do disco
        # Aloca os arquivos que foram adicionados via .txt
        for file_info in self.files.values():
            for i in range(file_info["memory_blocks"]):
                self.disc[file_info["first_block"] + i] = 1
    
    
    def create_file(self, name, size, creator):
        offset = None
        available = 0

        if name in self.files:
            self.log.append({
                "status": "Falha",
                "mensagem": f"O processo P{str(creator)} nao criou o arquivo (Arquivo já existe no disco)"
            })
        else:
            for i in range(self.blocks_quantity):
                block = self.disc[i]

                if block == 0:
                    available += 1

                    if available == size:
                        offset = i - available + 1

                        for j in range(size):
                            self.disc[offset + j] = 1
                        fileObj = File(name + ", " + str(offset) + ", " + str(size), creator)

                        self.files[fileObj.name] = {
                            "first_block": fileObj.first_block,
                            "memory_blocks": fileObj.memory_blocks,
                            "process_id": fileObj.process_id
                        }
                        self.log.append({
                            "status": "Sucesso",
                            "mensagem": f"O processo P{str(creator)} criou o arquivo {fileObj.name}"
                        })
                else:
                    available = 0

            if offset is None:
                self.log.append({
                    "status": "Falha",
                    "mensagem": f"O processo P{str(creator)} nao criou o arquivo {name} (sem espaco livre)"
                })

    
    def delete_file(self, filename, process: Process):
        if filename not in self.files:
            self.log.append({
                "status": "Falha",
                "mensagem": f"O processo {str(process.PID)} nao pode deletar o arquivo {filename}, pois ele não existe"
            })
            return
        file= self.files[filename]  # Pega as informações do arquivo
        if process.priority != 0 and file["process_id"] != process.PID:
            self.log.append({
                "status": "Falha",
                "mensagem": f"O processo {str(process.PID)} nao pode deletar o arquivo {filename}, pois o arquivo não foi criado por ele"
            })
        else:
            # Atualiza o mapa do disco
            for i in range(file["memory_blocks"]):
                self.disc[file["first_block"] + i] = 0
            self.log.append({
                "status": "Sucesso",
                "mensagem": f"O processo {str(process.PID)} deletou o arquivo {filename}"
            })
        

    def operate_process(self, process: Process):
        # Pegar a próxima operação
        op = None
        for operation in self.operations:
            if operation.pid == process.PID:
                op = operation
                self.operations.remove(operation)
                break
        
        if(op):
            if (op.opcode == 0):
                self.create_file(op.filename, op.file_size, process.PID)
            else:
                self.delete_file(op.filename, process)
                    
        else:
            print("Não tem operação pendente")  # Print para indicar que acabou, mudar dps na integração
