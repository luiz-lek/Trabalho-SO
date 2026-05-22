from enum import Enum
from processos import ProcessoIO, Status, ProcessoCPUBound

#Tarefas a fazer:
#1. fazer a verificação de estado de PRONTO dos processos nas funções: alocar..., Clock..., 

#Onde eu parei:
#Criar a classe DMA.

class Estado(Enum):
    Vazio = 0
    Ocupado = 1


class CPU:
    def __init__(self, id: int):
        self.id = id #identidade de cada CPU
        self.processo: None | ProcessoCPUBound | ProcessoIO = None #Processo a ser executado dentro da CPU
        self.unid_temp = 0 #contador a cada unidade de tempo percorrida
        self.estado = Estado.Vazio #Estado da CPU


    def alocar_processo(self, processo: ProcessoIO | ProcessoCPUBound):
        """
        Tem o objetivo de:
            1. armazenar o processo, passado pelo parametro, dentro do nosso objeto CPU
            2. mudar o estado da nossa CPU para OCUPADA
            3. mudar o estado do processo exexutado para EXECUTANDO
        """
        self.processo = processo
        self.processo.pcb.status = Status.EXECUTANDO
        self.estado = Estado.Ocupado


    def desalocar_processo(self) -> ProcessoIO | ProcessoCPUBound:
        """
        Tem o objetivo de:
            1. Retirar o processo dentro no nosso objeto CPU
            2. Mudar o estado da CPU para VAZIO
            3. Quando desalocado por interrução por fatia de tempo, muda o estado do processo para PRONTO
        """
        if(self.processo.pcb.status == Status.EXECUTANDO):
            self.processo.pcb.status = Status.PRONTO

        copia: ProcessoCPUBound | ProcessoIO = self.processo;
        self.processo = None
        self.estado = Estado.Vazio
        self.unid_temp = 0

        return copia


    def Clock_CPU(self):
        """
        Tem o objetivo de:
            1. Verificar se a CPU está vazia
            2. decrementar, em 1, o tempo de processador de cada processo
        """
        if(self.processo == None or self.estado == Estado.Vazio):
            return
        self.unid_temp += 1
        self.processo.atualizar_tempo_restante()


    def interrupção(self) -> ProcessoIO | ProcessoCPUBound:
        """
        Tem o objetivo de:
            1. interrompe o processo quando ele vai para o estado BLOQUEADO
            2. interrompe o processo quando ele termiana a fase 2 da cpu e é FINALIZADO
            3. interrompe o processo quando o processo CPUBound termina o tempo de execução
            4. interrompe o processo a cada quantum.
        """
        if self.processo is None:
            return

        if isinstance(self.processo, ProcessoIO):
            resultado = self.inter_processoIO()
            if resultado is not None:
                return resultado
                
        elif isinstance(self.processo, ProcessoCPUBound):
            resultado = self.inter_ProcessoCPUBound()
            if resultado is not None:
                return resultado

        if self.unid_temp >= 2 and not self.processo.pcb.prioridade == 0: 
            print("-----------------Interrupção: Fatia de tempo-----------------")
            return self.desalocar_processo()
        

    def inter_processoIO(self) -> ProcessoIO: #Verifica os casos de interrupção para processos do tipo IO
        if(self.processo.fase_io == True):
            print("-----------------Interrupção: Processo Bloqueado-----------------")
            return self.desalocar_processo()
        elif(self.processo.get_tempo_restante_execucao() == 0):
            print("-----------------Interrupção: Processo Finalizado-----------------")
            return self.desalocar_processo()
        else:
            return 
        

    def inter_ProcessoCPUBound(self) -> ProcessoCPUBound: #Verifica o caso de interrupção para processos do tipo CPUBound
        if(self.processo.get_tempo_restante_execucao() == 0):
            print("-----------------Interrupção: Processo Finalizado-----------------")
            return self.desalocar_processo()
        else:
            return


    def __str__(self) -> str:
        if (self.processo == None):
            return f"CPU {self.id} está ociosa"
        if(isinstance(self.processo, ProcessoIO)):
            return (f"Processo: {self.processo.pcb.id}"
                f"\n\tFase 1 CPU restante: {self.processo.tempo_restante_fase1_cpu}"
                f"\n\tFase I/O restante: {self.processo.tempo_restante_fase_io}"
                f"\n\tFase 2 CPU restante: {self.processo.tempo_restante_fase2_cpu}"
                f"\n\tStatus: {self.processo.pcb.status.name}"
                f"\n\tTamanho: {self.processo.tam} MiB")
        elif(isinstance(self.processo, ProcessoCPUBound)):
            return (f"Processo: {self.processo.pcb.id}" 
                f"\n\tTempo de CPU restante: {self.processo.tempo_restante_cpu}"
                f"\n\tStatus: {self.processo.pcb.status.name}"
                f"\n\tPrioridade: {self.processo.pcb.prioridade}"
                f"\n\tTamanho: {self.processo.tam} MiB")
    

class DMA:
    pass