from escalonador import Despachante
from processos import Processo, Status
from leitura_processos import LeituraArquivo

def main():
    despachante = Despachante() # Cria uma instância da classe Despachante para criar os objetos Processo a partir dos dados lidos do arquivo
    leitor_arquivo_processos = LeituraArquivo(despachante) # Cria uma instância da classe LeituraArquivo para ler os processos do arquivo de entrada
    processos: list[Processo] = leitor_arquivo_processos.alistaProcessos("entrada.txt") # Lê os processos do arquivo de entrada e os armazena em uma lista``

    
    # Teste de execução dos processos
    for processo in processos:
        processo.pcb.atualizar_status(Status.PRONTO) # Atualiza o status do processo para PRONTO para indicar que ele está pronto para execução
        tempo_total = processo.get_tempo_restante_total() # Obtém o tempo total restante para a execução do processo
        for i in range(tempo_total):
            processo.atualizar_tempo_restante()
            print(f"\n{processo}")

    
if __name__ == "__main__":
    main()