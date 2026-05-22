from processos import Processo

class Despachante:
    def __init__(self):
        # Fila de processos de tempo real prontos
        self.filaProntosTR = []

        # Filas de processos de usuário prontos
        self.filaProntos1 = []
        self.filaProntos2 = []
        self.filaProntos3 = []

    # Adiciona processo de tempo real na fila de prontos correspondente
    def admiteProcessoTR(self, p: Processo):
        self.filaProntosTR.append(p)

    # Adiciona processo de usuário na fila de prontos correspondente
    def admiteProcessoU(self, p: Processo):
        self.filaProntos1.append(p)