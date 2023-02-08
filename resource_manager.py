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
            return_value = True
        elif self.try_get_resource(process):
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
            for i in self.printer_users:
                if i == process.PID:
                    i = -1
                    break
        
        if process.disk_code:
            for i in self.SATA_users:
                if i == process.PID:
                    i = -1
                    break
        
        self.lock.release()     # Sai da região crítica

    # Tenta alocar recursos. Se conseguir, retorna True. Se não, False.
    def try_get_resource(self, process: Process) -> None:
        
        # Verifica se os recursos que o processo precisa estão disponíveis
        if process.scanner_req and (self.scanner_user != -1):
            print("BABY BABY BABY")
            print(self.scanner_user)
            return False
        
        if process.modem_req and (self.modem_user != -1):
            return False
        
        count = 0
        for i in self.printer_users:
            if i == -1:
                count += 1
        if process.printer_code_req and count == 0:
            return False
        
        count = 0
        for i in self.SATA_users:
            if i == -1:
                count += 1
        if process.disk_code and count == 0:
            return False


        # Aloca recursos para o processo
        if process.scanner_req:
            self.scanner_user = process.PID
        
        if process.modem_req:
            self.modem_user = process.PID
        
        if process.printer_code_req:
            for i in self.printer_users:
                if i == -1:
                    i = process.PID
                    break
        
        if process.disk_code:
            for i in self.SATA_users:
                if i == -1:
                    i = process.PID
                    break
    
        return True

    # Retorna True caso tenha tudo que precisa, e False se não.
    def verify_allocated_resources(self, process: Process):

        # Primeiro checa se processo precisa de QUALQUER recurso
        if process.scanner_req == 0 and process.printer_code_req == 0 and process.modem_req == 0 and process.disk_code == 0:            
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
                for i in self.printer_users:
                    if i == process.PID:
                        count = 1
                if count == 0:
                    return False
            
            if process.disk_code > 0:
                count = 0
                for i in self.SATA_users:
                    if i == process.PID:
                        count = 1
                if count == 0:
                    return False

            return True













