from escalonador import Despachante
from processos import Processo, Status
from leitura_processos import LeituraArquivo
import time
from CPU import CPU
from rich.traceback import install
install()

def main():
    despachante = Despachante() # Cria uma instância da classe Despachante para criar os objetos Processo a partir dos dados lidos do arquivo
    leitor_arquivo_processos = LeituraArquivo(despachante) # Cria uma instância da classe LeituraArquivo para ler os processos do arquivo de entrada
    processos: list[Processo] = leitor_arquivo_processos.alistaProcessos("/home/yagosg/Faculdade/Estudos/Internos/SO/Trabalho-SO/entrada.txt") # Lê os processos do arquivo de entrada e os armazena em uma lista``

    """
    # Teste de execução dos processos
    for processo in processos:
        tempo_total = processo.get_tempo_restante_execucao() # Obtém o tempo total restante para a execução do processo
        for i in range(tempo_total):
            processo.atualizar_tempo_restante()
            print(f"\n{processo}")
    """


    #Esse Código abaixo, eu criei para rodar os testes da CPU
    #Ele não vai rodar Todo o processo direitinho por que falta o DMA para lidar com a questão do processo BLOQUEADO e a MP para mudar o estatus do processo para PRONTO, mas quando for feito deve funcionar direitinho

    posição = 0
    CPU1 = CPU(0)
    CPU2 = CPU(1)
    CPU3 = CPU(2)
    CPU4 = CPU(3)

    CPUs = [CPU1, CPU2, CPU3, CPU4]

    while(True):

        if(CPUs[0].estado.value == 0):
            CPUs[0].alocar_processo(processos[posição])

        print(CPUs[0])

        CPUs[0].interrupção()
        CPUs[0].Clock_CPU()
        

        time.sleep(1)

    
if __name__ == "__main__":
    main()