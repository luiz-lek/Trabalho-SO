import Processos.Processo as Processo
from typing import override

class ProcessoCPUBound(Processo):
    def __init__(self, id: int, tempo_cpu: int, tam: int):
        if tam > 512: #tamanho em MiB
            raise ValueError("Tamanho do processo excede o limite de 512 MiB");
    
        try:
            super().__init__(id, tempo_cpu, 0, 0, tam)
        except ValueError as e:
            print(f"Erro ao criar processo CPU-bound: {e}")
            raise
        

        self.tempo1_cpu = tempo_cpu
        self.tam = tam