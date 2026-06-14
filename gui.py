from tkinter import *
from tkinter.ttk import Treeview 
from tkinter.ttk import Style
from processos import *
from sistema_operacional import SistemaOperaciona


class Application:

    def __init__(self, so=None):
        self.so=so
        self.processos = so.processos if so else []
        self.despachante = so.despachante if so else None
        self.lock = so.lock if so else None

        self.window = Tk() #cria a janela
        #Configurações da janela
        self.altura = int(self.window.winfo_screenheight() * 0.75) #Altura
        self.largura = int(self.window.winfo_screenwidth() * 0.75) #Largura
        self.tamJanela = str(self.largura) + "x" + str(self.altura)
        print(self.tamJanela)
        self.window.title("Escalonador de Processos") #nome da janela
        self.window.geometry(self.tamJanela) #tamanho da janela ( ͡° ͜ʖ ͡°) 
        icon = PhotoImage(file = "icon.png") #ícone da janela
        self.window.iconphoto(True, icon) #ainda o icone da janela
        self.window.config(bg="#000000") #Etnia da janela ¯\_(ツ)_/¯

        
        self.window.columnconfigure(0, weight=0)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=1)

        #Barra lateral
        self.barra = Frame(self.window, bg="#111111", width=(self.largura/5))
        self.barra.pack(side=LEFT, fill=Y)
        self.barra.pack_propagate(False)
        self.barra_aberta = True

        #Botão para retrair a barra lateral
        self.btn_retrair = Button(self.barra, text="X",
       bg="#111111", fg="#07D2EC", activebackground="#07D2EC", activeforeground="#111111",
       relief=FLAT, font=("Courier", 14),
       highlightthickness=0
       )
        self.btn_retrair.pack(pady=10)
        self.btn_retrair.bind("<ButtonRelease-1>", lambda e: self.retrair_barra())
        
        #Botões de navegação da barra lateral
        Button(self.barra, text="⚙  Criar Processo",
       bg="#111111", fg="#07D2EC", activebackground="#07D2EC", activeforeground="#111111",
       relief=FLAT, anchor="w",
       font=("Courier", 10),
       command=lambda: self.mostrar_tela(processMakingScreen), highlightthickness=0
       ).pack(fill=X, padx=10, pady=5)

        Button(self.barra, text="▤  Listar Processos",
       bg="#111111", fg="#07D2EC", activebackground="#07D2EC", activeforeground="#111111",
       relief=FLAT, anchor="w",
       font=("Courier", 10),
       command=lambda: self.mostrar_tela(processListScreen), highlightthickness=0
       ).pack(fill=X, padx=10, pady=5)

        Button(self.barra, text="▶  Escalonador",
       bg="#111111", fg="#07D2EC", activebackground="#07D2EC", activeforeground="#111111",
       relief=FLAT, anchor="w",
       font=("Courier", 10),
       command=lambda: self.mostrar_tela(processSchedulingScreen), highlightthickness=0
       ).pack(fill=X, padx=10, pady=5)

        
        self.conteudo = Frame(self.window, bg="#0a0a0a")
        self.conteudo.pack(side=LEFT, fill=BOTH, expand=True)

        self.mostrar_tela(processMakingScreen) #mostra a tela principal
        self.window.mainloop()

    def mostrar_tela(self, screen):
        for widget in self.conteudo.winfo_children():
            widget.destroy()
        screen(self.conteudo, self)

    def resetar(self):
        self.so = SistemaOperaciona()
        self.processos = self.so.processos
        self.despachante = self.so.despachante
        self.lock = self.so.lock

    def retrair_barra(self):
        print("estado antes:", self.barra_aberta)
        if self.barra_aberta:
            self.barra.config(width=50)
            self.btn_retrair.config(text="☰", font=("Courier", 14, "bold"))
            self.barra_aberta = False
        else:
            self.barra.config(width=(self.largura/5))
            self.btn_retrair.config(text="X", font=("Courier", 14, "bold"))
            self.barra_aberta = True
        print("estado depois:", self.barra_aberta)

