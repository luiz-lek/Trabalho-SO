from enum import Enum
from abc import abstractmethod

class Status(Enum):
    NOVO = 0
    PRONTO = 1
    EXECUTANDO = 2
    BLOQUEADO = 3
    FINALIZADO = 4

class Processo:
    def __init__(self, id: int, tempo_fase1_cpu: int, tempo_fase_io: int, tempo_fase2_cpu: int, tam_MiB: int):
        self.id = id
    
        self.tempo_fase1_cpu = tempo_fase1_cpu
        self.tempo_restante_fase1_cpu = tempo_fase1_cpu
        
        self.tempo_fase2_cpu = tempo_fase2_cpu
        self.tempo_restante_fase2_cpu = tempo_fase2_cpu

        self.tempo_fase_io = tempo_fase_io
        self.tempo_restante_fase_io = tempo_fase_io

        self.pcb = PCB(id)
        self.tam = tam_MiB

        self.fase1_cpu = True
        self.fase_io = False
        self.fase2_cpu = False
        

    @abstractmethod
    def atualizar_tempo_restante(self) -> None:
        if(self.pcb.status == Status.NOVO):
            self.pcb.atualizar_status(Status.PRONTO)
    
        if self.fase1_cpu:
            try:
                self._atualizar_tempo_restante_fase1_cpu()
            except RuntimeError as e:
                print(f"Erro ao atualizar tempo restante na fase 1 de CPU: {e}")
            return
        
        if self.fase_io:
            try:
                self._atualizar_tempo_restante_fase_io()
            except RuntimeError as e:
                print(f"Erro ao atualizar tempo restante na fase de E/S: {e}")
            return
        
        if self.fase2_cpu:
            try:
                self._atualizar_tempo_restante_fase2_cpu()
            except RuntimeError as e:
                print(f"Erro ao atualizar tempo restante na fase 2 de CPU: {e}")
            return
        
        raise RuntimeError("Processo já finalizou a execução.")

    def _atualizar_tempo_restante_fase1_cpu(self) -> None:
        if not self.fase1_cpu:
            raise RuntimeError("Processo não está na fase 1 de CPU.")
        
        self.tempo_restante_fase1_cpu -= 1
        if self.tempo_restante_fase1_cpu <= 0:
            self.fase1_cpu = False
            self.fase_io = True
            self.pcb.atualizar_status(Status.BLOQUEADO)
            print(f"Processo {self.pcb.id} passou para a fase de E/S e foi bloqueado.")

    def _atualizar_tempo_restante_fase_io(self) -> None:
        if not self.fase_io:
            raise RuntimeError("Processo não está na fase de E/S.")
        
        self.tempo_restante_fase_io -= 1
        if self.tempo_restante_fase_io <= 0:
            self.fase_io = False
            self.fase2_cpu = True
            self.pcb.atualizar_status(Status.PRONTO)
            print(f"Processo {self.pcb.id} passou para a fase 2 de CPU e está pronto para execução.")

    def _atualizar_tempo_restante_fase2_cpu(self) -> None:
        if not self.fase2_cpu:
            raise RuntimeError("Processo não está na fase 2 de CPU.")
        
        self.tempo_restante_fase2_cpu -= 1
        if self.tempo_restante_fase2_cpu <= 0:
            self.fase2_cpu = False
            self.pcb.atualizar_status(Status.FINALIZADO)
            print(f"Processo {self.pcb.id} finalizou a execução.")

    def __str__(self) -> str:
        return (f"Processo: {self.pcb.id}" 
                f"\n\tFase 1 CPU restante: {self.tempo_restante_fase1_cpu}"
                f"\n\tFase I/O restante: {self.tempo_restante_fase_io}"
                f"\n\tFase 2 CPU restante: {self.tempo_restante_fase2_cpu}"
                f"\n\tStatus: {self.pcb.status.name}"
                f"\n\tTamanho: {self.tam} MiB")

class ProcessoCPUBound(Processo):
    def __init__(self, id: int, tempo_cpu: int, tam_MiB: int):
        if tam_MiB > 512: #tamanho em MiB
            raise ValueError("Tamanho do processo excede o limite de 512 MiB");
    
        try:
            super().__init__(id, tempo_cpu, 0, 0, tam_MiB)
        except ValueError as e:
            print(f"Erro ao criar processo CPU-bound: {e}")
            raise
        

        self.tempo1_cpu = tempo_cpu

    def atualizar_tempo_restante(self) -> None:
        if(self.pcb.status == Status.NOVO):
            self.pcb.atualizar_status(Status.PRONTO)

        if not self.fase1_cpu:
            raise RuntimeError("\nProcesso CPU-bound já finalizado.")
        
        self.tempo_restante_fase1_cpu -= 1
        if self.tempo_restante_fase1_cpu <= 0:
            self.fase1_cpu = False
            self.pcb.atualizar_status(Status.FINALIZADO)
            print(f"\nProcesso CPU-bound {self.pcb.id} finalizou a execução.\n")
    
class CriadorProcessos:
    def __init__(self):
        self._id_aual = -1

    def criar(self, tempo_fase1_cpu: int, tempo_fase_io: int, tempo_fase2_cpu: int, tam_MiB: int) -> Processo:
        if tempo_fase1_cpu < 0 or tempo_fase2_cpu < 0 or tempo_fase_io < 0:
            raise ValueError("Tempos de CPU e E/S devem ser valores não negativos");
    
        id = self.gerar_id() 
    
        if(tempo_fase_io == 0):
            return ProcessoCPUBound(id, tempo_fase1_cpu + tempo_fase2_cpu, tam_MiB)
        return Processo(id, tempo_fase1_cpu, tempo_fase_io, tempo_fase2_cpu, tam_MiB)
    
    def gerar_id(self) -> int:
        self._id_aual += 1
        return self._id_aual
    
class PCB: #bloco com infos de controle de um processo
    def __init__(self, id: int):
        self.id = id
        self.status = Status.NOVO

    def atualizar_status(self, novo_status: int) -> None:
        self.status = novo_status