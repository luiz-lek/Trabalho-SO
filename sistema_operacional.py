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
        self.lock = threading.Lock()
        self.memoria_principal = MemoriaPrincipal()
        self.escalonador = Escalonador()
        self.despachante = Despachante()
        self.cpus: list[CPU] = [CPU(i) for i in range(4)]
        self.dma = DMA()

        self.processos = processos if processos is not None else []

        processos_lidos = alistaProcessos("entrada.txt", self.despachante)
        for processo in processos_lidos:
            self.processos.append(processo)
            self.escalonador.enfileirar_processo_novo(processo)

    def tick(self) -> dict:
        snapshot = {}
        
        processos_perderam_cpu: list[Processo] = list()

        for cpu in self.cpus:
            if cpu.estado == Estado.Vazio:
                processo = self.escalonador.selecionar_proximo_processo()
                self.despachante.despachar(processo, cpu)

            snapshot[cpu.id] = cpu.processo.id if cpu.processo else None

            processo_interrompido = cpu.clock()
            if processo_interrompido is not None:
                processos_perderam_cpu.append(processo_interrompido)
            print()

        for processo in processos_perderam_cpu:
            self.escalonador.tratar_retorno_cpu(processo)
            if processo.estado == EstadoProcesso.BLOQUEADO:
                self.dma.adicionar_processo(processo) 

        processos_desbloqueados = self.dma.clock()
        for processo_concluido in processos_desbloqueados:
            self.escalonador.desbloquer_processo(processo_concluido)

        self.tentar_admitir_processo_novo()
        print(f"\n{self.escalonador}\n")

        return snapshot

    def tentar_admitir_processo_novo(self) -> None:
        '''        
            O loop percorre toda a fila de novos e checa se tem memória praca cada processo.
            Para assim que não tiver mais processo ou a não tiver memória disponível (Não tenta alocar todos)
            Processos muito grande são penalizados indo para o fim da fila de novos.
        '''
        while 1 < 2:
            processo = self.escalonador.retirar_proximo_novo()
            if processo is None:
                break

            pos_inicio: int | None = self.memoria_principal.verificar_bloco_disponivel(processo.tam)
            if pos_inicio is None:
                self.escalonador.enfileirar_processo_novo(processo)
                return
            
            self.memoria_principal.alocar_processo(pos_inicio, processo)
            self.escalonador.admitir_processo(processo)

    def tem_processos_pendentes(self) -> bool:
        cpus_ocupadas = any(cpu.estado == Estado.Ocupado for cpu in self.cpus)
        fila_tempo_real = len(self.escalonador.fila_processos_tempo_real.fila) > 0
        fila_usuario = any(len(f) > 0 for f in self.escalonador.fila_processos_usuario.fila)
        bloqueados = len(self.escalonador.bloqueados) > 0
        return cpus_ocupadas or fila_tempo_real or fila_usuario or bloqueados