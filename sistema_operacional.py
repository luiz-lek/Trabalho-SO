import time

import escalonador
from leitura_processos import alistaProcessos
import memoria_principal
from processos import *
from escalonador import *
from cpu import *

class SistemaOperaciona:

    def __init__(self):
        # Todos os componentes do sistema operacional.
        self.memoria_principal = MemoriaPrincipal()
        self.escalonador = Escalonador()
        self.despachante = Despachante()
        self.cpus: list[CPU] = [CPU(i) for i in range(4)]
        self.dma = DMA()

        processos = alistaProcessos("entrada.txt", self.despachante)
        for processo in processos:
            self.escalonador.enfileirar_processo_novo(processo)

    def executar(self) -> None:
        self.clock_cpus()
        processos_desbloqueados: list[ProcessoIO] | None = self.dma.clock()
        for processo_concluido in processos_desbloqueados:
            self.escalonador.desbloquer_processo(processo_concluido)
        print(f"\n{self.escalonador}\n")

    def clock_cpus(self) -> None:
        '''
            Como o programa é sequencial, não podemos por um processo que acabou de sair da cpu direto no escalonador
            pois corremos o risco de um processo sair da cpu 0, por exemplo e ganhar cpu de novo se a cpu 1 tiver 
            livre, ganhar cpu de novo no mesmo clock.
        '''
        processos_perderam_cpu: list[Processo] = list()

        # Gera um pulso de clock nas 4 cpus
        for cpu in self.cpus:
            # Seleciona um novo processo se ela estiver livre
            if cpu.estado == Estado.Vazio:
                processo = self.escalonador.selecionar_proximo_processo()
                self.despachante.despachar(processo, cpu)

            # Insere na lista se o processo executado na cpu foi desalocado.
            processo_interrompido: Processo | None = cpu.clock()
            if processo_interrompido is not None:
                processos_perderam_cpu.append(processo_interrompido)
            print()

        # O escalonador insere na devida fila todos os processos que perderam cpu
        for processo in processos_perderam_cpu:
            self.escalonador.tratar_retorno_cpu(processo)

            if processo.estado == EstadoProcesso.BLOQUEADO:
                self.dma.adicionar_processo(processo)

            elif processo.estado == EstadoProcesso.FINALIZADO:
                self.memoria_principal.desalocar_processo(processo)

        self.tentar_admitir_processo_novo()

        time.sleep(1)

    def tentar_admitir_processo_novo(self) -> None:
        while 1 < 2:
            processo = self.escalonador.retirar_proximo_novo()
            if processo is None:
                break

            tem_memoria: int | None = self.memoria_principal.verificar_bloco_disponivel(processo.tam)
            if tem_memoria is None:
                self.escalonador.enfileirar_processo_novo(processo)
                return
            
            self.memoria_principal.alocar_processo(tem_memoria, processo)
            self.escalonador.admitir_processo(processo)