class processMakingScreen(Frame):

    def __init__(self, master, app):
        super().__init__(master, bg="#000000")
        self.app = app
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.columnconfigure(6, weight=1)
        self.pack(fill=BOTH, expand=True)
        
        centro = Frame(self, bg="#000000")
        centro.place(relx=0.5, rely=0.5, anchor="center")

        #Tempo CPU 1
        Label(centro, text="Tempo CPU 1", bg="#000000", fg="#07D2EC", 
            font=("Courier", 10)).grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.entry_cpu1 = Entry(centro, bg="#111111", fg="#07D2EC", insertbackground="#07D2EC")
        self.entry_cpu1.grid(row=3, column=0, padx=10, pady=8, sticky="w")

        #Tempo CPU 2
        Label(centro, text="Tempo CPU 2", bg="#000000", fg="#07D2EC", 
            font=("Courier", 10)).grid(row=2, column=1, padx=10, pady=8, sticky="w")
        self.entry_cpu2 = Entry(centro, bg="#111111", fg="#07D2EC", insertbackground="#07D2EC")
        self.entry_cpu2.grid(row=3, column=1, padx=10, pady=8, sticky="w")

        #Tempo I/O
        Label(centro, text="Tempo I/O", bg="#000000", fg="#07D2EC", 
            font=("Courier", 10)).grid(row=4, column=0, padx=10, pady=8, sticky="w")
        self.entry_io = Entry(centro, bg="#111111", fg="#07D2EC", insertbackground="#07D2EC")
        self.entry_io.grid(row=5, column=0, padx=10, pady=8, sticky="w")

        #Tamanho em memória
        Label(centro, text="Tamanho em memória", bg="#000000", 
            fg="#07D2EC", font=("Courier", 10)).grid(row=4, column=1, padx=10, pady=8, sticky="w")
        self.entry_memoria = Entry(centro, bg="#111111", fg="#07D2EC", insertbackground="#07D2EC")
        self.entry_memoria.grid(row=5, column=1, padx=10, pady=8, sticky="w")

         #prioridades
        Label(centro, text="Prioridade", bg="#000000", 
            fg="#07D2EC", font=("Courier", 10)).grid(row=6, column=0, padx=10, pady=8, sticky="w")
        self.entry_prioridade = Entry(centro, bg="#111111", fg="#07D2EC", insertbackground="#07D2EC")
        self.entry_prioridade.grid(row=7, column=0, padx=10, pady=8, sticky="w")

         #discos
        Label(centro, text="Discos", bg="#000000", 
            fg="#07D2EC", font=("Courier", 10)).grid(row=6, column=1, padx=10, pady=8, sticky="w")
        self.entry_discos = Entry(centro, bg="#111111", fg="#07D2EC", insertbackground="#07D2EC")
        self.entry_discos.grid(row=7, column=1, padx=10, pady=8, sticky="w")

        #Botão :D
        botao = Button(centro, text="Salvar", command=self.processMaker, bg="#05a8bc", fg="#000000",
                       relief=FLAT, activebackground="#07D2EC", 
                       activeforeground="#111111").grid(row=8, column=0, columnspan=2, pady=20)


    def processMaker(self):
        try:
            processo = self.app.despachante.criar_processo(
                int(self.entry_cpu1.get()),
                int(self.entry_io.get()),
                int(self.entry_cpu2.get()),
                int(self.entry_memoria.get()),
                int(self.entry_discos.get()),
                int(self.entry_prioridade.get())
            )
            self.app.processos.append(processo)
            self.app.so.escalonador.admitir_processo(processo)
        except Exception as e:
            print(f"Erro ao salvar processo: {e}")


