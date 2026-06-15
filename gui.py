from tkinter import *
from tkinter.ttk import Treeview 
from tkinter import messagebox
from tkinter.ttk import Style
from tkinter.ttk import Scrollbar as TtkScrollbar
from processos import *
from sistema_operacional import SistemaOperacional


class Application:

    def __init__(self, so=None):
        self.so = so
        self.processos = so.processos if so else []
        self.lock = so.lock if so else None

        self.telas = {} 

        self.window = Tk() #cria a janela
        #Configurações da janela
        self.altura = int(self.window.winfo_screenheight() * 0.75) #Altura
        self.largura = int(self.window.winfo_screenwidth() * 0.75) #Largura
        self.tamJanela = str(self.largura) + "x" + str(self.altura)
        print(self.tamJanela)
        self.window.title("Escalonador de Processos") #nome da janela
        self.window.geometry(self.tamJanela) #tamanho da janela 
        icon = PhotoImage(file = "icon.png") #ícone da janela
        self.window.iconphoto(True, icon) #ainda o icone da janela
        self.window.config(bg="#000000") #Etnia da janela 
        
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
        
        # --- ORDEM DOS BOTÕES DA BARRA LATERAL ---

        Button(self.barra, text="▶  Escalonador",
       bg="#111111", fg="#07D2EC", activebackground="#07D2EC", activeforeground="#111111",
       relief=FLAT, anchor="w",
       font=("Courier", 10),
       command=lambda: self.mostrar_tela(processSchedulingScreen), highlightthickness=0
       ).pack(fill=X, padx=10, pady=5)

        Button(self.barra, text="▤  Listar Processos",
       bg="#111111", fg="#07D2EC", activebackground="#07D2EC", activeforeground="#111111",
       relief=FLAT, anchor="w",
       font=("Courier", 10),
       command=lambda: self.mostrar_tela(processListScreen), highlightthickness=0
       ).pack(fill=X, padx=10, pady=5)

        Button(self.barra, text="⚙  Criar Processo",
       bg="#111111", fg="#07D2EC", activebackground="#07D2EC", activeforeground="#111111",
       relief=FLAT, anchor="w",
       font=("Courier", 10),
       command=lambda: self.mostrar_tela(processMakingScreen), highlightthickness=0
       ).pack(fill=X, padx=10, pady=5)

        
        self.conteudo = Frame(self.window, bg="#0a0a0a")
        self.conteudo.pack(side=LEFT, fill=BOTH, expand=True)

        self.mostrar_tela(processSchedulingScreen) 
        self.window.mainloop()

    def mostrar_tela(self, screen):
        # Esconde os widgets em vez de destruir
        for widget in self.conteudo.winfo_children():
            widget.pack_forget()

        # Se a tela não foi criada ainda, cria e salva no cache
        if screen not in self.telas:
            self.telas[screen] = screen(self.conteudo, self)
        
        # Recupera a tela do cache e exibe
        tela_atual = self.telas[screen]
        tela_atual.pack(fill=BOTH, expand=True)

        # Força a atualização dos dados se a tela possuir o método
        if hasattr(tela_atual, 'atualizar_dados'):
            tela_atual.atualizar_dados()

    def resetar(self):
        self.so = SistemaOperacional()
        self.processos = self.so.processos
        self.lock = self.so.lock
        
        # FIX: Agora destruímos de verdade as telas antigas para evitar bugs e sobreposição
        for widget in self.conteudo.winfo_children():
            widget.destroy()
            
        self.telas.clear() 
        self.mostrar_tela(processSchedulingScreen) # Recria a tela do zero!

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
            self.app.so.adicionar_processo(
                int(self.entry_cpu1.get()),
                int(self.entry_io.get()),
                int(self.entry_cpu2.get()),
                int(self.entry_memoria.get()),
                int(self.entry_discos.get()),
                int(self.entry_prioridade.get())
            )
            messagebox.showinfo("Sucesso", "Processo salvo e enfileirado!")
        except Exception as e:
            print(f"Erro ao salvar processo: {e}")
            messagebox.showwarning("Aviso", f"Dados inválidos:\n{e}")


