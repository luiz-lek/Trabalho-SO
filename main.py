from processos import Processo
from LeituraArquivo import LeituraArquivo

def main():
    leitor_arquivo_processos = LeituraArquivo() # Cria uma instância da classe LeituraArquivo para ler os processos do arquivo de entrada
    processos: list[Processo] = leitor_arquivo_processos.alistaProcessos("entrada.txt") # Lê os processos do arquivo de entrada e os armazena em uma lista

    # Imprime os processos lidos para verificação
    for processo in processos:
        print(processo)
    
if __name__ == "__main__":
    main()