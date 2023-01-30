# Gerencia os arquivos e aas operações dos arquivos
# deve ter uma lista com os objetos da classe File (de fioe.py)
# deve ter uma lista com as operações qe foram feitas (são dadas na entrada)

from file import File

class FileManager:
    def __init__(self):
        self.blocks_quantity = 0
        self.segments_quantity = 0
        self.files = []
        self.operations = []
        self.disc = []
        self.log = []
    
    def initialize_disc(self):
        self.disc = []

        for i in range(self.blocks_quantity):
            self.disc[i] = 0

        for file in self.files:
            if file.start_block != 0:
                self.disc[file.start_block + file.size] = file.name # TODO: TEM QUE VE ISSO AQUI DIREITINHO KKKK
    
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

    
    def delete_file(self, file):
        for i in range(file.size):
            self.disc[file.start_block + i] = 0
    

    def operate_process(self, process):
        ops = [op for op in self.operations if op.processId == process.pid]
        print(f"ops {ops}")

        for op in ops:
            if (op.opcode == 0):
                self.create_file(op.file, op.size, process.pid)
            else:
                file = [file for file in self.files if file.name == op.file]

                if (file != None):
                    if (process.priority == 0 or file.creator == None or process.pid == file.creator):
                        self.delete_file(file)
                        self.log.append({
                            "status": "Sucesso",
                            "mensagem": f"O processo P{str(process.pid)} deletou o arquivo"
                        })
                    else:
                        self.log.append({
                            "status": "Falha",
                            "mensagem": f"O processo {str(process.pid)} nao pode deletar o arquivo"
                        })
                else:
                    self.log.append({
                        "status": "Falha",
                        "mensagem": f"O processo P{str(process.pid)} nao pode deletar o arquivo"
                    })

            self.operations.remove(op)
