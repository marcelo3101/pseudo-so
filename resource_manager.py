# Faz administração de alocação de dispositivos de E/S do pseudo-SO

# Processos de tempo real não podem usar esses recursos.
# Não há preempção na alocação de dispositivos E/S

# Processo tenta entrar na CPU, se recursos n estiverem disponiveis, rotaciona
# Se estiverem, garante exclusao mutua, atualiza valores de ocupação e insere processo na CPU
# Quando acabar processo que usa dispositivos SO, acessa região crítica e libera recursos

# Implementaremos uma lógica onde o processo só aloca os recursos se todos os que ele precisam estão disponíveis
# Verificar se a alternativa (alocar o que dá e eventualmente executar quando tiver tudo que precisa) é melhor.

from process import Process
from multiprocessing import Lock, Value, Array

class ResourceManager:
    
    def __init__(self) -> None:
        
        # EDs que identificam quais processos estão na posse de quais recursos
        self.scanner_user =   -1
        self.printer_users = [-1,-1]
        self.modem_user =    -1
        self.SATA_users =    [-1,-1]
        
        # Único lock usado na alocação/liberação de dispositivos de E/S
        self.lock = Lock()


    # Retorna True se processo puder ser executado (processo em posse de todos os recursos necessários), e False se não.
    def allocate_resources(self, process: Process):
        
        # Primeiramente verifica se o processo é de tempo real (impossibilita de alocar recursos)
        if process.priority == 0:
            if process.scanner_req or process.printer_code_req or process.modem_req or process.disk_code:
                print("ERRO: O processo de PID " + str(process.PID) + " (de tempo real) tentou alocar recursos" )
                
                return False

        self.lock.acquire()     # Entra na região crítica
        
        return_value = False
        
        if self.verify_allocated_resources(process):
            #print("JÁ TEM")
            return_value = True
        elif self.try_get_resource(process):
            #print("NÃO TEM")
            return_value = True        
        
        #print("CHEGA AQUI")
        
        self.lock.release()     # Sai da região crítica

        return return_value
    
    def free_resources(self, process: Process):

        self.lock.acquire()     # Entra na região crítica
        
        if process.scanner_req and (self.scanner_user == process.PID):
            self.scanner_user = -1
        
        if process.modem_req and (self.modem_user == process.PID):
            self.modem_user = -1
        
        if process.printer_code_req:
            for i in range(len(self.printer_users)):
                if self.printer_users[i] == process.PID:
                    self.printer_users[i] = -1
            #print(self.printer_users)
        
        if process.disk_code:
            for i in range(len(self.SATA_users)):
                if self.SATA_users[i] == process.PID:
                    self.SATA_users[i] = -1
        
        # Notifica liberação de recursos caso o processo estivesse utilizando
        if process.scanner_req or process.modem_req or process.printer_code_req or process.disk_code:
            print("Processo de PID " + str(process.PID) + " Está liberando os seguintes reursos:")
            print(str(process.printer_code_req) + " impressoras")
            print(str(process.scanner_req) + " scanners")
            print(str(process.modem_req) + " modems")
            print(str(process.disk_code) + " dispositivos SATA\n")

        self.lock.release()     # Sai da região crítica

    # Tenta alocar recursos. Se conseguir, retorna True. Se não, False.
    def try_get_resource(self, process: Process) -> None:
        
        #print("Quantidade de impressoras necessárias: " + str(process.printer_code_req))

        # Verifica se os recursos que o processo precisa estão disponíveis
        if process.scanner_req and (self.scanner_user != -1):
            return False
        
        if process.modem_req and (self.modem_user != -1):
            return False
        
        count = 0
        for i in self.printer_users:
            if i == -1:
                count += 1
        if process.printer_code_req and (count < process.printer_code_req):
            return False
        
        count = 0
        for i in self.SATA_users:
            if i == -1:
                count += 1
        if process.disk_code and (count < process.disk_code):
            return False

        # Aloca recursos para o processo

        if process.scanner_req:
            self.scanner_user = process.PID

        
        if process.modem_req:
            self.modem_user = process.PID

        
        count = 0
        if process.printer_code_req:
            # Verifica quantidade de impressoras disponiveis
            for i in range(len(self.printer_users)):
                if self.printer_users[i] == -1:
                    count += 1
        # Se houver espaço disponivel, aloca no lugar devido
        if count >= process.printer_code_req:
            spaces_required = process.printer_code_req
            for i in range(len(self.printer_users)):
                if self.printer_users[i] == -1 and spaces_required:
                    self.printer_users[i] = process.PID
                    spaces_required -= 1

            #print("Estado atual da lista de utilizadoes das impressoras: " + str(self.printer_users))
            #print(self.printer_users)

        count = 0
        if process.disk_code:
            # Verifica quantidade de dispositivos SATA disponiveis
            for i in range(len(self.SATA_users)):
                if self.SATA_users[i] == -1:
                    count += 1
        if count >= process.disk_code:
            spaces_required = process.disk_code
            for i in range(len(self.SATA_users)):
                if self.SATA_users[i] == -1 and spaces_required:
                    self.SATA_users[i] = process.PID
                    spaces_required -= 1

        print("Processo de PID " + str(process.PID) + " Está alocando os seguintes reursos:")
        print(str(process.printer_code_req) + " impressoras")
        print(str(process.scanner_req) + " scanners")
        print(str(process.modem_req) + " modems")
        print(str(process.disk_code) + " dispositivos SATA\n")

        return True

    # Retorna True caso tenha tudo que precisa, e False se não.
    def verify_allocated_resources(self, process: Process):

        # Primeiro checa se processo precisa de QUALQUER recurso
        if process.scanner_req == 0 and process.printer_code_req == 0 and process.modem_req == 0 and process.disk_code == 0:            
            print("O processo de PID: " +str(process.PID) + " não precisa de nenhum dispositivo de E/S")
            return True
        # Se precisar de algum recurso, verifica se já os possui
        else:
            if process.scanner_req == 1:
                if self.scanner_user != process.PID:
                    return False
            
            if process.modem_req == 1:
                if self.modem_user != process.PID:
                    return False
            
            if process.printer_code_req > 0:
                count = 0
                for i in range(len(self.printer_users)):
                    if self.printer_users[i] == process.PID:
                        count += 1
                if count < process.printer_code_req:
                    return False
            
            if process.disk_code > 0:
                count = 0
                for i in range(len(self.SATA_users)):
                    if self.SATA_users[i] == process.PID:
                        count += 1
                if count < process.disk_code:
                    return False

            return True













