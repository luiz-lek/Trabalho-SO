import threading
from sistema_operacional import SistemaOperacional
from gui import Application
from rich.traceback import install

install()

def main():
    so = SistemaOperacional()
    app = Application(so)
              
if __name__ == "__main__":
    main()