class processListScreen(Frame):

    def __init__(self, master, app):
        super().__init__(master, bg="#000000")
        self.app = app
        self.pack(expand=True)
        
        #estilo da tabela
        style = Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#111111",
                        foreground="#07D2EC",
                        fieldbackground="#111111",
                        rowheight=30, font=("Courier", 10))
        style.configure("Treeview.Heading",
                        background="#0a0a0a", foreground="#07D2EC",
                        font=("Courier", 10, "bold"))
        

        tabela = Treeview(self,
                           columns=("pid", "cpu1", "io", "cpu2", "memoria")
                           , show="headings")
        tabela.pack(fill=BOTH, expand=True, padx=10, pady=10)

        tabela.heading("pid", text="PID")
        tabela.heading("cpu1", text="Tempo CPU 1")
        tabela.heading("cpu2", text="Tempo CPU 2")
        tabela.heading("io", text="Tempo I/O")
        tabela.heading("memoria", text="Tamanho em memória")

        tabela.column("pid", width=120)
        tabela.column("cpu1", width=120)
        tabela.column("io", width=120)
        tabela.column("cpu2", width=120)
        tabela.column("memoria", width=180)

        for processo in self.app.processos:
            if(isinstance(processo, ProcessoIO)):
                cpu1 = processo.tempo_fase1_cpu
                io = processo.tempo_fase_io
                cpu2 = processo.tempo_fase2_cpu
            else:
                cpu1 = processo.tempo_cpu
                io = "-"
                cpu2 = "-"
            
            tabela.insert("", "end", values=(
                processo.id,
                cpu1,
                io,
                cpu2,
                processo.tam
            ))

