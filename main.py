from leitura_processos import alistaProcessos
from sistema_operacional import SistemaOperaciona

from rich.traceback import install
install()

def main():
    so = SistemaOperaciona()
    for i in range(30):
        print(f"========================= Tique {i} =========================")
        so.executar()
    # app = Application()
              
if __name__ == "__main__":
    main()