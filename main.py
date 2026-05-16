from processos import Processo, CriadorProcessos, Status
from leitura_processos import *
from GUI import Application

def main():
    # Abre o arquivo de entrada, lê os processos e fecha o arquivo
    arquivo = open("entrada.txt", "r")
    processos = alistaProcessos(arquivo.readlines())
    arquivo.close()

    # Imprime os processos lidos para verificação
    for processo in processos:
        for i in range(processo.tempo_fase2_cpu):
            processo.atualizar_tempo_restante()
            print(f"\n{processo}")
            
    
if __name__ == "__main__":
    app = Application() # inicia as interface gráfica
    main()