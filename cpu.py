from enum import Enum
from processos import *
from queue import Queue

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
        self.interrupcao_habilitada: bool = False #variável para indicar se a CPU deve ser interrompida
        self.processo: None | Processo = None #Processo a ser executado dentro da CPU
        self.quantum = 0 #contador a cada unidade de tempo percorrida
        self.estado = Estado.Vazio #Estado da CPU


    def alocar_processo(self, processo: Processo):
        """
        Tem o objetivo de:
            1. armazenar o processo, passado pelo parametro, dentro do nosso objeto CPU
            2. mudar o estado da nossa CPU para OCUPADA
            3. mudar o estado do processo executado para EXECUTANDO
        """
        self.processo = processo

        # Processo já é despachado com o estado EXECUTANDO, 
        # então não é necessário atualizar o estado do processo aqui.

        if(processo.prioridade == 0):
            self.quantum = processo.get_tempo_execucao_restante()
            self.interrupcao_habilitada = False
        else:
            self.quantum = 2 ** processo.ultima_fila
            self.interrupcao_habilitada = True

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
        self.quantum = 0

        return copia
 

    def clock(self) -> Processo | None:
        """
        Tem o objetivo de:
            1. Verificar se a CPU está vazia
            2. decrementar, em 1, o tempo de processador de cada processo
            3. Verificar se o processo deve ser desalocado, seja por finalização, bloqueio ou interrupção.
        """
        if self.estado == Estado.Vazio:
            print(f"Cpu {self.id} ociosa...")
            return None
        
        print(f"CPU {self.id} executando processo {self.processo.id} (Fase: {self.processo.fase}, Tempo restante: {self.processo.get_tempo_execucao_restante()} u.t., Quantum restante: {self.quantum} u.t.)")
        self.quantum -= 1
        self.processo.decrementar_tempo_restante()

        processo_removido: Processo | None = None

        # Troca de contexto se o processo entrou em IO ou finalizou a execução. 
        trocou: bool = self._verificar_troca_de_contexto()
        if trocou:
            processo_removido = self.desalocar_processo()
        elif self.interrupcao_habilitada and self.quantum <= 0: # Interrupção por quantum esgotado.
            print(f"[Interrupção]: (Processo {self.processo.id}) esgotou o quantum e perdeu CPU.")
            processo_removido = self.interromper()

        return processo_removido


    def _verificar_troca_de_contexto(self) -> bool:
        trocou = False

        if self.processo.get_tempo_execucao_restante() == 0:
            print(f"[Finalizado]: Processo {self.processo.id} finalizou a execução e perdeu cpu.")
            self.processo.estado = EstadoProcesso.FINALIZADO
            return True
        
        if self.processo.prioridade == 0:
            return False
        
        if self.processo.fase == FaseProcesso.IO:
            print(f"[Chamada de sistema]: Processo {self.processo.id} solicitou I/O e perdeu cpu.")
            self.processo.estado = EstadoProcesso.BLOQUEADO
            return True

    def interromper(self) -> Processo | None:
        if not self.interrupcao_habilitada:
            raise RuntimeError(f"Interrupção não habilitada para a CPU {self.id}.")
        
        processo_interrompido = self.desalocar_processo()
        processo_interrompido.estado = EstadoProcesso.PRONTO
        return processo_interrompido

    def __str__(self) -> str:
        if (self.processo == None):
            return f"CPU {self.id} está ociosa"
        return self.processo.__str__();

class DMA:
    def __init__(self):
        # Representa fisicamente os 4 discos do sistema.
        self.discos: list[ProcessoIO | None] = [None, None, None, None]
        
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
        tam_fila = len(self.fila_espera)

        for _ in range (tam_fila):
            if len(self.fila_espera) == 0:
                return
            
            processo: ProcessoIO = self.fila_espera.pop(0)
            lista_discos = self.verificar_discos_disponiveis(processo.qtd_discos)

            if lista_discos is None:
                self.fila_espera.append(processo)
                continue
            
            for indice_disco in lista_discos:
                self.discos[indice_disco] = processo

    def verificar_discos_disponiveis(self, qtd_solicitada: int) -> list[int] | None:
        '''
            Retorna a lista com o índice no vetor de discos para o processor alocar.
            Se não tiver a quantidade desejada, retorna None.
        '''

        lista_disponveis: list[int] = []
        qtd_disponivel = 0

        for i in range(len(self.discos)):
            if self.discos[i] is not None:
                continue
            lista_disponveis.append(i)
            qtd_disponivel+=1
            if qtd_disponivel == qtd_solicitada:
                break

        if len(lista_disponveis) == qtd_solicitada:
            return lista_disponveis
        return None
    
    def clock(self) -> list[ProcessoIO]:
        """
        Avança o tempo de I/O de todos os processos que estão atualmente nos discos.
        Retorna uma lista de processos que terminaram o I/O neste exato tique,
        para que o main.py possa devolvê-los ao Escalonador.
        """

        print(f"DMA [fila de espera]: ", end=" ")
        for processo in  self.fila_espera:
            print(f"{processo.id}", end=" ")
        print()

        processos_concluidos: list[ProcessoIO] = []
        processos_executados = set()

        for i in range(4):
            processo = self.discos[i]

            if (processo is None) or (processo in processos_executados):
                continue

            processo.decrementar_tempo_restante()
            processos_executados.add(processo)

            if processo.tempo_fase_io <= 0:
                processo.estado = EstadoProcesso.PRONTO
                processos_concluidos.append(processo)
                self.liberar_discos(processo)
        
        self._alocar_nos_discos()
        return processos_concluidos
    
    def liberar_discos(self, processo: Processo):
        # Libera tds os discos que ele está ocupando
        print(f"DMA: Processo {processo.id} liberou o Disco(s) ", end="")
        for i in range (len(self.discos)):
            if self.discos[i] is processo:
                self.discos[i] = None
                print(f"{i} ", end="")
        print()

    def __str__(self) -> str:
        """
        Gera uma representação em texto do estado atual do DMA,
        útil para exibir na interface/console a cada unidade de tempo.
        """
        status_discos = []
        for i in range(4):
            if self.discos[i] is None:
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