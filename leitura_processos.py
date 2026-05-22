from processos import *
from escalonador import Despachante

class LeituraArquivo:
    
    def __init__(self, despachante: Despachante):
        self.despachante = despachante

    def alistaProcessos(self, nome_arquivo: str) -> list[ProcessoIO]:
        # Abre o arquivo de entrada, lê os processos e fecha o arquivo
        arquivo = open(nome_arquivo, "r")
        linhas_arquivo: list[str] = arquivo.readlines()
        processos: list[Processo] = [] # Lista de processos vazia

        for linha in linhas_arquivo:
            try:
                processo = self.leProcesso(linha) # Lê um processo da linha do arquivo
                print(f"\nProcesso lido: {processo}") # Imprime o processo lido para verificação
                processos.append(processo) # Adiciona o processo à lista de processos
            except (ValueError) as e:
                print(f"Erro ao ler processo da linha '{linha.strip()}'")
        arquivo.close()

        return processos

    def leProcesso(self, linhaProcesso: str) -> ProcessoIO:
        # Divide a linha do processo usando vírgula como delimitador e converte os valores para os tipos apropriados
        partes = linhaProcesso.strip().split(",")

        # Cria e retorna um objeto Processo usando os valores extraídos da linha
        try:
            processo = self.despachante.criar_processo(
                int(partes[0]),  # durCpu1
                int(partes[1]),  # durIO
                int(partes[2]),  # durCpu2
                int(partes[3]),  # tam
                int(partes[4])   # prioridade
            )
            return processo
        except (ValueError) as e:
            print(f"Erro ao criar processo: {e}")
            raise