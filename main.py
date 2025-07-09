import tkinter as tk
from tkinter import messagebox
import bcrypt
from bd import conectar

from bd import conectar

def buscar_setores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome_setor FROM setores")
    setores = cursor.fetchall()
    conn.close()
    return setores  # Lista de tuplas (id, nome)

setores_lista = buscar_setores()
setores_dict = {nome: id for id, nome in setores_lista}
nomes_setores = list(setores_dict.keys())  # Apenas os nomes para mostrar no menu

# Função para limpar os campos após o cadastro
def limpar_campos():
    entry_nome.delete(0,tk.END)
    entry_email.delete(0,tk.END)
    entry_usuario.delete(0,tk.END)
    entry_senha.delete(0,tk.END)
    var_setor.set(nomes_setores[0])

def cadastrar_usuario():
    nome = entry_nome.get()
    email = entry_email.get()
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    setor_nome = var_setor.get()
    setor_id = setores_dict.get(setor_nome)
    perfil_id = 1  # padrão colaborador
    cargo = '1'

    if not nome or not email or not usuario or not senha or not setor_id:
        messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
        return

    senha_criptografada = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO colaboradores (nome, email, usuario, senha, cargo, setor_id, perfil_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, email, usuario, senha_criptografada, cargo, setor_id, perfil_id))

        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        limpar_campos()

    except Exception as e:
        messagebox.showerror("Erro", str(e))

app = tk.Tk()
app.title("Cadastro de Usuário")

# Setores possíveis (ENUM do banco)
var_setor = tk.StringVar(value=nomes_setores[0])
menu_setor = tk.OptionMenu(app, var_setor, *nomes_setores)

tk.Label(app, text="Nome:").grid(row=0, column=0, sticky='e')
entry_nome = tk.Entry(app)
entry_nome.grid(row=0, column=1)

tk.Label(app, text="Email:").grid(row=1, column=0, sticky='e')
entry_email = tk.Entry(app)
entry_email.grid(row=1, column=1)

tk.Label(app, text="Usuário:").grid(row=2, column=0, sticky='e')
entry_usuario = tk.Entry(app)
entry_usuario.grid(row=2, column=1)

tk.Label(app, text="Senha:").grid(row=3, column=0, sticky='e')
entry_senha = tk.Entry(app, show="*")
entry_senha.grid(row=3, column=1)

tk.Label(app, text="Setor:").grid(row=4, column=0, sticky='e')
menu_setor = tk.OptionMenu(app, var_setor, *nomes_setores)
menu_setor.grid(row=4, column=1)

btn_cadastrar = tk.Button(app, text="Cadastrar", command=cadastrar_usuario)
btn_cadastrar.grid(row=5, column=0, columnspan=2, pady=10)

app.mainloop()

