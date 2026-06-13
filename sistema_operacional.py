import threading
import time

import escalonador
from leitura_processos import alistaProcessos
import memoria_principal
from processos import *
from escalonador import *
from cpu import *

class SistemaOperaciona:

    def __init__(self, processos: list[Processo] | None = None) -> None:
        # Todos os componentes do sistema operacional.
        self.lock = threading.Lock() # Lock para sincronizar o acesso à lista de processos entre o sistema operacional e a GUI.
        self.memoria_principal = MemoriaPrincipal()
        self.escalonador = Escalonador(self.memoria_principal)
        self.despachante = Despachante()
        self.cpus: list[CPU] = [CPU(i) for i in range(4)]
        self.dma = DMA()

        self.processos = processos if processos is not None else [] #pra guardar a referência da lista de processos, caso seja passada como argumento, para que a GUI possa acessar os processos do sistema operacional.

        processos_lidos = alistaProcessos("entrada.txt", self.despachante)
        for processo in processos_lidos:
            self.processos.append(processo) #Popula a lista
            self.escalonador.escalonar_processo_novo(processo)

    def executar(self) -> None:
        for i in range(20):
            print(f"\n--- Tique {i} ---")
            self.clock_cpus()
            processos_desbloqueados = self.dma.clock()
            for processo_concluido in processos_desbloqueados:
                self.escalonador.escalonar_processo_bloqueado(processo_concluido.id)

    

    def clock_cpus(self) -> None:
        '''
        Como o programa é sequencial, não podemos por um processo que acabou de sair da cpu direto no escalonador
        pois corremos o risco de um processo sair da cpu 0, por exemplo e ganhar cpu de novo se a cpu 1 tiver 
        livre, ganhar cpu de novo no mesmo clock.
        '''
        processos_perderam_cpu: list[Processo] = list()

        # Gera um pulso de cock nas 4 cpus
        for cpu in self.cpus:
            # Escalona um novo processo se ela estiver livre
            if cpu.estado == Estado.Vazio:
                processo = self.escalonador.escalonar_processo_para_execucao()
                self.despachante.despachar(processo, cpu)

            # Escalona se o processo executado na cpu foi desalocado.
            processo_interrompido: Processo | None = cpu.clock()
            if processo_interrompido is not None:
                processos_perderam_cpu.append(processo_interrompido)
            print()

        for processo in processos_perderam_cpu:
            self.escalonador.escalonar_processo_interrompido(processo)

        time.sleep(0.5)