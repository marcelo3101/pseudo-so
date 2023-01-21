# Classe que representa o arquivo
# DEVE ter um campo com o processo que a criou

class File:
    def __init__(self, file, creator = None):
        file = file.split(",")

        self.name = file[0]
        self.start_block = int(file[1])
        self.size = int(file[2])
        self.creator = creator


# file = File("file_name, 5, 3", "antonio vinicius")
# print(file.name)