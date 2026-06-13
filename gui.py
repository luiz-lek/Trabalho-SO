from tkinter import *
from tkinter.ttk import Treeview 
from tkinter.ttk import Style
from processos import *


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
        self.barra = Frame(self.window, bg="#111111", width=(self.largura/6))
        self.barra.pack(side=LEFT, fill=Y)
        self.barra.pack_propagate(False)
        self.barra_aberta = True

        #Botão para retrair a barra lateral
        self.btn_retrair = Button(self.barra, text="x",
       bg="#111111", fg="#07D2EC", activebackground="#07D2EC", activeforeground="#111111",
       relief=FLAT, font=("Courier", 14),
       highlightthickness=0
       )
        self.btn_retrair.pack(pady=10)
        self.btn_retrair.bind("<ButtonRelease-1>", lambda e: self.retrair_barra())
        
        #Botões de navegação da barra lateral
        Button(self.barra, text="⚙ Criar Processo",
       bg="#111111", fg="#07D2EC", activebackground="#07D2EC", activeforeground="#111111",
       relief=FLAT, anchor="w",
       font=("Courier", 10),
       command=lambda: self.mostrar_tela(processMakingScreen), highlightthickness=0
       ).pack(fill=X, padx=10, pady=5)

        Button(self.barra, text="▤ Listar Processos",
       bg="#111111", fg="#07D2EC", activebackground="#07D2EC", activeforeground="#111111",
       relief=FLAT, anchor="w",
       font=("Courier", 10),
       command=lambda: self.mostrar_tela(processListScreen), highlightthickness=0
       ).pack(fill=X, padx=10, pady=5)

        Button(self.barra, text="▶ Escalonador",
       bg="#111111", fg="#07D2EC", activebackground="#07D2EC", activeforeground="#111111",
       relief=FLAT, anchor="w",
       font=("Courier", 10),
       command=lambda: self.mostrar_tela(processSchedulingScreen), highlightthickness=0
       ).pack(fill=X, padx=10, pady=5)

        
        self.conteudo = Frame(self.window, bg="#0a0a0a")
        self.conteudo.pack()

        self.mostrar_tela(processMakingScreen) #mostra a tela principal
        self.window.mainloop()

    def mostrar_tela(self, screen):
        for widget in self.conteudo.winfo_children():
            widget.destroy()
        screen(self.conteudo, self)

    def retrair_barra(self):
        print("estado antes:", self.barra_aberta)
        if self.barra_aberta:
            self.barra.config(width=50)
            self.btn_retrair.config(text="☰", font=("Courier", 14, "bold"))
            self.barra_aberta = False
        else:
            self.barra.config(width=(self.largura/6))
            self.btn_retrair.config(text="x", font=("Courier", 14, "bold"))
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

        #Tempo CPU 1
        Label(self, text="Tempo CPU 1", bg="#000000", fg="#07D2EC", 
            font=("Courier", 10)).grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.entry_cpu1 = Entry(self, bg="#111111", fg="#07D2EC", insertbackground="#07D2EC")
        self.entry_cpu1.grid(row=3, column=0, padx=10, pady=8, sticky="w")

        #Tempo CPU 2
        Label(self, text="Tempo CPU 2", bg="#000000", fg="#07D2EC", 
            font=("Courier", 10)).grid(row=2, column=1, padx=10, pady=8, sticky="w")
        self.entry_cpu2 = Entry(self, bg="#111111", fg="#07D2EC", insertbackground="#07D2EC")
        self.entry_cpu2.grid(row=3, column=1, padx=10, pady=8, sticky="w")

        #Tempo I/O
        Label(self, text="Tempo I/O", bg="#000000", fg="#07D2EC", 
            font=("Courier", 10)).grid(row=4, column=0, padx=10, pady=8, sticky="w")
        self.entry_io = Entry(self, bg="#111111", fg="#07D2EC", insertbackground="#07D2EC")
        self.entry_io.grid(row=5, column=0, padx=10, pady=8, sticky="w")

        #Tamanho em memória
        Label(self, text="Tamanho em memória", bg="#000000", 
            fg="#07D2EC", font=("Courier", 10)).grid(row=4, column=1, padx=10, pady=8, sticky="w")
        self.entry_memoria = Entry(self, bg="#111111", fg="#07D2EC", insertbackground="#07D2EC")
        self.entry_memoria.grid(row=5, column=1, padx=10, pady=8, sticky="w")

        #Botão :D
        botao = Button(self, text="Salvar", command=self.processMaker, bg="#05a8bc", fg="#000000",
                       relief=FLAT, activebackground="#07D2EC", 
                       activeforeground="#111111").grid(row=6, column=0, columnspan=2, pady=20)


    def processMaker(self):
        try:
            processo = self.app.despachante.criar_processo(
                int(self.entry_cpu1.get()),
                int(self.entry_cpu2.get()),
                int(self.entry_io.get()),
                int(self.entry_memoria.get())
            )
            self.app.processos.append(processo)
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
        self.pack(expand=True)
        Label(self, text="Em desenvolvimento...", bg="#000000", fg="#07D2EC", font=("Courier", 14, "bold")).pack(pady=20)
