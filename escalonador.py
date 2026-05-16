from processos import *

QTD_FILAS_FEED_BACK = 3

class politica_FCFS:
    def __init__(self):
        self.fila = Fila()

    def adicionar_processo(self, processo: Processo) -> None:
        self.fila.adicionar_processo(processo)

    def retirar_processo(self) -> Processo:
        if self.fila.esta_vazia():
            return None
        return self.fila.remover_processo()
    
    def esta_vazia(self) -> bool:
        return self.fila.esta_vazia()
    
class politica_feed_back:
    def __init__(self, qtd_filas: int):
        self.fila: list[Fila] = []
        self.qtd_filas = qtd_filas

        for i in range(self.qtd_filas):
            fila_i = Fila()
            self.fila.append(fila_i)

    def retirar_processo(self) -> Processo: # Retorna o processo e o indice da fila de onde foi retirado.
        for i in range(self.qtd_filas):
            if not self.fila[i].esta_vazia():
                processo = self.fila[i].remover_processo()
                processo.pcb.ultima_fila = i
                return processo
        return None
    
    def filas_estao_vazias(self) -> bool:
        for i in range(self.qtd_filas):
            if not self.fila[i].esta_vazia():
                return False
        return True
        
    def adicionar_novo_processo(self, processo: Processo) -> None: # Processos novos sempre entram na fila 0.
        self.fila[0].adicionar_processo(processo)

    def reinserir_processo_despachado(self, processo: Processo) -> None:
        ultima_fila = processo.pcb.ultima_fila
        if(ultima_fila == self.qtd_filas - 1):
            self.fila[ultima_fila].adicionar_processo(processo)
            return
        self.fila[ultima_fila + 1].adicionar_processo(processo)

class Fila:
    def __init__(self):
        self.fila: list[Processo] = []

    def adicionar_processo(self, processo: Processo) -> None:
        self.fila.append(processo)

    def remover_processo(self) -> Processo:
        if not self.esta_vazia():
            return None
        return self.fila.pop(0)

    def esta_vazia(self) -> bool:
        return len(self.fila) == 0
    
class Escalonador:
    def __init__(self, memoria): # Adicionar o tipo da memória assim que implementado.
        self.despachante = Despachante(self)

        self.fila_novo = Fila()
        self.fila_prioridade0 = politica_FCFS()
        self.fila_prioridade1 = politica_feed_back(QTD_FILAS_FEED_BACK)

    def adicionar_novo_processo(self, tempo_fase1_cpu: int, tempo_fase_io: int, tempo_fase2_cpu: int, tam_MiB: int, prioridade: int) -> None:
        processo: Processo = self.despachante.criar_processo(tempo_fase1_cpu, tempo_fase_io, tempo_fase2_cpu, tam_MiB, prioridade)

        # Adicionar verificação de memória disponível aqui, para decidir se o processo vai pra fila de prontos ou pra fila de novos e esperar memória.
        if processo.pcb.prioridade == 0:
            self.fila_prioridade0.adicionar_processo(processo)
            return
        self.fila_prioridade1.adicionar_novo_processo(processo)

    def admitir_processo(self) -> None:
        if self.fila_novo.esta_vazia():
            raise RuntimeError("Não há processos para admitir.")
        
    def reinserir_processo_apos_quantum(self, processo: Processo) -> None:
        processo.pcb.Status = Status.PRONTO
        if processo.pcb.prioridade == 0:
            raise RuntimeError("Processos de prioridade 0 não devem ser reinseridos após quantum, pois são executados de forma contínua.")
        self.fila_prioridade1.reinserir_processo_despachado(processo)   

class Despachante():
    def __init__(self, escalonador: Escalonador):
        self.escalonador = escalonador
        self._id_aual = -1

    def _gerar_id(self) -> int: # Gera id de forma incremental.
        self._id_aual += 1
        return self._id_aual

    def criar_processo(self, tempo_fase1_cpu: int, tempo_fase_io: int, tempo_fase2_cpu: int, tam_MiB: int, prioridade: int) -> Processo:
        if tempo_fase1_cpu < 0 or tempo_fase2_cpu < 0 or tempo_fase_io < 0:
            raise ValueError("Tempos de CPU e E/S devem ser valores não negativos");
    
        id = self._gerar_id() 
    
        if(tempo_fase_io == 0): # Se o processo não tem fase de E/S, ele é CPU-bound e pode ser tratado como um processo único de CPU.
            return ProcessoCPUBound(id, tempo_fase1_cpu + tempo_fase2_cpu, tam_MiB, prioridade)
        return ProcessoIO(id, tempo_fase1_cpu, tempo_fase_io, tempo_fase2_cpu, tam_MiB, prioridade)
    
    def despachar(self) -> Processo: # Dá prioridade para processos da fila0, que tem prioridade 0.
        if not self.escalonador.fila_prioridade0.esta_vazia():
            return self.escalonador.fila_prioridade0.retirar_processo()
        return self.escalonador.fila_prioridade1.retirar_processo()