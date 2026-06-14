import threading
from sistema_operacional import SistemaOperaciona
from gui import Application
from rich.traceback import install

install()

def main():
    so = SistemaOperaciona()

    app = Application(so=so)
              
if __name__ == "__main__":
    main()