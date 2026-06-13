import threading
from sistema_operacional import SistemaOperaciona
from gui import Application
from rich.traceback import install

install()


def main():
    processos = []
    so = SistemaOperaciona(processos=processos)

    thread_so = threading.Thread(target=so.executar, daemon=True)
    thread_so.start()
    
    app = Application(so=so)
              
if __name__ == "__main__":
    main()