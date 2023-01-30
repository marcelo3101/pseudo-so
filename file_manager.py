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

        if(name in [file.name for file in self.files]):
            self.log.append({
                "status": "Falha",
                "mensagem": f"O processo P{str(creator)} nao criou o arquivo (Arquivo ja existe no disco)"
            })
        else:
            for i in range(self.blocks_quantity):
                block = self.disc[i]

                if block == 0:
                    available += 1

                    if available == size:
                        offset = i - available + 1

                        for j in range(size):
                            self.disc[offset + available + j] = name
                            offset += 1

                        file = File([name, offset, size], creator)

                        self.files.append(file)
                        self.log.append({
                            "status": "Sucesso",
                            "mensagem": f"O processo P{str(creator)} criou o arquivo"
                        })
                else:
                    available = 0

            if available == 0:
                self.log.append({
                    "status": "Falha",
                    "mensagem": f"O processo P{str(creator)} nao criou o arquivo (sem espaco livre)"
                })

    
    def delete_file(self, filename, process: Process):
        if filename not in self.files:
            self.log.append({
                "status": "Falha",
                "mensagem": f"O processo {str(process.pid)} nao pode deletar o arquivo {filename}, pois ele não existe"
            })
            return
        file= self.files[filename]  # Pega as informações do arquivo
        if process.priority != 0 and file["process_id"] != process.PID:
            self.log.append({
                "status": "Falha",
                "mensagem": f"O processo {str(process.pid)} nao pode deletar o arquivo {filename}, pois o arquivo não foi criado por ele"
            })
        else:
            # Atualiza o mapa do disco
            for i in range(file["memory_blocks"]):
                self.disc[file["first_block"] + i] = 0
            self.log.append({
                "status": "Sucesso",
                "mensagem": f"O processo {str(process.pid)} deletou o arquivo {filename}"
            })
        

    def operate_process(self, process):
        ops = [op for op in self.operations if op.processId == process.pid]
        print(f"ops {ops}")

        for op in ops:
            if (op.opcode == 0):
                self.create_file(op.file, op.size, process.pid)
            else:
                self.delete_file(op.filename)
                    
            self.operations.remove(op)
