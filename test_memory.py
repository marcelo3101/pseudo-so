from memory_manager import MemoryManager
from process import Process


"""
Apenas um arquivo para testar as funções da classe MemoryManager


<tempo de inicialização>, <prioridade>, <tempo de processador>, <blocos em memória>, <número-código da impressora requisitada>,
<requisição do scanner>, <requisição do modem>, <número-código do disco>
"""

memory_manager = MemoryManager()

process1 = Process("2, 1, 3, 128, 0, 0, 0, 0")

process2 = Process("2, 1, 3, 64, 0, 0, 0, 0")

process3 = Process("2, 0, 3, 64, 0, 0, 0, 0")


memory_manager.allocate(process1)
memory_manager.allocate(process2)
memory_manager.free(process1)
memory_manager.free(process1)
memory_manager.allocate(process3)
print(memory_manager.memory[0:64])
print(memory_manager.memory[64:])

