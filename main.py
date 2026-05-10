from processos import Processo, CriadorProcessos
from LeituraArquivo import LeituraArquivo

def main():
    leitor_arquivo_processos = LeituraArquivo() # Cria uma instância da classe LeituraArquivo para ler os processos do arquivo de entrada
    criador_processos = CriadorProcessos() # Cria uma instância da classe CriadorProcessos para criar os objetos Processo a partir dos dados lidos do arquivo
    leitor_arquivo_processos = LeituraArquivo(criador_processos) # Cria uma instância da classe LeituraArquivo para ler os processos do arquivo de entrada
    processos: list[Processo] = leitor_arquivo_processos.alistaProcessos("entrada.txt") # Lê os processos do arquivo de entrada e os armazena em uma lista

    # Imprime os processos lidos para verificação
    for processo in processos:
        print(f"\n{processo}")
    
if __name__ == "__main__":
    main()