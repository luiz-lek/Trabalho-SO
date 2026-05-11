from processos import Processo, Processo_IO, ProcessoCPUBound, Status

QTD_FILAS_FEED_BACK = 3

class politica_FCFS:
    def __init__(self):
        self.fila = Fila()

    def adicionar_processo(self, processo: Processo) -> None:
        self.fila.adicionar_processo(processo)

    def despachar(self) -> Processo:
        if self.fila.esta_vazia():
            raise RuntimeError("Fila vazia. Não há processos para remover.")
        return self.fila.remover_processo()
    
class politica_feed_back:
    def __init__(self, qtd_filas: int):
        self.fila: list[Fila] = []
        for i in range(qtd_filas):
            self.fila.append(Fila())

    def despachar(self) -> Processo:
        if not self.fila[0].esta_vazia():
            return self.fila[0].remover_processo()
        if not self.fila[1].esta_vazia():
            return self.fila[1].remover_processo()
        if not self.fila[2].esta_vazia():
            return self.fila[2].remover_processo()
        raise RuntimeError("Todas as filas estão vazias. Não há processos para remover.")
        
    def adicionar_novo_processo(self, processo: Processo) -> None:
        self.adicioanr_processo(processo, 0)

    def reinserir_processo(self, processo: Processo) -> None:
        pass

class Fila:
    def __init__(self):
        self.fila: list[Processo_IO] = []

    def adicionar_processo(self, processo: Processo) -> None:
        self.fila.append(processo)

    def remover_processo(self) -> Processo:
        if not self.fila:
            raise RuntimeError("Fila vazia. Não há processos para remover.")
        return self.fila.pop(0)

    def esta_vazia(self) -> bool:
        return len(self.fila) == 0
    
class Despachante():
    def __init__(self):
        self._id_aual = -1
        self.fila_prioridade0 = politica_FCFS() # Cria uma instância da classe Fila para armazenar os processos que estão prontos para execução
        self.fila_prioridade1 = politica_feed_back(QTD_FILAS_FEED_BACK) # Cria uma instância da classe

    def gerar_id(self) -> int:
        self._id_aual += 1
        return self._id_aual

    def criar_novo_processo(self, tempo_fase1_cpu: int, tempo_fase_io: int, tempo_fase2_cpu: int, tam_MiB: int, prioridade: int) -> Processo:
        if tempo_fase1_cpu < 0 or tempo_fase2_cpu < 0 or tempo_fase_io < 0:
            raise ValueError("Tempos de CPU e E/S devem ser valores não negativos");
    
        id = self.gerar_id() 
    
        if(tempo_fase_io == 0):
            return ProcessoCPUBound(id, tempo_fase1_cpu + tempo_fase2_cpu, tam_MiB, prioridade)
        return Processo_IO(id, tempo_fase1_cpu, tempo_fase_io, tempo_fase2_cpu, tam_MiB, prioridade)