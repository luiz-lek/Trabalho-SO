from processos import *

class MemoriaPrincipal:
    def __init__(self):
        # Lista de alocação (0 para vazio e 1 para alocado)
        self.tam_memoria = 32000
        self.alocacao = [None] * self.tam_memoria

    
    def alocar_processo(self, inicio: int, processo: Processo):
        if inicio + processo.tam > len(self.alocacao):
            raise IndexError("A alocação estora o limite do vetor")
        
        for i in range(inicio, inicio + processo.tam):
            self.alocacao[i] = processo.id

    def desalocar_processo(self, processo: Processo):
        for i in range(self.tam_memoria):
            if self.alocacao[i] == processo.id:
                j = i
                while j < self.tam_memoria and self.alocacao[j] == processo.id:
                    self.alocacao[j] = None
                    j+=1
                break

    def verificar_bloco_disponivel(self, tam_bloco: int) -> int:
        i = 0
        tam_mem = len(self.alocacao)
        
        while i <= tam_mem - tam_bloco:
            bloco_livre = True
            
            for j in range(tam_bloco):
                if self.alocacao[i + j] != None:
                    bloco_livre = False
                    
                    i = i + j + 1
                    break
            
            if bloco_livre:
                return i
                
        return None
