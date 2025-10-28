import tkinter as tk
from tkinter import HORIZONTAL, ttk, messagebox
import time
import threading
import re

class DadosBackup:
    def __init__(self, nome_usuario):
        self.nome_usuario = nome_usuario

class SistemaBackup:
    def __init__(self, tela_main):
        self.tela_main = tela_main
        self.tela_main.title("Sistema de Backup")
        self.tela_main.geometry("350x125")
        self.tela_main.configure(bg="#fad0dd")
        self.tela_main.resizable(False, False)
        self.tela_main.grid_columnconfigure(0, weight=1)
        self.tela_main.grid_columnconfigure(1, weight=1)


        self.progresso_valor = tk.IntVar()
        self.progresso_valor.set(0)
        
        self.ui()

    def ui(self):

        # Texto
        self.LabelUser = tk.Label(self.tela_main, text="INFORME O NOME DE USUÁRIO: ")
        self.LabelUser.grid(row=0, column=0, columnspan=2, sticky='', pady=(10, 5))
        self.LabelUser.configure(bg="#fad0dd")

        # Caixa de entrada
        self.EntryUser = tk.Entry(self.tela_main, justify='center')
        self.EntryUser.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=(0, 5))
        
        
        # Botões
        self.ButtonS = tk.Button(self.tela_main, text="Iniciar", command=self.iniciar_backup)
        self.ButtonS.grid(row=3, column=0, pady=5, padx=5)

        self.ButtonN = tk.Button(self.tela_main, text="Cancelar", command=self.cancelar_backup)
        self.ButtonN.grid(row=3, column=1, pady=5, padx=5)
        
        # Barra de Progresso
        self.BarraProgresso = ttk.Progressbar(self.tela_main, 
            orient=HORIZONTAL, 
            length=330, 
            mode="determinate", 
            variable=self.progresso_valor
        )

    def validacao_nome(self, nome):
    
        padrao = r'^[a-zA-Z][a-zA-A.]{2,19}$'
        
        if not nome:
            return False, "O nome de usuário não pode estar vazio."
        
        if not re.match(padrao, nome):
            return False, "Nome inválido!\n\n" \
                        " ex) joao.silva "
        
        return True, None



    def mostrar_barra(self, mostrar=True):
        """Alterna a visibilidade da barra de progresso."""
        if mostrar:
            # Remove outros elementos e mostra a barra
            self.LabelUser.grid_remove()
            self.EntryUser.grid_remove()
            self.ButtonS.grid_remove()
            self.ButtonN.grid_remove()
            
            # Mostra a barra
            self.BarraProgresso.grid(row=0, column=0, columnspan=2, padx=10, pady=20, sticky='ew')
            self.tela_main.geometry("350x80")
            
        else:
            # Oculta a barra e restaura a tela inicial
            self.BarraProgresso.grid_remove()
            self.LabelUser.grid()
            self.EntryUser.grid()
            self.ButtonS.grid()
            self.ButtonN.grid()
            self.tela_main.geometry("350x125")

   
    def iniciar_backup(self):
        nome_usuario = self.EntryUser.get()
        
        # Validação do nome de usuário
        if not nome_usuario:
            messagebox.showerror("Erro", "Informe o nome de usuário.")
            return
        
        # Validação com regex
        valido, erro = self.validacao_nome(nome_usuario)
        if not valido:
            messagebox.showerror("Erro", erro)
            return

        # Prepara a UI para o backup
        self.mostrar_barra(mostrar=True)
        self.BarraProgresso.config(maximum=100)
        self.progresso_valor.set(0)
        
        # Inicia a tarefa de backup em uma thread separada
        self.backup_thread = threading.Thread(target=self.executar_backup_simulado, args=(nome_usuario,))
        self.backup_thread.start()

    def executar_backup_simulado(self, nome_usuario):
        #Simula o processo de backup e atualiza a barra de progresso."""
        print(f"Iniciando backup para: {nome_usuario}")
        
        # Simulação de 10 passos
        num_passos = 10 
        
        for passo in range(1, num_passos + 1):
            time.sleep(0.5)
            
            # Calcula o percentual e atualiza a variável de controle
            percentual = int((passo / num_passos) * 100)
            self.progresso_valor.set(percentual)
            
            # Atualiza a barra
            self.tela_main.update_idletasks()
            
            print(f"Passo {passo} de {num_passos} concluído ({percentual}%)")

        # Chama a função de finalização
        self.tela_main.after(0, self.finalizar_backup)

    def finalizar_backup(self):
      
        messagebox.showinfo("Sucesso", "Backup concluído com sucesso!")
        self.mostrar_barra(mostrar=False)
        self.progresso_valor.set(0)

    def cancelar_backup(self):
        """Cancela o backup e restaura a UI."""
        if hasattr(self, 'backup_thread') and self.backup_thread.is_alive():
            messagebox.showwarning("Cancelado", "O backup foi cancelado.")
        
        self.mostrar_barra(mostrar=False)
        self.progresso_valor.set(0)

      
        
  
if __name__ == '__main__':
    tela_main = tk.Tk()
    app = SistemaBackup(tela_main)
    tela_main.mainloop()
