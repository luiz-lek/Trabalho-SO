from processos import *
from escalonador import *
from cpu import *

class SistemaOperaciona:

    def __init__(self, processos: list[Processo]):
        self.memoria = MemoriaPrincipal()
        self.escalonador = Escalonador(self.memoria)
        self.despachante = Despachante()

        self.cpus: list[CPU]
        for i in range(4):
            self.cpus[i].append(CPU())

        self.dma = DMA()

        for processo in processos:
            self.escalonador.inserir_processo_novo(processo)

    def executar_unidade_tempo(self) -> None:
        interrupcao: list[ProcessoIO] = None
        for cpu in self.cpus:
            cpu.clock()
            interrupcao = self.dma.clock()
            for processoIO in interrupcao:
                self.escalonador.desbloquear_processo(processoIO.id)