import Processos.PCB as PCB

class Processo:
    def __init__(self, tempo_fase1_cpu: int, tempo_fase_es: int, tempo_fase2_cpu: int, tam: int):
        if tempo_fase1_cpu < 0 or tempo_fase2_cpu < 0 or tempo_fase_es < 0:
            raise ValueError("Tempos de CPU e E/S devem ser valores não negativos");
    
        self.tempo_fase1_cpu = tempo_fase1_cpu
        self.tempo_restante_fase1_cpu = tempo_fase1_cpu
        
        self.tempo_fase2_cpu = tempo_fase2_cpu
        self.tempo_restante_fase2_cpu = tempo_fase2_cpu

        self.tempo_fase_es = tempo_fase_es
        self.tempo_restante_fase_es = tempo_fase_es

        self.pcb = PCB(id)

        self.fase1_cpu = True
        self.fase_es = False
        self.fase2_cpu = False
        

    def executar_unidade_tempo(self) -> None:
        if self.fase1_cpu:
            try:
                self.executar_unidade_tempo_fase1_cpu()
            except RuntimeError as e:
                print(f"Erro ao executar unidade de tempo na fase 1 de CPU: {e}")
            return
        if self.fase_es:
            try:
                self.executar_unidade_tempo_fase_es()
            except RuntimeError as e:
                print(f"Erro ao executar unidade de tempo na fase de E/S: {e}")
            return
        if self.fase2_cpu:
            try:
                self.executar_unidade_tempo_fase2_cpu()
            except RuntimeError as e:
                print(f"Erro ao executar unidade de tempo na fase 2 de CPU: {e}")
            return
        raise RuntimeError("Processo já finalizou a execução.")

    def _executar_unidade_tempo_fase1_cpu(self) -> None:
        if not self.fase1_cpu:
            raise RuntimeError("Processo não está na fase 1 de CPU.")
        
        self.tempo_restante_fase1_cpu -= 1
        if self.tempo_restante_fase1_cpu <= 0:
            self.fase1_cpu = False
            self.fase_es = True
            self.pcb.atualizar_status(PCB.Status.BLOQUEADO)
            print(f"Processo {self.pcb.id} passou para a fase de E/S e foi bloqueado.")

    def _executar_unidade_tempo_fase_es(self) -> None:
        if not self.fase_es:
            raise RuntimeError("Processo não está na fase de E/S.")
        
        self.tempo_restante_fase_es -= 1
        if self.tempo_restante_fase_es <= 0:
            self.fase_es = False
            self.fase2_cpu = True
            self.pcb.atualizar_status(PCB.Status.PRONTO)
            print(f"Processo {self.pcb.id} passou para a fase 2 de CPU e está pronto para execução.")

    def _executar_unidade_tempo_fase2_cpu(self) -> None:
        if not self.fase2_cpu:
            raise RuntimeError("Processo não está na fase 2 de CPU.")
        
        self.tempo_restante_fase2_cpu -= 1
        if self.tempo_restante_fase2_cpu <= 0:
            self.fase2_cpu = False
            self.pcb.atualizar_status(PCB.Status.FINALIZADO)
            print(f"Processo {self.pcb.id} finalizou a execução.") 