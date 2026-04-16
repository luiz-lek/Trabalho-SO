from enum import Enum

class Status(Enum):
    NOVO = 1
    PRONTO_SUSPENSO = 2
    PRONTO = 3
    EXECUTANDO = 4
    SAIDA = 5
    BLOQUEADO = 6
    BLOQUEADO_SUSPENSO = 7

class Processo:
    def __init__(self, id, status, programa):
        self.id = id
        self.status = status
        self.programa = programa