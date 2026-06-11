from enum import Enum
from processos import *

"""
Tarefas a fazer:
1. fazer a verificação de estado de PRONTO dos processos nas funções: alocar..., Clock..., 
2. Eu tava pensando colocar a função interrupção dentro do clock para não precisar chamar duas funções dentro da main.py

"""
class Estado(Enum):
    Vazio = 0
    Ocupado = 1


class CPU:
    def __init__(self, id: int):
        self.id = id #identidade de cada CPU
        self.processo: None | Processo = None #Processo a ser executado dentro da CPU
        self.unid_temp = 0 #contador a cada unidade de tempo percorrida
        self.estado = Estado.Vazio #Estado da CPU


    def alocar_processo(self, processo: Processo):
        """
        Tem o objetivo de:
            1. armazenar o processo, passado pelo parametro, dentro do nosso objeto CPU
            2. mudar o estado da nossa CPU para OCUPADA
            3. mudar o estado do processo exexutado para EXECUTANDO
        """
        self.processo = processo
        self.processo.estado = Estado.EXECUTANDO

        if(processo.prioridade == 0):
            self.unid_temp = processo.get_tempo_execucao_restante()
        else:
            self.unid_temp = 2 ** processo.ultima_fila

        self.estado = Estado.Ocupado


    def desalocar_processo(self) -> Processo:
        """
        Tem o objetivo de:
            1. Retirar o processo dentro no nosso objeto CPU
            2. Mudar o estado da CPU para VAZIO
        """

        copia: Processo = self.processo;
        self.processo = None
        self.estado = Estado.Vazio
        self.unid_temp = 0

        return copia
 

    def clock(self):
        """
        Tem o objetivo de:
            1. Verificar se a CPU está vazia
            2. decrementar, em 1, o tempo de processador de cada processo
        """
        if(self.processo == None or self.estado == Estado.Vazio):
            return
        self.unid_temp -= 1
        self.processo.atualizar_tempo_restante()


    def interromper(self) -> Processo | None:
        """
        Tem o objetivo de:
            1. interrompe o processo quando ele vai para o estado BLOQUEADO
            2. interrompe o processo quando ele termiana a fase 2 da cpu e é FINALIZADO
            3. interrompe o processo quando o processo CPUBound termina o tempo de execução
            4. interrompe o processo a cada quantum.
        """
        if self.processo is None or self.processo.prioridade == 0:
            return None

        elif self.processo.fase == FaseProcesso.IO:
            print("-----------------Interrupção: Processo Bloqueado-----------------")
            self.processo.estado = Estado.BLOQUEADO
                
        elif self.processo.get_tempo_restante_execucao() == 0:
            print("-----------------Interrupção: Processo Finalizado-----------------")
            self.processo.estado = Estado.FINALIZADO

        elif self.unid_temp <= 0: 
            print("-----------------Interrupção: Fatia de tempo-----------------")
            # Não foi bloqueado nem finalizado. Então, o processo volta para a fila de prontos.
            self.processo.estado = Estado.PRONTO
        
        return self.desalocar_processo
        

    def __str__(self) -> str:
        if (self.processo == None):
            return f"CPU {self.id} está ociosa"
        return self.processo.__str__();

class DMA:
    def __init__(self):
        # Representa fisicamente os 4 discos do sistema.
        self.discos: list[ProcessoIO | None] = [None, None, None, None]
        self.estados_discos = [Estado.Vazio for _ in range(4)]
        
        # Fila para processos que chegaram bloqueados, mas não há disco livre no momento.
        self.fila_espera: list[ProcessoIO] = []


    def adicionar_processo(self, processo: ProcessoIO) -> None:
        """
        Recebe um processo que terminou a Fase 1 da CPU e o coloca na fila de espera.
        Em seguida, tenta alocá-lo imediatamente em um disco, se houver vaga.
        """
        self.fila_espera.append(processo)
        self._alocar_nos_discos()


    def _alocar_nos_discos(self) -> None:
        """
        Método interno (privado) que move os processos da fila de espera 
        para os discos que estiverem com o estado Vazio.
        """
        for i in range(4):
            if self.estados_discos[i] == Estado.Vazio and len(self.fila_espera) > 0:
                # Remove o primeiro processo da fila (posição 0) e coloca no disco
                processo_para_alocar = self.fila_espera.pop(0)
                
                self.discos[i] = processo_para_alocar
                self.estados_discos[i] = Estado.Ocupado
                print(f"DMA: Processo {processo_para_alocar.id} iniciou I/O no Disco {i}.")


    def clock(self) -> list[ProcessoIO]:
        """
        Avança o tempo de I/O de todos os processos que estão atualmente nos discos.
        Retorna uma lista de processos que terminaram o I/O neste exato tique,
        para que o main.py possa devolvê-los ao Escalonador.
        """
        processos_concluidos: list[ProcessoIO] = []

        for i in range(4):
            if self.estados_discos[i] == Estado.Ocupado:
                processo = self.discos[i]
                
                if processo is not None:
                    processo.atualizar_tempo_restante()

                    if processo.tempo_fase_io <= 0:
                        processos_concluidos.append(processo)
                        
                        self.discos[i] = None
                        self.estados_discos[i] = Estado.Vazio
                        print(f"DMA: Processo {processo.id} liberou o Disco {i}.")

        self._alocar_nos_discos()
        
        return processos_concluidos
    

    def __str__(self) -> str:
        """
        Gera uma representação em texto do estado atual do DMA,
        útil para exibir na interface/console a cada unidade de tempo.
        """
        status_discos = []
        for i in range(4):
            if self.estados_discos[i] == Estado.Vazio:
                status_discos.append(f"Disco {i}: Vazio")
            else:
                processo = self.discos[i]
                if processo is not None:
                    status_discos.append(f"Disco {i}: Processo {processo.id} (Faltam {processo.tempo_restante_fase_io} u.t.)")
        
        fila_ids = [p.id for p in self.fila_espera]
        
        return (f"--- Status do DMA ---\n"
                f"{chr(10).join(status_discos)}\n"
                f"Fila de Espera (I/O): {fila_ids}\n"
                f"---------------------")
    

"""
código para interrompar a CPU em caso de finalização de processo do DMA. Eu pensei e colocá-la na main
para a implementação deste código eu pensei em fazer:


for processo in FinalizadosDMA: #FinalizadosDMA é a fila de processos que tenha terminado sua execução no DMA
    fila.adicionar_processo(processo) #não sei se essa é a função para adicionar o processo a fista

quant_cpu_interrompida = len(FinalizadosDMA) #quantidade de processo finalizados no DMA

for cpu in CPUs:
    if(quant_cpu_interrompida == 0): #se não tiver processo finalizado pelo DMA, então nenhuma CPU será interrompida
        break;
    if(cpu.processo is None):
        continue
    if(cpu.processo.pioridade == 1): #As CPUs devem ficar um uma lista contendo todas as 4 CPUs
        process_interrompido = cpu.desalocar_processo();    
        flia.adicionar_processo(processo_interompido);
        quant_cpu_interrompida -= 1;

"""