from processos import *
from cpu import *
from queue import Queue
from memoria_principal import MemoriaPrincipal

QTD_FILAS_FEED_BACK = 3

class politica_FCFS:

    def __init__(self):
        self.fila: list[Processo] = list()

    def adicionar_processo(self, processo: Processo) -> None:
        self.fila.append(processo)

    def retirar_processo(self) -> Processo:
        if len(self.fila) == 0:
            return None
        return self.fila.pop(0)
    
class politica_feed_back:

    def __init__(self, qtd_filas: int):
        self.fila: list[list[Processo]] = list()
        self.qtd_filas = qtd_filas

        for i in range(self.qtd_filas):
            fila_i = list()
            self.fila.append(fila_i)

    def retirar_processo(self) -> Processo: # Retorna o processo
        for i in range(self.qtd_filas):
            if len(self.fila[i]) != 0:
                processo = self.fila[i].pop(0)
                processo.ultima_fila = i
                return processo
            
        return None
        
    def adicionar_novo_processo(self, processo: Processo) -> None: # Processos novos sempre entram na fila 0.
        self.fila[0].append(processo)

    def reinserir_processo_despachado(self, processo: Processo) -> None: # Insere um processo que perdeu cpu na fila seguinte. 
        ultima_fila = processo.ultima_fila                           # Se estava na última fila antes de ser despachado, ele permanece nela.
        if(ultima_fila == self.qtd_filas - 1):
            self.fila[ultima_fila].append(processo)
            return
        self.fila[ultima_fila + 1].append(processo)
    
class Escalonador:
    
    def __init__(self): # Adicionar o tipo da memória assim que implementado.
        self.novos: list[Processo] = list()
        self.finalizados: list[Processo] = list()
        self.bloqueados: list[Processo] = list()
        self.fila_processos_tempo_real = politica_FCFS()
        self.fila_processos_usuario = politica_feed_back(QTD_FILAS_FEED_BACK)

    def admitir_processo(self, processo: Processo) -> None:
        if processo.prioridade == 0:
            self.fila_processos_tempo_real.adicionar_processo(processo)
            return
        self.fila_processos_usuario.adicionar_novo_processo(processo)

    def enfileirar_processo_novo(self, processo: Processo) -> None:
        self.novos.append(processo)

    def retirar_proximo_novo(self) -> Processo | None:
        if len(self.novos) == 0:
            return None
        return self.novos.pop(0)
        
    def selecionar_proximo_processo(self) -> Processo:
        processo = self.fila_processos_tempo_real.retirar_processo()
        if processo is not None:
            return processo
        return self.fila_processos_usuario.retirar_processo()
        
    def tratar_retorno_cpu(self, processo: Processo) -> None:
        if processo.estado == EstadoProcesso.PRONTO: # então ele deve ser reinserido na fila de prontos.
            self.fila_processos_usuario.reinserir_processo_despachado(processo)

        elif processo.estado == EstadoProcesso.BLOQUEADO: # O processo foi bloqueado por E/S, 
            self.bloqueados.append(processo) # então ele deve ser reinserido na lista de bloqueados.
        
        elif processo.estado == EstadoProcesso.FINALIZADO: # O processo finalizou a execução, 
            self.finalizados.append(processo) # então ele não deve ser inserido na lista de finalizados.

    def desbloquer_processo(self, processo: Processo):
        # Desbloqueia processo que terminou I/O
        self.bloqueados.remove(processo)
        self.fila_processos_usuario.adicionar_novo_processo(processo)

    def __str__(self) -> str:
        # Pega os IDs diretamente iterando pelas listas
        ids_novos = [p.id for p in self.novos]
        ids_bloqueados = [p.id for p in self.bloqueados]
        ids_finalizados = [p.id for p in self.finalizados]

        # Fila do FCFS
        ids_tempo_real = [p.id for p in self.fila_processos_tempo_real.fila]

        # Monta a representação das filas de usuário (Feed-back)
        filas_usuario_str = ""
        for i in range(self.fila_processos_usuario.qtd_filas):
            ids_na_fila = [p.id for p in self.fila_processos_usuario.fila[i]]
            filas_usuario_str += f"\n\tFila {i}: {ids_na_fila}"

        return (f"--- Estado do Escalonador ---"
                f"\nNovos: {ids_novos}"
                f"\nProntos (Tempo Real)\n\tFila: {ids_tempo_real}"
                f"\nProntos (Usuário): {filas_usuario_str}"
                f"\nBloqueados: {ids_bloqueados}"
                f"\nFinalizados: {ids_finalizados}"
                f"\n-----------------------------")


class Despachante():

    def __init__(self):
        self._id_atual = -1

    def _gerar_id(self) -> int: # Gera id de forma incremental.
        self._id_atual += 1
        return self._id_atual

    def criar_processo(self, tempo_fase1_cpu: int, tempo_fase_io: int, tempo_fase2_cpu: int, tam_MiB: int, qtd_discos: int, prioridade: int) -> Processo:
        if tempo_fase1_cpu < 0 or tempo_fase2_cpu < 0 or tempo_fase_io < 0:
            raise ValueError("Tempos de CPU e E/S devem ser valores não negativos");
    
        id = self._gerar_id() 
    
        if tempo_fase_io == 0: # Se o processo não tem fase de E/S, ele é CPU-bound e pode ser tratado como um processo único de CPU.
            return ProcessoCPUBound(id, tempo_fase1_cpu + tempo_fase2_cpu, tam_MiB, prioridade)
        return ProcessoIO(id, tempo_fase1_cpu, tempo_fase_io, tempo_fase2_cpu, tam_MiB, qtd_discos, prioridade)
    
    def despachar(self, processo: Processo, cpu: CPU) -> Processo:
        if processo is not None:
            cpu.alocar_processo(processo)
        return processo