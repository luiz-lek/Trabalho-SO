# 🖥️ Simulador de Sistema Operacional

Trabalho da disciplina **Sistemas Operacionais** TCC00316

Simulação de um sistema operacional com escalonamento de processos, gerenciamento de memória, I/O via DMA e interface gráfica em Tkinter.



## Como rodar

**Pré-requisitos:** Python 3

Instale o Tkinter caso não tenha:


### Clone o repositório

```bash
git clone https://github.com/luiz-lek/Trabalho-SO.git
cd Trabalho-SO
```

### Rode o projeto
```bash
python app.py
```

> O arquivo `entrada.txt` deve estar na mesma pasta que `app.py`, com os processos que serão carregados na inicialização.

---

## 📄 Formato do "entrada.txt"

Cada linha representa um processo, com os campos separados por vírgula:

```
tempo_fase1_cpu, tempo_io, tempo_fase2_cpu, tamanho_MiB, qtd_discos, prioridade
```

**Exemplo:**
```
4,2,3,128,1,1
6,0,0,256,0,0
```

| Campo | Descrição |
|---|---|
| `tempo_fase1_cpu` | Duração da primeira fase de CPU (u.t.) |
| `tempo_io` | Duração da fase de I/O (0 = processo CPU-bound) |
| `tempo_fase2_cpu` | Duração da segunda fase de CPU (u.t.) |
| `tamanho_MiB` | Memória necessária (máx. 32000 MiB; CPU-bound: máx. 512 MiB) |
| `qtd_discos` | Discos solicitados para I/O (1–4; 0 para CPU-bound) |
| `prioridade` | `0` = tempo real (FCFS) / `1` = usuário (Feedback) |

---

## 📁 Estrutura dos arquivos

```
.
├── app.py                  # Ponto de entrada da aplicação
├── sistema_operacional.py  # Classe principal que orquestra todos os componentes
├── escalonador.py          # Escalonador (FCFS + Feedback) e Despachante
├── cpu.py                  # Classes CPU e DMA
├── processos.py            # Classes de processo (CPU-bound e I/O-bound)
├── memoria_principal.py    # Gerenciamento de memória (First Fit)
├── leitura_processos.py    # Leitura do arquivo de entrada
├── gui.py                  # Interface gráfica (Tkinter)
└── entrada.txt             # Arquivo com os processos a serem simulados
```

---

## ⚙️ Componentes principais

### Escalonamento
- Processos de **tempo real** (prioridade 0): política **FCFS**
- Processos de **usuário** (prioridade 1): política **Feedback multinível** com 3 filas e quantum exponencial (`2^fila`)

### Memória
- Memória principal de **32.000 MiB**
- Alocação pelo algoritmo **First Fit**
- Desalocação automática ao término do processo

### I/O via DMA
- **4 discos** disponíveis
- Processos bloqueados aguardam disco na fila de espera do DMA
- Ao concluir o I/O, o processo volta para a fila de prontos

### Ciclo de execução
Cada tick do sistema executa, em ordem:
1. Despacha processos para CPUs ociosas
2. Executa um ciclo de clock em cada CPU
3. Trata processos que perderam a CPU (bloqueio, preempção ou finalização)
4. Avança o DMA e desbloqueia processos que concluíram I/O
5. Tenta admitir novos processos na memória

---

## 👥 Autores
- [@Danilo Alexandre](https://github.com/TheChronicMasterX)
- [@Eric Maia](https://github.com/3ricz71)
- [@Luiz Eduardo](https://github.com/luiz-lek)
- [@Yago Santos](https://github.com/YAGO-SG)
