from processos import Processo
from leitura_processos import *
from escalonador import *
from cpu import CPU
import threading
from memoria_principal import MemoriaPrincipal
from gui import Application
from rich.traceback import install

install()

def executar():
    # Abre o arquivo de entrada, lê os processos e fecha o arquivo
    memoria_principal = MemoriaPrincipal()
    escalonador = Escalonador(memoria_principal)
    despachante = Despachante()

    processos: list[Processo] = alistaProcessos("entrada.txt", despachante)


def main():
    executar()
    app = Application()
            
    
if __name__ == "__main__":
    main()