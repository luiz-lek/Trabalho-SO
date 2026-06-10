from processos import *
from cpu import CPU
from queue import Queue
from memoria_principal import MemoriaPrincipal

QTD_FILAS_FEED_BACK = 3

class politica_FCFS:

    def __init__(self):
        self.fila = Queue()

    def adicionar_processo(self, processo: Processo) -> None:
        self.fila.put(processo)

    def retirar_processo(self) -> Processo:
        if self.fila.empty():
            return None
        return self.fila.get()
    
class politica_feed_back:

    def __init__(self, qtd_filas: int):
        self.fila: list[Queue] = []
        self.qtd_filas = qtd_filas

        for i in range(self.qtd_filas):
            fila_i = Queue()
            self.fila.append(fila_i)

    def retirar_processo(self) -> Processo: # Retorna o processo
        for i in range(self.qtd_filas):
            if not self.fila[i].empty():
                processo = self.fila[i].get()
                processo.pcb.ultima_fila = i
                return processo
            
        return None
        
    def adicionar_novo_processo(self, processo: Processo) -> None: # Processos novos sempre entram na fila 0.
        self.fila[0].put(processo)

    def reinserir_processo_despachado(self, processo: Processo) -> None: # Insere um processo que perdeu cpu na fila seguinte. 
        ultima_fila = processo.pcb.ultima_fila                           # Se estava na última fila antes de ser despachado, ele permanece nela.
        if(ultima_fila == self.qtd_filas - 1):
            self.fila[ultima_fila].put(processo)
            return
        self.fila[ultima_fila + 1].put(processo)
    
class Escalonador:
    
    def __init__(self, memoria_principal: MemoriaPrincipal): # Adicionar o tipo da memória assim que implementado.
        self.novos = Queue()
        self.finalizados: list[Processo] = list()
        self.bloqueados: list[Processo] = list()
        self.prioridade0 = politica_FCFS()
        self.prioridade1 = politica_feed_back(QTD_FILAS_FEED_BACK)

        self.memoria_principal = memoria_principal

    def inserir_processo_novo(self, processo: Processo) -> None:
        # Adicionar verificação de memória disponível aqui, para decidir se o processo vai pra fila de prontos ou pra fila de novos e esperar memória.

        if processo.pcb.prioridade == 0:
            self.prioridade0.adicionar_processo(processo)
            return
        self.prioridade1.adicionar_novo_processo(processo)

    def selecionar_processo_para_execucao(self) -> Processo:
        processo = self.prioridade0.retirar_processo()
        if processo is not None:
            return processo
        return self.prioridade1.retirar_processo()
    
    def admitir_processo(self) -> None:
        if self.novos.esta_vazia():
            return
        
        processo = self.novos.get();
        if processo is not None:
            self.inserir_processo_novo(processo);
        
    def inserir_processo_interrompido(self, processo: Processo) -> None:
        if processo.pcb.status == Status.EXECUTANDO: # O porcesso foi interrompido por quantum, 
            processo.pcb.status = Status.PRONTO # então ele deve ser reinserido na fila de prontos.
            self.prioridade1.reinserir_processo_despachado(processo)

        elif processo.pcb.status == Status.BLOQUEADO: # O processo foi bloqueado por E/S, 
            self.bloqueados.append(processo) # então ele deve ser reinserido na lista de bloqueados.
        
        elif processo.pcb.status == Status.FINALIZADO: # O processo finalizou a execução, 
            self.finalizados.append(processo) # então ele não deve ser inserido na lista de finalizados.


class Despachante():

    def __init__(self):
        self._id_atual = -1

    def _gerar_id(self) -> int: # Gera id de forma incremental.
        self._id_atual += 1
        return self._id_atual

    def criar_processo(self, tempo_fase1_cpu: int, tempo_fase_io: int, tempo_fase2_cpu: int, tam_MiB: int, prioridade: int) -> Processo:
        if tempo_fase1_cpu < 0 or tempo_fase2_cpu < 0 or tempo_fase_io < 0:
            raise ValueError("Tempos de CPU e E/S devem ser valores não negativos");
    
        id = self._gerar_id() 
    
        if tempo_fase_io == 0: # Se o processo não tem fase de E/S, ele é CPU-bound e pode ser tratado como um processo único de CPU.
            return ProcessoCPUBound(id, tempo_fase1_cpu + tempo_fase2_cpu, tam_MiB, prioridade)
        return ProcessoIO(id, tempo_fase1_cpu, tempo_fase_io, tempo_fase2_cpu, tam_MiB, prioridade)
    
    def despachar(self, processo: Processo) -> Processo: # Dá prioridade para processos da fila0, que tem prioridade 0.
        if processo is not None:
            processo.pcb.status = Status.EXECUTANDO
        return processo