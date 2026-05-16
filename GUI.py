from tkinter import *
from tkinter.ttk import Treeview 
from tkinter.ttk import Style
class Application:

    def __init__(self):
        self.window = Tk() #cria a janela
        #Configurações da janela
        self.window.title("Escalonador de Processos") #nome da janela
        self.window.geometry('680x480') #tamanho da janela ( ͡° ͜ʖ ͡°) 
        icon = PhotoImage(file = "icon.png") #ícone da janela
        self.window.iconphoto(True, icon) #ainda o icone da janela
        self.window.config(bg="#000000") #Etnia da janela ¯\_(ツ)_/¯

        
        self.window.columnconfigure(0, weight=0)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=1)

        #Barra lateral
        self.barra = Frame(self.window, bg="#111111", width=180)
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
            self.barra.config(width=180)
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

        #ID do processo
        Label(self, text="PID", bg="#000000", fg="#07D2EC", font=("Courier", 10)).grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.entry_pid = Entry(self, bg="#111111", fg="#07D2EC", insertbackground="#07D2EC")
        self.entry_pid.grid(row=1, column=0, padx=10, pady=8, sticky="w")

        #Tempo CPU 1
        Label(self, text="Tempo CPU 1", bg="#000000", fg="#07D2EC", font=("Courier", 10)).grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.entry_cpu1 = Entry(self, bg="#111111", fg="#07D2EC", insertbackground="#07D2EC")
        self.entry_cpu1.grid(row=3, column=0, padx=10, pady=8, sticky="w")

        #Tempo CPU 2
        Label(self, text="Tempo CPU 2", bg="#000000", fg="#07D2EC", font=("Courier", 10)).grid(row=2, column=1, padx=10, pady=8, sticky="w")
        self.entry_cpu2 = Entry(self, bg="#111111", fg="#07D2EC", insertbackground="#07D2EC")
        self.entry_cpu2.grid(row=3, column=1, padx=10, pady=8, sticky="w")

        #Tempo I/O
        Label(self, text="Tempo I/O", bg="#000000", fg="#07D2EC", font=("Courier", 10)).grid(row=4, column=0, padx=10, pady=8, sticky="w")
        self.entry_io = Entry(self, bg="#111111", fg="#07D2EC", insertbackground="#07D2EC")
        self.entry_io.grid(row=5, column=0, padx=10, pady=8, sticky="w")

        #Tamanho em memória
        Label(self, text="Tamanho em memória", bg="#000000", fg="#07D2EC", font=("Courier", 10)).grid(row=4, column=1, padx=10, pady=8, sticky="w")
        self.entry_memoria = Entry(self, bg="#111111", fg="#07D2EC", insertbackground="#07D2EC")
        self.entry_memoria.grid(row=5, column=1, padx=10, pady=8, sticky="w")

        #Botão :D
        botao = Button(self, text="Salvar", command=self.processMaker, bg="#05a8bc", fg="#000000",
                       relief=FLAT, activebackground="#07D2EC", activeforeground="#111111").grid(row=6, column=0, columnspan=2, pady=20)


    def processMaker(self):
        print("Salvando processo...")
        numero = self.entry_pid.get()
        tempo_cpu1 = self.entry_cpu1.get()
        tempo_cpu2 = self.entry_cpu2.get()
        tempo_io = self.entry_io.get()
        tamanho_memoria = self.entry_memoria.get()
        print(f"infos: {numero} {tempo_cpu1} {tempo_cpu2} {tempo_io} {tamanho_memoria}")
        
        try:
            with open("entrada.txt", "a") as f:
                f.write(f"{numero}, {tempo_cpu1}, {tempo_io}, {tempo_cpu2}, {tamanho_memoria}\n")
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

        tabela.column("pid", width=85)
        tabela.column("cpu1", width=85)
        tabela.column("io", width=85)
        tabela.column("cpu2", width=85)
        tabela.column("memoria", width=160)

        try:
            with open("entrada.txt", "r") as f:
                for linha in f.readlines():
                    valores = linha.strip().split(",")
                    tabela.insert("", END, values=valores)
        except Exception as e:
            print(f"Erro ao ler processos: {e}")

class processSchedulingScreen(Frame):

    def __init__(self, master, app):
        super().__init__(master, bg="#000000")
        self.app = app
        self.pack(expand=True)
        Label(self, text="Em desenvolvimento...", bg="#000000", fg="#07D2EC", font=("Courier", 14, "bold")).pack(pady=20)
