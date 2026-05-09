import Processos.Processo as Processo
import Processos.Status as Status

class CriadorProcessos:
    def __init__ (self):
        self.contador_id = -1

    def proximo_id(self) -> int:
        self.contador_id += 1
        return self.contador_id

    def criar_processo(self, tempo1_cpu: int, tempo2_cpu: int, tempo_es: int, tam: int) -> Processo:
        id = self.proximo_id()
        processo = None

        try:
            processo = Processo(id, tempo1_cpu, tempo2_cpu, tempo_es, tam)
        except ValueError as e:
            print(f"Erro ao criar processo: {e}")
            raise

        return processo