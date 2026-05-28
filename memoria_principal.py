from processos import *

class MemoriaPrincipal:
    def __init__(self):
        # Lista de alocação (0 para vazio e 1 para alocado)
        self.alocacao = [0] * 32000

        # Lista de processos
        self.processos = []

    def aloca(self, p: Processo) -> None:
        # Verificando se há espaço suficiente para alocar o processo
        for i in range(len(self.alocacao)):
            if self.alocacao[i] == 0: # Encontrou um espaço vazio
                if i + p.tam <= len(self.alocacao): # Verifica se o processo cabe no espaço vazio restante
                    
                    # Faz a alocação do processo na memória
                    for j in range(i, i + p.tam):
                        self.alocacao[j] = 1

                    self.processos.append(p) # Adiciona o processo à lista de processos alocados
                    print(f"Processo {p.pcb.id} alocado na memória.")
                    p.pcb.pos_memoria = i
                    return
                
        print(f"Não há espaço suficiente para alocar o processo {p.pcb.id}.")

    def desaloca(self, p: Processo):
        if p not in self.processos:
            print(f"Processo {p.pcb.id} não encontrado na memória.")
            return
        
        # Desaloca o processo da memória marcando o intervalo como vazio (0)
        fim_intervalo = p.pcb.pos_meoria + p.tam + 1
        for i in range(p.pcb.pos_memoria, fim_intervalo):
            self.alocacao[i] = 0
        
        self.processos.remove(p) # Remove o processo da lista de processos alocados
        print(f"Processo {p.pcb.id} desalocado da memória do intervalo correspondente")