class Processo:
    def __init__(self, idProcesso, durCpu1, durIO, durCpu2, tam):
        self.idProcesso = idProcesso
        self.durCpu1 = durCpu1
        self.durIO = durIO
        self.durCpu2 = durCpu2
        self.tam = tam

    def __str__(self):
        return f"Processo {self.idProcesso}: CPU1={self.durCpu1}, IO={self.durIO}, CPU2={self.durCpu2}, TAM={self.tam}"