class processListScreen(Frame):

    def __init__(self, master, app):
        super().__init__(master, bg="#000000")
        self.app = app
        self.pack(expand=True)
        
        style = Style()
        style.theme_use("clam")
        
        style.configure("Treeview", background="#111111",
                        foreground="#07D2EC",
                        fieldbackground="#111111",
                        rowheight=40, font=("Courier", 14)) 
        
        style.configure("Treeview.Heading",
                        background="#0a0a0a", foreground="#07D2EC",
                        font=("Courier", 14, "bold"))
        
        self.tabela = Treeview(self,
                           columns=("pid", "prioridade", "cpu1", "io", "cpu2", "memoria", "discos")
                           , show="headings", height=15)
        self.tabela.pack(fill=BOTH, expand=True, padx=20, pady=20)

        self.tabela.heading("pid", text="PID")
        self.tabela.heading("prioridade", text="Prioridade")
        self.tabela.heading("cpu1", text="Tempo CPU 1")
        self.tabela.heading("cpu2", text="Tempo CPU 2")
        self.tabela.heading("io", text="Tempo I/O")
        self.tabela.heading("memoria", text="Memória")
        self.tabela.heading("discos", text="Discos")

        self.tabela.column("pid", width=100, anchor="center")
        self.tabela.column("prioridade", width=160, anchor="center")
        self.tabela.column("cpu1", width=160, anchor="center")
        self.tabela.column("io", width=160, anchor="center")
        self.tabela.column("cpu2", width=160, anchor="center")
        self.tabela.column("memoria", width=160, anchor="center")
        self.tabela.column("discos", width=120, anchor="center")

        self.atualizar_dados()

    def atualizar_dados(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for processo in self.app.processos:
            if(isinstance(processo, ProcessoIO)):
                cpu1 = processo.tempo_fase1_cpu
                io = processo.tempo_fase_io
                cpu2 = processo.tempo_fase2_cpu
            else:
                cpu1 = processo.tempo_cpu
                io = "-"
                cpu2 = "-"
            
            num_prioridade = getattr(processo, 'prioridade', '-')
            discos = getattr(processo, 'discos', getattr(processo, 'qtd_discos', '-'))

            prioridade = "Tempo real" if num_prioridade == 0 else "Usuário"
            
            self.tabela.insert("", "end", values=(
                processo.id,
                prioridade, 
                cpu1,
                io,
                cpu2,
                processo.tam,
                discos 
            ))


class processSchedulingScreen(Frame):

    def __init__(self, master, app):
        super().__init__(master, bg="#000000")
        self.app = app
        self.pack(fill=BOTH, expand=True)
        
        self.tique_atual = 1
        self.historico: list[dict] = []

        # Botões
        frame_botoes = Frame(self, bg="#000000")
        frame_botoes.pack(pady=30)

        Button(frame_botoes, text="▶️",
               bg="#05a8bc", fg="#000000", relief=FLAT,
               activebackground="#00FF37", activeforeground="#111111",
               font=("Courier", 14, "bold"),
               command=self._tick
               ).pack(side=LEFT, padx=10)

        Button(frame_botoes, text="⏩",
               bg="#05a8bc", fg="#000000", relief=FLAT,
               activebackground="#D9FF00", activeforeground="#111111",
               font=("Courier", 14, "bold"),
               command=self._escalonar_tudo
               ).pack(side=LEFT, padx=10)
        
        Button(frame_botoes, text="🔁",
                bg="#05a8bc", fg="#ffffff", relief=FLAT,
                activebackground="#cc4444", activeforeground="#ffffff",
                font=("Courier", 14, "bold"),
                command=self._resetar
                ).pack(side=LEFT, padx=10)
        
        container_gantt = Frame(self, bg="#000000")
        container_gantt.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # --- BARRA DE MEMÓRIA PRINCIPAL ---
        frame_memoria = Frame(self, bg="#000000")
        frame_memoria.pack(fill=X, padx=10, pady=(10, 0))
        
        Label(frame_memoria, text="Memória Principal (32000)", bg="#000000", fg="#07D2EC",
              font=("Courier", 14, "bold")).pack(anchor="w")
        
        self.canvas_memoria = Canvas(frame_memoria, bg="#111111", height=30, 
                                     highlightthickness=1, highlightbackground="#07D2EC")
        self.canvas_memoria.pack(fill=X, pady=5)
        
        self.canvas_memoria.bind("<Configure>", lambda e: self._atualizar_memoria())

        # --- LABEL E EVENTOS DE HOVER ---
        self.label_info_memoria = Label(frame_memoria, text="Passe o mouse sobre a barra para ver os detalhes", 
                                        bg="#000000", fg="#aaaaaa", font=("Courier", 10))
        self.label_info_memoria.pack(anchor="w")

        self.canvas_memoria.tag_bind("bloco", "<Enter>", self._hover_memoria_entrar)
        self.canvas_memoria.tag_bind("bloco", "<Leave>", self._hover_memoria_sair)

        style = Style()
        style.theme_use("clam")
        style.configure("Custom.Horizontal.TScrollbar",
                        background="#07D2EC", troughcolor="#111111",
                        bordercolor="#000000", arrowcolor="#111111",
                        lightcolor="#07D2EC", darkcolor="#05a8bc")
        
        style.map("Custom.Horizontal.TScrollbar", background=[("active", "#05a8bc")])

        scrollbar = TtkScrollbar(container_gantt, orient=HORIZONTAL, style="Custom.Horizontal.TScrollbar")
        scrollbar.pack(side=BOTTOM, fill=X)

        self.canvas_gantt = Canvas(container_gantt, bg="#000000",
                                    yscrollcommand=None, xscrollcommand=scrollbar.set,
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
                font=("Courier", 14, "bold")).grid(row=i+1, column=0, padx=(0, 5), pady=5)
            
        frame_inferior = Frame(self, bg="#000000")
        frame_inferior.pack(fill=BOTH, expand=True, padx=10, pady=20)

        frame_filas = Frame(frame_inferior, bg="#111111")
        frame_filas.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

        Label(frame_filas, text="Estado das Filas", bg="#111111", fg="#07D2EC",
              font=("Courier", 16, "bold")).pack(anchor="w", padx=10, pady=10)
        
        self.label_novos = Label(frame_filas, text="Novos (Aguardando Memória): []",
                                 bg="#111111", fg="#ff0000", font=("Courier", 14, "bold"))
        self.label_novos.pack(anchor="w", padx=10, pady=3)

        self.label_tempo_real = Label(frame_filas, text="Tempo Real (FCFS): []",
                                      bg="#111111", fg="#07D2EC", font=("Courier", 14))
        self.label_tempo_real.pack(anchor="w", padx=10, pady=3) 

        # --- A CORREÇÃO ENTRA AQUI ---
        self.labels_usuario = []
        for i in range(3):
            lbl = Label(frame_filas, text=f"Usuário Fila {i}: []",
                        bg="#111111", fg="#07D2EC", font=("Courier", 14))
            lbl.pack(anchor="w", padx=10, pady=3)
            self.labels_usuario.append(lbl)

        self.label_bloqueados = Label(frame_filas, text="Bloqueados: []",
                                      bg="#111111", fg="#07D2EC", font=("Courier", 14))
        self.label_bloqueados.pack(anchor="w", padx=10, pady=3)

        self.label_finalizados = Label(frame_filas, text="Finalizados: []",
                                       bg="#111111", fg="#07D2EC", font=("Courier", 14))
        self.label_finalizados.pack(anchor="w", padx=10, pady=3)

        self.label_dma = Label(frame_filas, text="DMA (discos): []",
                       bg="#111111", fg="#07D2EC", font=("Courier", 14))
        self.label_dma.pack(anchor="w", padx=10, pady=3)

        self.label_dma_espera = Label(frame_filas, text="DMA (fila de espera): []",
                                    bg="#111111", fg="#07D2EC", font=("Courier", 14))
        self.label_dma_espera.pack(anchor="w", padx=10, pady=(3, 10)) 

        frame_logs = Frame(frame_inferior, bg="#111111")
        frame_logs.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))

        Label(frame_logs, text="Histórico de Eventos", bg="#111111", fg="#07D2EC",
              font=("Courier", 16, "bold")).pack(anchor="w", padx=10, pady=10)

        self.txt_logs = Text(frame_logs, bg="#0a0a0a", fg="#07D2EC",
                             insertbackground="#07D2EC", font=("Courier", 13),
                             relief=FLAT, height=10, state=DISABLED)
        self.txt_logs.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))

    def _atualizar_memoria(self):
        self.canvas_memoria.delete("all")
        
        # Verifica se a memória existe no SO
        if not hasattr(self.app.so, 'memoria_principal'):
            return
            
        mem = self.app.so.memoria_principal.alocacao
        tam_total = len(mem)
        largura_canvas = self.canvas_memoria.winfo_width()
        
        if largura_canvas <= 1:
            return 
            
        segmentos = []
        bloco_atual = mem[0]
        tamanho_atual = 0
        
        for p in mem:
            if p == bloco_atual:
                tamanho_atual += 1
            else:
                segmentos.append((bloco_atual, tamanho_atual))
                bloco_atual = p
                tamanho_atual = 1
                
        if tamanho_atual > 0:
            segmentos.append((bloco_atual, tamanho_atual))
            
        x_atual = 0
        for pid, tamanho in segmentos:
            largura_bloco = (tamanho / tam_total) * largura_canvas
            
            if pid is None:
                cor_fundo = "#111111"
                texto = ""
            else:
                cor_fundo = "#05a8bc"
                texto = f"P{pid}"
                
            self.canvas_memoria.create_rectangle(
                x_atual, 0, x_atual + largura_bloco, 30, 
                fill=cor_fundo, outline="#000000",
                tags=("bloco", str(pid), str(tamanho)) 
            )
            
            if pid is not None and largura_bloco > 30:
                self.canvas_memoria.create_text(
                    x_atual + largura_bloco / 2, 15, 
                    text=texto, fill="#000000", font=("Courier", 10, "bold")
                )
                
            x_atual += largura_bloco

    # --- NOVOS MÉTODOS DE HOVER ---
    def _hover_memoria_entrar(self, event):
        item = self.canvas_memoria.find_withtag("current")
        if item:
            tags = self.canvas_memoria.gettags(item[0])
            if len(tags) >= 3:
                pid = tags[1]
                tamanho = tags[2]
                if pid == "None":
                    self.label_info_memoria.config(text=f"Espaço Livre | Tamanho: {tamanho} unidades", fg="#aaaaaa")
                else:
                    self.label_info_memoria.config(text=f"Processo PID: {pid} | Tamanho: {tamanho} unidades", fg="#07D2EC")

    def _hover_memoria_sair(self, event):
        self.label_info_memoria.config(text="Passe o mouse sobre a barra para ver os detalhes", fg="#aaaaaa")

    def _tick(self):
        so = self.app.so

        snapshot = so.tick()  

        quantums_atuais = {}
        for cpu_id, cpu in enumerate(so.cpus):
            if cpu.estado.name == "Ocupado" and cpu.processo and getattr(cpu.processo, 'prioridade', 0) != 0:
                quantums_atuais[cpu_id] = getattr(cpu, 'quantum', '?') 
            else:
                quantums_atuais[cpu_id] = "-" 

        self.historico.append(snapshot)
        self._adicionar_coluna_gantt(self.tique_atual, snapshot, quantums_atuais)
        
        if hasattr(so, 'logs') and so.logs:
            self.txt_logs.config(state="normal")
            for msg in so.logs:
                self.txt_logs.insert("end", f"[Tique {self.tique_atual}] {msg}\n")
            self.txt_logs.insert("end", "\n")
            self.txt_logs.config(state="disabled")
            self.txt_logs.see("end") 
            so.logs.clear() 

        self.tique_atual += 1
        self._atualizar_filas()
        self._atualizar_memoria()

        self.canvas_gantt.update_idletasks()
        self.canvas_gantt.xview_moveto(1.0)

    def _escalonar_tudo(self):
        if self.app.so.tem_processos_pendentes():
            self._tick()
            self.after(50, self._escalonar_tudo)

    def _adicionar_coluna_gantt(self, tique: int, snapshot: dict, quantums_atuais: dict):
        Label(self.frame_gantt, text=str(tique), bg="#000000", fg="#07D2EC",
              font=("Courier", 14, "bold"), width=9, anchor="center"
              ).grid(row=0, column=tique + 1, padx=2)
        
        for cpu_id in range(4):
            pid = snapshot.get(cpu_id)
            q = quantums_atuais.get(cpu_id, "-")
            
            if pid is not None:
                if q != "-":
                    texto = f"P:{pid}\nQ:{q}"
                else:
                    texto = f"P:{pid}\n(-)"
            else:
                texto = ""
            
            cor_bg = "#07D2EC" if pid is not None else "#0a0a0a"
            cor_fg = "#000000" if pid is not None else "#07D2EC" 

            Label(self.frame_gantt, text=texto,
                  bg=cor_bg, fg=cor_fg,
                  font=("Courier", 14, "bold"), width=9, height=2, anchor="center", 
                  relief=RIDGE
                  ).grid(row=cpu_id + 1, column=tique + 1, padx=2, pady=2)

    def _atualizar_filas(self):
        esc = self.app.so.escalonador
        dma = self.app.so.dma

        ids_novos = [p.id for p in esc.novos]
        self.label_novos.config(text=f"Novos (Aguardando Memória): {ids_novos}")

        ids_tr = [p.id for p in esc.fila_processos_tempo_real.fila]
        self.label_tempo_real.config(text=f"Tempo Real (FCFS): {ids_tr}")

        for i in range(3):
            ids = [p.id for p in esc.fila_processos_usuario.fila[i]]
            self.labels_usuario[i].config(text=f"Usuário Fila {i}: {ids}")

        ids_bloq = [p.id for p in esc.bloqueados]
        self.label_bloqueados.config(text=f"Bloqueados: {ids_bloq}")

        ids_fin = [p.id for p in esc.finalizados]
        self.label_finalizados.config(text=f"Finalizados: {ids_fin}")

        ids_discos = [p.id if p is not None else "-" for p in dma.discos]
        self.label_dma.config(text=f"DMA (discos): {ids_discos}")

        ids_espera = [p.id for p in dma.fila_espera]
        self.label_dma_espera.config(text=f"DMA (fila de espera): {ids_espera}")
        
    def _resetar(self):
        self.app.resetar()