class processSchedulingScreen(Frame):

    def __init__(self, master, app):
        super().__init__(master, bg="#000000")
        self.app = app
        self.pack(fill=BOTH, expand=True)
        
        self.tique_atual = 0
        self.historico: list[dict] = []

        #Butões 🇧🇹

        frame_botoes = Frame(self, bg="#000000")
        frame_botoes.pack(pady=30)

        Button(frame_botoes, text="▶️",
               bg="#05a8bc", fg="#000000", relief=FLAT,
               activebackground="#00FF37", activeforeground="#111111",
               font=("Courier", 10),
               command=self._tick
               ).pack(side=LEFT, padx=10)

        Button(frame_botoes, text="⏩",
               bg="#05a8bc", fg="#000000", relief=FLAT,
               activebackground="#D9FF00", activeforeground="#111111",
               font=("Courier", 10),
               command=self._escalonar_tudo
               ).pack(side=LEFT, padx=10)
        

        Button(frame_botoes, text="🔁",
                bg="#05a8bc", fg="#ffffff", relief=FLAT,
                activebackground="#cc4444", activeforeground="#ffffff",
                font=("Courier", 10),
                command=self._resetar
                ).pack(side=LEFT, padx=10)
        

        container_gantt = Frame(self, bg="#000000")
        container_gantt.pack(fill=BOTH, expand=True, padx=10, pady=5)

        scrollbar = Scrollbar(container_gantt, orient=HORIZONTAL)
        scrollbar.pack(side=BOTTOM, fill=X)


        self.canvas_gantt = Canvas(container_gantt, bg="#000000",
                                    yscrollcommand=None,
                                    xscrollcommand=scrollbar.set,
                                    highlightthickness=0)
        self.canvas_gantt.pack(side=TOP, fill=BOTH, expand=True)
        scrollbar.config(command=self.canvas_gantt.xview)

 
        self.frame_gantt = Frame(self.canvas_gantt, bg="#000000")
        self.canvas_window = self.canvas_gantt.create_window((0, 0), window=self.frame_gantt, anchor="nw")


        self.frame_gantt.bind("<Configure>", lambda e: self.canvas_gantt.configure(
            scrollregion=self.canvas_gantt.bbox("all")
        ))


        for i in range(4):
            Label(self.frame_gantt, text=f"CPU {i}", bg="#000000", fg="#07D2EC",
                font=("Courier", 10, "bold")).grid(row=i+1, column=0, padx=(0, 5), pady=5)

        #filas

        frame_filas = Frame(self, bg="#111111")
        frame_filas.pack(fill=X, padx=10, pady=10)

        Label(frame_filas, text="Estado das Filas", bg="#111111", fg="#07D2EC",
              font=("Courier", 10, "bold")).pack(anchor="w", padx=10, pady=5)

        self.label_tempo_real = Label(frame_filas, text="Tempo Real (FCFS): []",
                                      bg="#111111", fg="#07D2EC", font=("Courier", 9))
        self.label_tempo_real.pack(anchor="w", padx=10)

        for i in range(3):
            lbl = Label(frame_filas, text=f"Usuário Fila {i}: []",
                        bg="#111111", fg="#07D2EC", font=("Courier", 9))
            lbl.pack(anchor="w", padx=10)

        self.labels_usuario = frame_filas.winfo_children()[2:]  # pega os 3 labels de fila

        self.label_bloqueados = Label(frame_filas, text="Bloqueados: []",
                                      bg="#111111", fg="#07D2EC", font=("Courier", 9))
        self.label_bloqueados.pack(anchor="w", padx=10)

        self.label_finalizados = Label(frame_filas, text="Finalizados: []",
                                       bg="#111111", fg="#07D2EC", font=("Courier", 9))
        self.label_finalizados.pack(anchor="w", padx=10, pady=(0, 5))

        self.label_dma = Label(frame_filas, text="DMA (discos): []",
                       bg="#111111", fg="#07D2EC", font=("Courier", 9))
        
        self.label_dma.pack(anchor="w", padx=10)

        self.label_dma_espera = Label(frame_filas, text="DMA (fila de espera): []",
                                    bg="#111111", fg="#07D2EC", font=("Courier", 9))
        self.label_dma_espera.pack(anchor="w", padx=10)

    def _tick(self):
        so = self.app.so
        if not so.tem_processos_pendentes():
            return

        snapshot = so.tick()  # ← recebe o snapshot pronto

        self.historico.append(snapshot)
        self._adicionar_coluna_gantt(self.tique_atual, snapshot)
        self.tique_atual += 1
        self._atualizar_filas()

    def _escalonar_tudo(self):
        if self.app.so.tem_processos_pendentes():
            self._tick()
            self.after(50, self._escalonar_tudo)

    def _adicionar_coluna_gantt(self, tique: int, snapshot: dict):
        # Header do tique
        Label(self.frame_gantt, text=str(tique), bg="#000000", fg="#555555",
              font=("Courier", 8), width=4, anchor="center"
              ).grid(row=0, column=tique + 1, padx=1)

        for cpu_id in range(4):
            pid = snapshot.get(cpu_id)
            texto = str(pid) if pid is not None else ""
            cor_bg = "#1a3a4a" if pid is not None else "#0a0a0a"

            Label(self.frame_gantt, text=texto,
                  bg=cor_bg, fg="#07D2EC",
                  font=("Courier", 9), width=4, anchor="center",
                  relief=RIDGE
                  ).grid(row=cpu_id + 1, column=tique + 1, padx=1, pady=1)

    def _atualizar_filas(self):
        esc = self.app.so.escalonador
        dma = self.app.so.dma

        ids_tr = [p.id for p in esc.fila_processos_tempo_real.fila]
        self.label_tempo_real.config(text=f"Tempo Real (FCFS): {ids_tr}")

        for i in range(3):
            ids = [p.id for p in esc.fila_processos_usuario.fila[i]]
            self.labels_usuario[i].config(text=f"Usuário Fila {i}: {ids}")

        ids_bloq = [p.id for p in esc.bloqueados]
        self.label_bloqueados.config(text=f"Bloqueados: {ids_bloq}")

        ids_fin = [p.id for p in esc.finalizados]
        self.label_finalizados.config(text=f"Finalizados: {ids_fin}")

        # DMA
        ids_discos = [p.id if p is not None else "-" for p in dma.discos]
        self.label_dma.config(text=f"DMA (discos): {ids_discos}")

        ids_espera = [p.id for p in dma.fila_espera]
        self.label_dma_espera.config(text=f"DMA (fila de espera): {ids_espera}")
    def _resetar(self):
        self.app.resetar()
        
        for widget in self.frame_gantt.winfo_children():
            widget.destroy()
        
        for i in range(4):
            Label(self.frame_gantt, text=f"CPU {i}", bg="#000000", fg="#07D2EC",
                font=("Courier", 10, "bold")).grid(row=i+1, column=0, padx=(0, 5), pady=5)
        
        self.tique_atual = 0
        self.historico = []
        
        self._atualizar_filas()
