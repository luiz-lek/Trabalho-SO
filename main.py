from processos import Processo, Status
from leitura_processos import *
from escalonador import *
from cpu import Cpu
from memoria_principal import MemoriaPrincipal
from GUI import Application

def main():
    # Abre o arquivo de entrada, lê os processos e fecha o arquivo
    memoria = MemoriaPrincipal() # Criar a memória assim que implementada.
    escalonador = Escalonador(memoria)
    despachante = Despachante()
    leitura_entrada = LeituraArquivo(despachante)
    processos: list[Processo] = leitura_entrada.alistaProcessos("entrada.txt")

    # Imprime os processos lidos para verificação
    for processo in processos:
        print(f"\nProcesso lido: {processo}")
        escalonador.inserir_processo__novo(processo)

    # processo = processos[0] # Seleciona o primeiro processo para execução
    # for i in range(10): # Simula 10 ciclos de execução da CPU.
    #     if processo.pcb.prioridade == 1:
    #         if processo.pcb.status == Status.EXECUTANDO: # Não foi bloqueado ou finalizado durante a execução, então ele deve ser reinserido no final da fila.
    #             processo.pcb.status = Status.PRONTO
    #         escalonador.inereir_processo_interrompido(processo) # Reinsere o processo que estava sendo executado no final da fila, caso ele não tenha finalizado a execução.
    #     processo = escalonador.selecionar_processo_para_execucao() # Seleciona o primeiro processo para execução
    #     if processo is None:
    #         break
    #     despachante.despachar(processo) # Despacha o processo selecionado para execução
    #     processo.decrementar_tempo_restante() # Decrementa o tempo restante do processo que está sendo executado, simulando a execução de uma unidade de tempo da CPU.
    #     print(f"\nProcesso em execução\n {processo}")
            
    
if __name__ == "__main__":
    app = Application() # inicia as interface gráfica
    main()