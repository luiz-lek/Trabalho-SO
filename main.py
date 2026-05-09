from Processo import Processo

def alistaProcessos(arquivo):
    processos = [] # Lista de processos vazia

    for linha in arquivo:
        processo = leProcesso(linha) # Lê um processo da linha do arquivo
        print(f"Processo lido: {processo}") # Imprime o processo lido para verificação
        processos.append(processo) # Adiciona o processo à lista de processos

    return processos

def leProcesso(linhaProcesso):
    # Divide a linha do processo usando vírgula como delimitador e converte os valores para os tipos apropriados
    partes = linhaProcesso.strip().split(",")

    # Cria e retorna um objeto Processo usando os valores extraídos da linha
    return Processo(
        int(partes[0]),  # idProcesso
        int(partes[1]),  # durCpu1
        int(partes[2]),  # durIO
        int(partes[3]),  # durCpu2
        int(partes[4]),  # tam
    )

def main():
    # Abre o arquivo de entrada, lê os processos e fecha o arquivo
    arquivo = open("entrada.txt", "r")
    processos = alistaProcessos(arquivo.readlines())
    arquivo.close()

    # Imprime os processos lidos para verificação
    for processo in processos:
        print(processo)
    
if __name__ == "__main__":
    main()