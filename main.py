from processos import Processo, CriadorProcessos, Status
from leitura_processos import LeituraArquivo

def main():
    criador_processos = CriadorProcessos() # Cria uma instância da classe CriadorProcessos para criar os objetos Processo a partir dos dados lidos do arquivo
    leitor_arquivo_processos = LeituraArquivo(criador_processos) # Cria uma instância da classe LeituraArquivo para ler os processos do arquivo de entrada
    processos: list[Processo] = leitor_arquivo_processos.alistaProcessos("entrada.txt") # Lê os processos do arquivo de entrada e os armazena em uma lista``

    # Teste de execução dos processos
    for processo in processos:
        processo.pcb.atualizar_status(Status.PRONTO) # Atualiza o status do processo para PRONTO para indicar que ele está pronto para execução
        for i in range(processo.tempo_fase1_cpu):
            processo.atualizar_tempo_restante()
            print(f"\n{processo}")

    for processo in processos:
        for i in range(processo.tempo_fase_io):
            processo.atualizar_tempo_restante()
            print(f"\n{processo}")

    for processo in processos:
        for i in range(processo.tempo_fase2_cpu):
            processo.atualizar_tempo_restante()
            print(f"\n{processo}")
            
    
if __name__ == "__main__":
    main()