from tkinter import *

class Application:
    def __init__(self):
        self.window = Tk()
        Label(self.window, text="PID").grid(row=0, column=0)
        self.entry_pid = Entry(self.window)
        self.entry_pid.grid(row=0, column=1)
        Label(self.window, text="Tempo CPU 1").grid(row=1, column=0)
        self.entry_cpu1 = Entry(self.window)
        self.entry_cpu1.grid(row=1, column=1)
        Label(self.window, text="Tempo CPU 2").grid(row=2, column=0)
        self.entry_cpu2 = Entry(self.window)
        self.entry_cpu2.grid(row=2, column=1)
        Label(self.window, text="Tempo I/O").grid(row=3, column=0)
        self.entry_io = Entry(self.window)
        self.entry_io.grid(row=3, column=1)
        Label(self.window, text="Tamanho em memória").grid(row=4, column=0)
        self.entry_memoria = Entry(self.window)
        self.entry_memoria.grid(row=4, column=1)

        #Configurações da janela
        self.window.title("Escalonador de Processos") #nome da janela
        self.window.geometry('680x480') #tamanho da janela ( ͡° ͜ʖ ͡°) 
        icon = PhotoImage(file = "icon.png") #ícone da janela
        self.window.iconphoto(True, icon) #ainda o icone da janela
        self.window.config(bg="#000000") #Etnia da janela ¯\_(ツ)_/¯

        #Botão :D
        botao = Button(self.window, text="Salvar", command=self.processMaker).grid(row=6, column=1)

        self.window.mainloop()
        
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
