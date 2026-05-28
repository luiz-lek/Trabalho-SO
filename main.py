from processos import Processo
from leitura_processos import *
from escalonador import *
from cpu import CPU
import threading
from memoria_principal import MemoriaPrincipal
from gui import Application
from cpu import CPU
from rich.traceback import install

install()

def executar_processo_prioridade0(processo: Processo, escalonador: Escalonador):
    while(processo.get_tempo_execucao_restante() > 0):
        processo.decrementar_tempo_restante()

    print(f"\n\nProcesso finalizado no estado:\n{processo}")


def executar_processo_prioridade1(processo: Processo, escalonador: Escalonador):
    tempo = 2 ** processo.pcb.ultima_fila

    for i in range(tempo):
        processo.decrementar_tempo_restante()
        escalonador.decrementar_tempo_bloqueados()
        estado = processo.pcb.status
        if estado == Status.BLOQUEADO or estado == Status.FINALIZADO:
            break

    print(f"\n\nProcesso interrompido no estado:\n{processo}")


def executar():
    # Abre o arquivo de entrada, lê os processos e fecha o arquivo
    memoria_principal = MemoriaPrincipal()
    escalonador = Escalonador(memoria_principal)
    despachante = Despachante()

    processos: list[Processo] = alistaProcessos("entrada.txt", despachante)

    # Imprime os processos lidos para verificação
    for processo in processos:        
        # print(f"\nProcesso lido: {processo}")
        escalonador.inserir_processo_novo(processo)

    for i in range(20):
        processo = escalonador.selecionar_processo_para_execucao()

        if processo is None:
            print("Nenhum processo para executar.")
            continue

        despachante.despachar(processo)

        if(processo.pcb.prioridade == 0):
            executar_processo_prioridade0(processo, escalonador)
        else:
            print(f"\n\nProcesso entrou no estado:\n{processo}")
            executar_processo_prioridade1(processo, escalonador)

        escalonador.inserir_processo_interrompido(processo)



def main():
    executar()
    app = Application()
            
    
if __name__ == "__main__":
    main()