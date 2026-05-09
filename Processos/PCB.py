from Processos.Processo import Status

class PCB: #bloco com infos de controle de um processo
    def __init__(self, id: int):
        self.id = id
        self._status = Status.NOVO

    def atualizar_status(self, novo_status: int) -> None:
        self._status = novo_status