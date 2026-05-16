from enum import Enum
from typing import Optional
from processos import Processo

class Estado(Enum):
    Vazio = 0
    Ocupado = 1


class CPU:
    def __init__(self, id: int):
        self.id = id
        self.processo: Optional[Processo] = None
        self.unid_temp = 0
        self.estado = Estado.Vazio

    def alocar_processo(self, processo: Processo):
        self.processo = processo
        self.estado = Estado.Ocupado

    def desalocar_processo(self):
        self.processo = None
        self.estado = Estado.Vazio

    def temp_CPU(self):
        if self.processo is None:
            return
        self.unid_temp += 1
        if getattr(self.processo, "tempo_restante_fase1_cpu", 0) != 0:
            self.processo.tempo_restante_fase1_cpu -= 1
        elif getattr(self.processo, "tempo_restante_fase_io", 0) != 0:
            self.processo.tempo_restante_fase_io -= 1
        elif getattr(self.processo, "tempo_restante_fase2_cpu", 0) != 0:
            self.processo.tempo_restante_fase2_cpu -= 1
        else:
            self.desalocar_processo()

    def quantum(self):
        pass

    def __str__(self) -> str:
        if self.processo is None:
            return "CPU está Ociosa"
        return (f"Processo: {self.processo.pcb.id}"
                f"\n\tFase 1 CPU restante: {self.processo.tempo_restante_fase1_cpu}"
                f"\n\tFase I/O restante: {self.processo.tempo_restante_fase_io}"
                f"\n\tFase 2 CPU restante: {self.processo.tempo_restante_fase2_cpu}"
                f"\n\tStatus: {self.processo.pcb.status.name}"
                f"\n\tTamanho: {self.processo.tam} MiB")