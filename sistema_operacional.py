import threading
import time

import escalonador
from leitura_processos import alistaProcessos
import memoria_principal
from processos import *
from escalonador import *
from cpu import *

class SistemaOperacional:

    def __init__(self, processos: list[Processo] | None = None) -> None:
        self.lock = threading.Lock()
        self.memoria_principal = MemoriaPrincipal()
        self.escalonador = Escalonador()
        self.despachante = Despachante()
        self.cpus: list[CPU] = [CPU(i) for i in range(4)]
        self.dma = DMA()
        self.logs: list[str] = []

        self.processos = alistaProcessos("entrada.txt", self.despachante)
        for processo in self.processos:
            self.escalonador.enfileirar_processo_novo(processo)
            self.tentar_admitir_processo_novo()

    def tick(self) -> dict:
        snapshot = {}
        
        processos_perderam_cpu: list[Processo] = list()

        for cpu in self.cpus:
            if cpu.estado == Estado.Vazio:
                processo = self.escalonador.selecionar_proximo_processo()
                if processo: # Garante que há processo antes de despachar
                    self.despachante.despachar(processo, cpu)
                    self.logs.append(f"🚀 CPU {cpu.id}: Processo {processo.id} começou a executar.")

            snapshot[cpu.id] = cpu.processo.id if cpu.processo else None

            processo_interrompido = cpu.clock()
            if processo_interrompido is not None:
                processos_perderam_cpu.append(processo_interrompido)

            print()

        for processo in processos_perderam_cpu:
            self.escalonador.tratar_retorno_cpu(processo)
            if processo.estado == EstadoProcesso.BLOQUEADO:
                self.dma.adicionar_processo(processo)
                self.logs.append(f"❌ Processo {processo.id} foi BLOQUEADO (solicitou I/O).")
            elif processo.estado == EstadoProcesso.FINALIZADO:
                self.memoria_principal.desalocar_processo(processo) # ◄--- FIX: Corrigido o "self,self."
                self.logs.append(f"🏁 Processo {processo.id} FINALIZOU e liberou memória.")
            else:
                self.logs.append(f"⏳ Processo {processo.id} sofreu preempção (Fim do Quantum).")

        cpus_interrompidas = list() 
        processos_desbloqueados = self.dma.clock()
        for processo_concluido in processos_desbloqueados:
            self.escalonador.desbloquer_processo(processo_concluido)
            self.logs.append(f"🔓 Processo {processo_concluido.id} concluiu I/O e voltou para PRONTO.")
            for cpu in self.cpus:
                if cpu.interrupcao_habilitada and not cpu in cpus_interrompidas:
                    cpus_interrompidas.append(cpu)

        self.tentar_admitir_processo_novo()
        print(f"\n{self.escalonador}\n")

        return snapshot

    def tentar_admitir_processo_novo(self) -> None:
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
            self.logs.append(f"📥 Processo {processo.id} ADMITIDO na memória (Tamanho: {processo.tam} MiB).")

    def adicionar_processo(self, tempo_fase1_cpu: int, tempo_fase_io: int, tempo_fase2_cpu: int, tam_MiB: int, qtd_discos: int, prioridade: int):
        processo = self.despachante.criar_processo(tempo_fase1_cpu, tempo_fase_io, tempo_fase2_cpu, tam_MiB, qtd_discos, prioridade)
        self.processos.append(processo)
        self.escalonador.enfileirar_processo_novo(processo)
        self.tentar_admitir_processo_novo()


    def tem_processos_pendentes(self) -> bool:
        cpus_ocupadas = any(cpu.estado == Estado.Ocupado for cpu in self.cpus)
        fila_tempo_real = len(self.escalonador.fila_processos_tempo_real.fila) > 0
        fila_usuario = any(len(f) > 0 for f in self.escalonador.fila_processos_usuario.fila)
        bloqueados = len(self.escalonador.bloqueados) > 0
        novos = len(self.escalonador.novos) > 0

        return cpus_ocupadas or fila_tempo_real or fila_usuario or bloqueados or novos 