from processos import Processo, Status
from leitura_processos import *
from escalonador import *
import threading
from memoria_principal import MemoriaPrincipal
from GUI import Application
from cpu import CPU
from rich.traceback import install
install()

def main():
    # Abre o arquivo de entrada, lê os processos e fecha o arquivo
    escalonador = Escalonador()
    despachante = Despachante()
    leitura_entrada = LeituraArquivo(despachante)
    processos: list[Processo] = leitura_entrada.alistaProcessos("entrada.txt")

    # Imprime os processos lidos para verificação
    for processo in processos:
        print(f"\nProcesso lido: {processo}")
        escalonador.inserir_processo__novo(processo)

    app = Application()
            
    
if __name__ == "__main__":
    main()