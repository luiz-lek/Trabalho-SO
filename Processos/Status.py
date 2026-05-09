from enum import Enum

class Status(Enum):
    NOVO = 0
    PRONTO = 1
    EXECUTANDO = 2
    BLOQUEADO = 3
    FINALIZADO = 4