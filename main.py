from processos import Processo, Status
from leitura_processos import *
from escalonador import *
from GUI import Application

def main():
    # Abre o arquivo de entrada, lê os processos e fecha o arquivo
    memoria = None # Criar a memória assim que implementada.
    escalonador = Escalonador(memoria)
    despachante = Despachante(escalonador)
    leitura_entrada = LeituraArquivo(despachante)
    processos: list[Processo] = leitura_entrada.alistaProcessos("entrada.txt")

    # Imprime os processos lidos para verificação
    for processo in processos:
        tempo_total = processo.get_tempo_restante_execucao() # Obtém o tempo total restante para a execução do processo
        processo.pcb.status = Status.PRONTO # Define o status do processo como PRONTO para simular a execução
        for i in range(tempo_total):
            processo.atualizar_tempo_restante()
            print(f"\n{processo}")
            
    
if __name__ == "__main__":
    app = Application() # inicia as interface gráfica
    main()