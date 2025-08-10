# # Revisado a conexão com o bd
# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog
# from tkcalendar import DateEntry
# from utils.db import Database
# import logging
# import csv
# from datetime import datetime
# from mysql.connector import Error, InterfaceError
#
# class HistoricoAtividadesView:
#     def __init__(self, master, colaborador):
#         self.master = master  # Janela raiz (tk.Tk) de HomeView
#         self.colaborador = colaborador
#         self.selecionados = set()
#         self.limite_linhas = tk.IntVar(value=50)
#
#         # Cria o frame de conteúdo dentro da janela raiz
#         self.frame_conteudo = tk.Frame(self.master, bg='#f8f9fa', padx=10, pady=5)
#         self.frame_conteudo.pack(fill='both', expand=True)
#
#         self._configurar_estilos()
#         self._setup_ui()
#         self._carregar_filtros()
#         self._carregar_atividades()
#
#     def _configurar_estilos(self):
#         """Configura os estilos visuais para melhor visibilidade"""
#         self.style = ttk.Style()
#         self.style.configure("Treeview", font=('Segoe UI', 10), rowheight=25,
#                             background="#ffffff", fieldbackground="#ffffff",
#                             bordercolor="#dddddd", borderwidth=1)
#         self.style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'),
#                             background='#e1e1e1', relief='flat', padding=3)
#         self.style.map("Treeview", background=[('selected', '#e6f3ff')],
#                       foreground=[('selected', 'black')])
#         self.style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
#
#         # Estilos para botões menores
#         self.style.configure("TButton", font=('Segoe UI', 9, 'bold'), padding=4)
#         self.style.configure("Custom.TButton", background="#007bff", foreground="white",
#                             padding=4)
#         self.style.map("Custom.TButton",
#                       background=[('active', '#0056b3'), ('!disabled', '#007bff')],
#                       foreground=[('active', 'white'), ('!disabled', 'white')])
#
#     def _setup_ui(self):
#         ttk.Label(self.frame_conteudo, text="Histórico de Atividades",
#                   font=('Segoe UI', 18, 'bold')).pack(pady=(0, 8))
#
#         filtro_frame = tk.Frame(self.frame_conteudo, bg='#f8f9fa')
#         filtro_frame.pack(fill='x', pady=(0, 8))
#
#         self.var_tipo = tk.StringVar()
#         self.var_data_ini = tk.StringVar()
#         self.var_data_fim = tk.StringVar()
#         self.var_ticket = tk.StringVar()
#         self.var_setor = tk.StringVar()
#         self.var_colaborador = tk.StringVar()
#
#         # Tipo
#         ttk.Label(filtro_frame, text="Tipo:").pack(side='left')
#         self.filtro_tipo = ttk.Combobox(filtro_frame, textvariable=self.var_tipo,
#                                         state='readonly')
#         self.filtro_tipo.pack(side='left', padx=3)
#
#         # De (Data Inicial)
#         ttk.Label(filtro_frame, text="De:").pack(side='left')
#         self.filtro_data_ini = DateEntry(filtro_frame, textvariable=self.var_data_ini,
#                                          date_pattern='yyyy-MM-dd', background='darkblue',
#                                          foreground='white', borderwidth=1, width=10)
#         self.filtro_data_ini.pack(side='left', padx=3)
#         self.filtro_data_ini.bind("<<DateEntrySelected>>",
#                                   lambda e: self._carregar_atividades())
#
#         # Até (Data Final)
#         ttk.Label(filtro_frame, text="Até:").pack(side='left')
#         self.filtro_data_fim = DateEntry(filtro_frame, textvariable=self.var_data_fim,
#                                          date_pattern='yyyy-MM-dd', background='darkblue',
#                                          foreground='white', borderwidth=1, width=10)
#         self.filtro_data_fim.pack(side='left', padx=3)
#         self.filtro_data_fim.bind("<<DateEntrySelected>>",
#                                   lambda e: self._carregar_atividades())
#
#         # Ticket
#         ttk.Label(filtro_frame, text="Ticket:").pack(side='left')
#         ttk.Entry(filtro_frame, textvariable=self.var_ticket).pack(side='left', padx=3)
#
#         # Setor
#         ttk.Label(filtro_frame, text="Setor:").pack(side='left')
#         self.filtro_setor = ttk.Combobox(filtro_frame, textvariable=self.var_setor,
#                                          state='readonly')
#         self.filtro_setor.pack(side='left', padx=3)
#
#         # Colaborador
#         ttk.Label(filtro_frame, text="Colaborador:").pack(side='left')
#         self.filtro_colaborador = ttk.Combobox(filtro_frame, textvariable=self.var_colaborador,
#                                                state='readonly')
#         self.filtro_colaborador.pack(side='left', padx=3)
#
#         # Botões de filtro
#         ttk.Button(filtro_frame, text="Filtrar", style="Custom.TButton",
#                    command=self._carregar_atividades).pack(side='left', padx=5)
#         ttk.Button(filtro_frame, text="Limpar Filtros", style="Custom.TButton",
#                    command=self._limpar_filtros).pack(side='left', padx=3)
#
#         # Botões de ação
#         btn_frame = tk.Frame(self.frame_conteudo, bg='#f8f9fa')
#         btn_frame.pack(fill='x', pady=(0, 5))
#         tk.Button(btn_frame, text="Excluir", bg="#dc3545", fg="white",
#                   command=self._excluir_selecionados).pack(side='left', padx=3)
#         tk.Button(btn_frame, text="Editar", bg="#ffc107", fg="black",
#                   command=self._editar_selecionado).pack(side='left', padx=3)
#         tk.Button(btn_frame, text="Ver Detalhes", bg="#6c757d", fg="white",
#                   command=self._ver_detalhes).pack(side='left', padx=3)
#
#         # Frame para Treeview com barra de rolagem
#         tree_frame = tk.Frame(self.frame_conteudo)
#         tree_frame.pack(fill='both', expand=True, pady=(5, 0))
#
#         self.scrollbar = tk.Scrollbar(tree_frame)
#         self.scrollbar.pack(side='right', fill='y')
#
#         columns = ("id", "data", "tipo", "ticket", "descricao",
#                    "colaborador", "setor")
#         self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
#                                  height=15, selectmode='extended', style="Treeview",
#                                  yscrollcommand=self.scrollbar.set)
#         self.tree.heading("id", text="☑")
#         self.tree.column("id", width=50, anchor='center', stretch=False)
#         col_configs = [("data", "Data", 90), ("tipo", "Tipo", 110),
#                        ("ticket", "Ticket", 90), ("descricao", "Descrição", 150),
#                        ("colaborador", "Colaborador", 110), ("setor", "Setor", 110)]
#         for col, text, width in col_configs:
#             self.tree.heading(col, text=text)
#             self.tree.column(col, width=width)
#         self.tree.pack(side='left', fill='both', expand=True)
#         self.scrollbar.config(command=self.tree.yview)
#
#         # Configura o evento de clique na coluna de seleção
#         self.tree.bind("<Button-1>", self._toggle_selecao)
#
#         # Opção de limite de linhas
#         limite_frame = tk.Frame(self.frame_conteudo, bg='#f8f9fa')
#         limite_frame.pack(fill='x', pady=(5, 0))
#         ttk.Label(limite_frame, text="Linhas por página:").pack(side='left', padx=5)
#         self.combo_limite = ttk.Combobox(limite_frame, textvariable=self.limite_linhas,
#                                          values=[50, 100, 200, 300, 400], state='readonly')
#         self.combo_limite.pack(side='left', padx=5)
#         self.combo_limite.bind("<<ComboboxSelected>>", lambda e: self._carregar_atividades())
#
#         # Exportar CSV
#         export_frame = tk.Frame(self.frame_conteudo, bg='#f8f9fa')
#         export_frame.pack(fill='x', pady=(5, 5))
#         tk.Button(export_frame, text="Exportar CSV", bg="#17a2b8", fg="white",
#                   command=self._exportar_csv).pack(side='right', padx=5)
#
#     def _carregar_filtros(self):
#         """Carrega as opções disponíveis para os filtros de tipo, setor e colaborador"""
#         try:
#             with Database().get_connection() as conn:
#                 with conn.cursor(dictionary=True) as cursor:
#                     cursor.execute("SELECT nome FROM tipos_atendimento ORDER BY nome")
#                     tipos = [""] + [row['nome'] for row in cursor.fetchall()]
#                     self.filtro_tipo['values'] = tipos
#
#                     cursor.execute("SELECT nome_setor FROM setores ORDER BY nome_setor")
#                     setores = [""] + [row['nome_setor'] for row in cursor.fetchall()]
#                     self.filtro_setor['values'] = setores
#
#                     cursor.execute("SELECT nome FROM colaboradores ORDER BY nome")
#                     colaboradores = [""] + [row['nome'] for row in cursor.fetchall()]
#                     self.filtro_colaborador['values'] = colaboradores
#         except Error as e:
#             logging.error(f"Erro de banco de dados ao carregar filtros: {e}", exc_info=True)
#             messagebox.showerror("Erro", "Falha na conexão com o banco de dados")
#         except Exception as e:
#             logging.error(f"Erro ao carregar filtros: {e}", exc_info=True)
#             messagebox.showerror("Erro", f"Falha ao carregar filtros:\n{e}")
#
#     def _carregar_atividades(self):
#         try:
#             with Database().get_connection() as conn:
#                 with conn.cursor(dictionary=True) as cursor:
#                     base_query = """
#                         SELECT
#                             a.id,
#                             a.data_atendimento,
#                             t.nome AS tipo_atendimento,
#                             a.numero_atendimento,
#                             a.descricao,
#                             c.nome AS colaborador_nome,
#                             s.nome_setor
#                         FROM atividades a
#                         JOIN tipos_atendimento t ON a.tipo_atendimento_id = t.id
#                         JOIN colaboradores c ON a.colaborador_id = c.id
#                         JOIN setores s ON c.setor_id = s.id
#                     """
#                     where_clauses, params = [], []
#
#                     perfil = self.colaborador.cargo.value.lower()
#                     if perfil == 'colaborador':
#                         where_clauses.append("a.colaborador_id = %s")
#                         params.append(self.colaborador.id)
#                     elif perfil == 'gestor':
#                         where_clauses.append("s.id = %s")
#                         params.append(self.colaborador.setor_id)
#
#                     if self.var_tipo.get():
#                         where_clauses.append("t.nome = %s")
#                         params.append(self.var_tipo.get())
#
#                     if self.var_data_ini.get():
#                         data_ini = self._validar_data(self.var_data_ini.get())
#                         if data_ini:
#                             where_clauses.append("DATE(a.data_atendimento) >= %s")
#                             params.append(data_ini.isoformat())
#
#                     if self.var_data_fim.get():
#                         data_fim = self._validar_data(self.var_data_fim.get())
#                         if data_fim:
#                             where_clauses.append("DATE(a.data_atendimento) <= %s")
#                             params.append(data_fim.isoformat())
#
#                     if self.var_ticket.get():
#                         where_clauses.append("a.numero_atendimento LIKE %s")
#                         params.append(f"%{self.var_ticket.get()}%")
#
#                     if self.var_setor.get():
#                         where_clauses.append("s.nome_setor = %s")
#                         params.append(self.var_setor.get())
#
#                     if self.var_colaborador.get():
#                         where_clauses.append("c.nome = %s")
#                         params.append(self.var_colaborador.get())
#
#                     if where_clauses:
#                         base_query += " WHERE " + " AND ".join(where_clauses)
#
#                     base_query += " ORDER BY a.data_atendimento DESC LIMIT %s"
#                     params.append(self.limite_linhas.get())
#                     cursor.execute(base_query, tuple(params))
#                     resultados = cursor.fetchall()
#
#             # Limpa a treeview
#             for item in self.tree.get_children():
#                 self.tree.delete(item)
#             self.selecionados.clear()
#
#             # Configura tags para linhas alternadas
#             self.tree.tag_configure('linha_par', background='#ffffff')
#             self.tree.tag_configure('linha_impar', background='#f2f2f2')
#
#             # Preenche a treeview com os resultados
#             for index, row in enumerate(resultados):
#                 iid = str(row['id'])
#                 data_br = row['data_atendimento'].strftime('%d-%m-%Y')
#                 marcado = "☑" if iid in self.selecionados else "◻"
#                 tag_linha = 'linha_par' if index % 2 == 0 else 'linha_impar'
#
#                 self.tree.insert('', 'end', iid=iid, values=(
#                     marcado,
#                     data_br.upper(),
#                     str(row['tipo_atendimento']).upper(),
#                     str(row['numero_atendimento']).upper(),
#                     str(row['descricao']).upper(),
#                     str(row['colaborador_nome']).upper(),
#                     str(row['nome_setor']).upper()
#                 ), tags=(tag_linha,))
#
#         except Error as e:
#             logging.error(f"Erro de banco de dados ao carregar atividades: {e}", exc_info=True)
#             messagebox.showerror("Erro", "Falha na conexão com o banco de dados")
#         except InterfaceError as e:
#             logging.error(f"Erro de interface com o banco: {e}", exc_info=True)
#             messagebox.showerror("Erro", "Problema na comunicação com o banco de dados")
#         except Exception as e:
#             logging.error(f"Erro ao carregar atividades: {e}", exc_info=True)
#             messagebox.showerror("Erro", f"Falha ao carregar atividades:\n{e}")
#
#     def _toggle_selecao(self, event):
#         """Alterna a seleção de itens na tabela ao clicar na coluna de seleção."""
#         region = self.tree.identify("region", event.x, event.y)
#         if region != "cell":
#             return
#
#         column = self.tree.identify_column(event.x)
#         if column != "#1":
#             return
#
#         item = self.tree.identify_row(event.y)
#         if not item:
#             return
#
#         if item in self.selecionados:
#             self.selecionados.remove(item)
#             self.tree.set(item, "id", "◻")
#         else:
#             self.selecionados.add(item)
#             self.tree.set(item, "id", "☑")
#
#         self.tree.selection_remove(self.tree.selection())
#         if item in self.selecionados:
#             self.tree.selection_add(item)
#
#     def _exportar_csv(self):
#         """Exporta os dados da tabela para um arquivo CSV"""
#         try:
#             filepath = filedialog.asksaveasfilename(
#                 defaultextension=".csv",
#                 filetypes=[("CSV Files", "*.csv")],
#                 title="Salvar como"
#             )
#             if not filepath:
#                 return
#
#             with open(filepath, mode='w', newline='', encoding='utf-8') as f:
#                 writer = csv.writer(f, delimiter=';')
#
#                 # Cabeçalho (pula coluna de seleção)
#                 cols = list(self.tree['columns'])[1:]
#                 headers = [self.tree.heading(col)['text'] for col in cols]
#                 writer.writerow(headers)
#
#                 # Exporta apenas itens selecionados
#                 items = self.tree.selection() if self.tree.selection() else self.tree.get_children()
#                 for item in items:
#                     values = self.tree.item(item)['values'][1:]
#                     row = [
#                         v.strftime('%Y-%m-%d %H:%M:%S')
#                         if isinstance(v, datetime) else v
#                         for v in values
#                     ]
#                     writer.writerow(row)
#
#             messagebox.showinfo("Sucesso",
#                               f"Dados exportados com sucesso para:\n{filepath}")
#         except Exception as e:
#             logging.error(f"Erro ao exportar CSV: {e}", exc_info=True)
#             messagebox.showerror("Erro", f"Falha ao exportar CSV:\n{e}")
#
#     def _limpar_filtros(self):
#         """Limpa os filtros redefinindo para valores padrão"""
#         self.var_tipo.set("")
#         self.var_data_ini.set("")
#         self.var_data_fim.set("")
#         self.var_ticket.set("")
#         self.var_setor.set("")
#         self.var_colaborador.set("")
#         self._carregar_atividades()
#
#     def _excluir_selecionados(self):
#         """Exclui os itens selecionados da tabela"""
#         if not self.selecionados:
#             messagebox.showwarning("Aviso", "Nenhum item selecionado para exclusão.")
#             return
#
#         confirm = messagebox.askyesno(
#             "Confirmar Exclusão",
#             f"Tem certeza que deseja excluir {len(self.selecionados)} registro(s)?",
#             icon='warning'
#         )
#         if not confirm:
#             return
#
#         try:
#             with Database().get_connection() as conn:
#                 with conn.cursor() as cursor:
#                     ids = list(self.selecionados)
#                     placeholders = ",".join(["%s"] * len(ids))
#                     cursor.execute(
#                         f"DELETE FROM atividades WHERE id IN ({placeholders})",
#                         tuple(ids))
#                     conn.commit()
#
#             count = len(ids)
#             self.selecionados.clear()
#             self._carregar_atividades()
#             messagebox.showinfo("Sucesso",
#                               f"{count} registro(s) excluído(s) com sucesso.")
#         except Error as e:
#             logging.error(f"Erro de banco de dados ao excluir registros: {e}", exc_info=True)
#             messagebox.showerror("Erro", "Falha na conexão com o banco de dados")
#         except Exception as e:
#             logging.error(f"Erro ao excluir registros: {e}", exc_info=True)
#             messagebox.showerror("Erro", f"Falha ao excluir registros:\n{e}")
#
#     def _ver_detalhes(self):
#         """Abre a janela de detalhes da atividade selecionada."""
#         try:
#             selecionado = self.tree.selection()
#             if not selecionado:
#                 messagebox.showwarning("Aviso",
#                                      "Selecione uma atividade para ver detalhes.")
#                 return
#
#             atividade_id = int(selecionado[0])
#             from screens.detalhes_atividade_view import DetalhesAtividadeView
#
#             top = tk.Toplevel(self.master)
#             top.title("Detalhes da Atividade")
#             top.grab_set()
#             DetalhesAtividadeView(top, atividade_id)
#         except Exception as e:
#             logging.error(f"Erro ao abrir detalhes: {e}", exc_info=True)
#             messagebox.showerror("Erro", f"Não foi possível abrir detalhes:\n{e}")
#
#     def _editar_selecionado(self):
#         """Abre a janela de edição para o item selecionado."""
#         try:
#             selecionado = self.tree.selection()
#             if not selecionado:
#                 messagebox.showwarning("Aviso",
#                                      "Selecione uma atividade para editar.")
#                 return
#
#             atividade_id = int(selecionado[0])
#             from screens.editar_atividade_view import EditarAtividadeView
#
#             top = tk.Toplevel(self.master)
#             top.title("Editar Atividade")
#             top.transient(self.master)
#             top.grab_set()
#
#             EditarAtividadeView(
#                 master=top,
#                 atividade_id=atividade_id,
#                 colaborador=self.colaborador,
#                 on_save=self._carregar_atividades
#             )
#             top.wait_window()
#         except Exception as e:
#             logging.error(f"Erro ao abrir edição: {e}", exc_info=True)
#             messagebox.showerror("Erro", f"Não foi possível editar a atividade:\n{e}")
#
#     def _validar_data(self, data_str):
#         """
#         Converte string para date nos formatos:
#           - 'YYYY-MM-DD' (padrão DateEntry)
#           - 'DD-MM-YYYY'
#         Retorna date ou None se inválido.
#         """
#         formatos = ['%Y-%m-%d', '%d-%m-%Y']
#         for fmt in formatos:
#             try:
#                 return datetime.strptime(data_str, fmt).date()
#             except ValueError:
#                 continue
#
#         messagebox.showwarning(
#             "Formato inválido",
#             f"Data '{data_str}' precisa estar em aaaa-mm-dd ou dd-mm-aaaa"
#         )
#         return None
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Histórico de Atividades")
#     class MockColaborador:
#         def __init__(self):
#             self.id = 1
#             self.cargo = type('Cargo', (), {'value': 'colaborador'})()
#             self.setor_id = 1
#     app = HistoricoAtividadesView(root, MockColaborador())
#     root.mainloop()

# Versão FINAL com Pesquisa por Enter
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from utils.db import Database
import logging
import csv
from datetime import datetime
from mysql.connector import Error


class HistoricoAtividadesView:
    def __init__(self, master, colaborador):
        self.master = master
        self.colaborador = colaborador
        self.selecionados = set()
        self.todos_selecionados_state = False

        self.limite_linhas = tk.IntVar(value=50)
        self.var_contador_selecao = tk.StringVar(value="Nenhum item selecionado")

        self.frame_conteudo = ttk.Frame(self.master, style='TFrame')
        self.frame_conteudo.pack(fill='both', expand=True, padx=10, pady=5)

        self._configurar_estilos()
        self._setup_ui()
        self._carregar_filtros()
        self._carregar_atividades()

    def _configurar_estilos(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure(".", font=('Segoe UI', 10), background='#f8f9fa', foreground='#212529')
        self.style.configure("TFrame", background='#f8f9fa')
        self.style.configure("TLabel", background='#f8f9fa')
        self.style.configure("TLabelframe", background='#f8f9fa', bordercolor="#dee2e6", padding=5)
        self.style.configure("TLabelframe.Label", background='#f8f9fa', foreground="#495057",
                             font=('Segoe UI', 9, 'bold'))
        self.style.configure("Treeview", rowheight=28, fieldbackground="#ffffff")
        self.style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'), padding=5, background='#e9ecef',
                             relief='flat')
        self.style.map("Treeview.Heading", background=[('active', '#dce0e3')])
        self.style.map("Treeview", background=[('selected', '#b8d8ff')], foreground=[('selected', '#004085')])
        self.style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        self.style.configure("TButton", font=('Segoe UI', 9, 'bold'), padding=(8, 5), relief='flat', borderwidth=0)
        self.style.configure("Primary.TButton", background="#007bff", foreground="white")
        self.style.map("Primary.TButton", background=[('active', '#0056b3')])
        self.style.configure("Danger.TButton", background="#dc3545", foreground="white")
        self.style.map("Danger.TButton", background=[('active', '#c82333')])
        self.style.configure("Warning.TButton", background="#ffc107", foreground="black")
        self.style.map("Warning.TButton", background=[('active', '#e0a800')])
        self.style.configure("Secondary.TButton", background="#6c757d", foreground="white")
        self.style.map("Secondary.TButton", background=[('active', '#5a6268')])
        self.style.configure("Info.TButton", background="#17a2b8", foreground="white")
        self.style.map("Info.TButton", background=[('active', '#117a8b')])
        self.style.configure("pendente.Treeview", background="#FFFBE6")

    def _setup_ui(self):
        ttk.Label(self.frame_conteudo, text="Histórico de Atividades", font=('Segoe UI', 18, 'bold')).pack(pady=(0, 10),
                                                                                                           anchor='w')

        main_filtro_frame = ttk.Frame(self.frame_conteudo)
        main_filtro_frame.pack(fill='x', pady=(0, 10), expand=True)

        filtro_conteudo_frame = ttk.LabelFrame(main_filtro_frame, text="Filtrar por Conteúdo")
        filtro_conteudo_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))

        self.var_descricao_filtro = tk.StringVar()
        self.var_tipo = tk.StringVar()
        self.var_ticket = tk.StringVar()

        ttk.Label(filtro_conteudo_frame, text="Tipo:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.filtro_tipo = ttk.Combobox(filtro_conteudo_frame, textvariable=self.var_tipo, state='readonly', width=25)
        self.filtro_tipo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.filtro_tipo.bind("<<ComboboxSelected>>", lambda e: self._carregar_atividades())  # Filtra ao selecionar

        ttk.Label(filtro_conteudo_frame, text="Ticket:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        entry_ticket = ttk.Entry(filtro_conteudo_frame, textvariable=self.var_ticket, width=27)
        entry_ticket.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        entry_ticket.bind("<Return>", lambda e: self._carregar_atividades())  # <<< NOVO: Pesquisa com Enter

        ttk.Label(filtro_conteudo_frame, text="Descrição:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        entry_descricao = ttk.Entry(filtro_conteudo_frame, textvariable=self.var_descricao_filtro, width=27)
        entry_descricao.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        entry_descricao.bind("<Return>", lambda e: self._carregar_atividades())  # <<< NOVO: Pesquisa com Enter
        filtro_conteudo_frame.columnconfigure(1, weight=1)

        filtro_pessoas_data_frame = ttk.LabelFrame(main_filtro_frame, text="Filtrar por Pessoas e Data")
        filtro_pessoas_data_frame.pack(side='left', fill='x', expand=True)

        self.var_data_ini = tk.StringVar()
        self.var_data_fim = tk.StringVar()
        self.var_setor = tk.StringVar()
        self.var_colaborador = tk.StringVar()

        ttk.Label(filtro_pessoas_data_frame, text="Colaborador:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.filtro_colaborador = ttk.Combobox(filtro_pessoas_data_frame, textvariable=self.var_colaborador,
                                               state='readonly', width=20)
        self.filtro_colaborador.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.filtro_colaborador.bind("<<ComboboxSelected>>", lambda e: self._carregar_atividades())

        ttk.Label(filtro_pessoas_data_frame, text="Setor:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.filtro_setor = ttk.Combobox(filtro_pessoas_data_frame, textvariable=self.var_setor, state='readonly',
                                         width=20)
        self.filtro_setor.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.filtro_setor.bind("<<ComboboxSelected>>", lambda e: self._carregar_atividades())

        data_frame = ttk.Frame(filtro_pessoas_data_frame)
        data_frame.grid(row=2, column=0, columnspan=2, sticky='ew')
        ttk.Label(data_frame, text="De:").pack(side='left', padx=(5, 2))
        self.filtro_data_ini = DateEntry(data_frame, textvariable=self.var_data_ini, date_pattern='yyyy-MM-dd',
                                         width=10)
        self.filtro_data_ini.pack(side='left')
        self.filtro_data_ini.bind("<<DateEntrySelected>>", lambda e: self._carregar_atividades())

        ttk.Label(data_frame, text="Até:").pack(side='left', padx=(10, 2))
        self.filtro_data_fim = DateEntry(data_frame, textvariable=self.var_data_fim, date_pattern='yyyy-MM-dd',
                                         width=10)
        self.filtro_data_fim.pack(side='left')
        self.filtro_data_fim.bind("<<DateEntrySelected>>", lambda e: self._carregar_atividades())
        filtro_pessoas_data_frame.columnconfigure(1, weight=1)

        action_filter_frame = ttk.Frame(main_filtro_frame)
        action_filter_frame.pack(side='left', fill='y', padx=(10, 0))
        ttk.Button(action_filter_frame, text="Filtrar", style="Primary.TButton",
                   command=self._carregar_atividades).pack(fill='x', expand=True, ipady=2)
        ttk.Button(action_filter_frame, text="Limpar", style="Secondary.TButton", command=self._limpar_filtros).pack(
            fill='x', expand=True, ipady=2, pady=(5, 0))

        btn_frame = ttk.Frame(self.frame_conteudo)
        btn_frame.pack(fill='x', pady=5)
        ttk.Button(btn_frame, text="Excluir", style="Danger.TButton", command=self._excluir_selecionados).pack(
            side='left', padx=(0, 5))
        ttk.Button(btn_frame, text="Editar", style="Warning.TButton", command=self._editar_selecionado).pack(
            side='left', padx=5)
        ttk.Button(btn_frame, text="Ver Detalhes", style="Secondary.TButton", command=self._ver_detalhes).pack(
            side='left', padx=5)

        tree_frame = ttk.Frame(self.frame_conteudo)
        tree_frame.pack(fill='both', expand=True)
        self.scrollbar = ttk.Scrollbar(tree_frame)
        self.x_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal')
        columns = ("id", "data", "status", "tipo", "ticket", "descricao", "colaborador", "setor")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15, selectmode='extended',
                                 style="Treeview", yscrollcommand=self.scrollbar.set,
                                 xscrollcommand=self.x_scrollbar.set)
        self.scrollbar.config(command=self.tree.yview);
        self.x_scrollbar.config(command=self.tree.xview)
        self.scrollbar.pack(side='right', fill='y');
        self.x_scrollbar.pack(side='bottom', fill='x')
        self.tree.pack(fill='both', expand=True)
        self.tree.heading("id", text="◻", command=self._selecionar_todos)
        self.tree.column("id", width=40, anchor='center', stretch=False)
        col_configs = [("data", "Data", 100), ("status", "Status", 100), ("tipo", "Tipo", 150),
                       ("ticket", "Ticket", 100), ("descricao", "Descrição", 400), ("colaborador", "Colaborador", 150),
                       ("setor", "Setor", 120)]
        for col, text, width in col_configs: self.tree.heading(col, text=text); self.tree.column(col, width=width)
        self.tree.bind("<Button-1>", self._toggle_selecao);
        self.tree.bind("<Double-1>", self._ver_detalhes_on_double_click)

        footer_frame = ttk.Frame(self.frame_conteudo)
        footer_frame.pack(fill='x', pady=(5, 0))
        limite_frame = ttk.Frame(footer_frame)
        limite_frame.pack(side='left')
        ttk.Label(limite_frame, text="Linhas:").pack(side='left', padx=(0, 5))
        self.combo_limite = ttk.Combobox(limite_frame, textvariable=self.limite_linhas, values=[50, 100, 200, 500],
                                         state='readonly', width=5)
        self.combo_limite.pack(side='left')
        self.combo_limite.bind("<<ComboboxSelected>>", lambda e: self._carregar_atividades())
        ttk.Label(footer_frame, textvariable=self.var_contador_selecao, font=('Segoe UI', 9, 'italic')).pack(
            side='left', padx=20)
        ttk.Button(footer_frame, text="Exportar Selecionados", style="Info.TButton", command=self._exportar_csv).pack(
            side='right')

    def _truncar_texto(self, texto, limite):
        if not texto: return ""
        return (texto[:limite] + '...') if len(texto) > limite else texto

    def _carregar_filtros(self):
        try:
            db = Database()
            self.filtro_tipo['values'] = [""] + [r['nome'] for r in
                                                 db.execute_query("SELECT nome FROM tipos_atendimento ORDER BY nome")]
            self.filtro_setor['values'] = [""] + [r['nome_setor'] for r in db.execute_query(
                "SELECT nome_setor FROM setores ORDER BY nome_setor")]
            self.filtro_colaborador['values'] = [""] + [r['nome'] for r in db.execute_query(
                "SELECT nome FROM colaboradores ORDER BY nome")]
        except Error as e:
            logging.error(f"Erro ao carregar filtros: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Falha ao carregar filtros:\n{e}")

    def _carregar_atividades(self):
        try:
            db = Database()
            base_query = "SELECT a.id, a.data_atendimento, a.status, t.nome AS tipo_atendimento, a.numero_atendimento, a.descricao, c.nome AS colaborador_nome, s.nome_setor FROM atividades a JOIN tipos_atendimento t ON a.tipo_atendimento_id = t.id JOIN colaboradores c ON a.colaborador_id = c.id JOIN setores s ON c.setor_id = s.id"
            where_clauses, params = [], []
            if (perfil := self.colaborador.cargo.value.lower()) == 'colaborador':
                where_clauses.append("a.colaborador_id = %s");
                params.append(self.colaborador.id)
            elif perfil == 'gestor':
                where_clauses.append("s.id = %s");
                params.append(self.colaborador.setor_id)
            if self.var_tipo.get(): where_clauses.append("t.nome = %s"); params.append(self.var_tipo.get())
            if self.var_ticket.get(): where_clauses.append("a.numero_atendimento LIKE %s"); params.append(
                f"%{self.var_ticket.get()}%")
            if self.var_setor.get(): where_clauses.append("s.nome_setor = %s"); params.append(self.var_setor.get())
            if self.var_colaborador.get(): where_clauses.append("c.nome = %s"); params.append(
                self.var_colaborador.get())
            if self.var_descricao_filtro.get(): where_clauses.append("a.descricao LIKE %s"); params.append(
                f"%{self.var_descricao_filtro.get()}%")
            if self.var_data_ini.get() and (
            data_ini := self._validar_data(self.var_data_ini.get())): where_clauses.append(
                "DATE(a.data_atendimento) >= %s"); params.append(data_ini.isoformat())
            if self.var_data_fim.get() and (
            data_fim := self._validar_data(self.var_data_fim.get())): where_clauses.append(
                "DATE(a.data_atendimento) <= %s"); params.append(data_fim.isoformat())

            final_query = base_query + (" WHERE " + " AND ".join(where_clauses) if where_clauses else "")
            final_query += " ORDER BY a.data_atendimento DESC, a.id DESC LIMIT %s"
            params.append(self.limite_linhas.get())
            resultados = db.execute_query(final_query, tuple(params))

            self.tree.delete(*self.tree.get_children())
            self.selecionados.clear()
            self._atualizar_contador_selecao()

            self.tree.tag_configure('linha_par', background='#ffffff');
            self.tree.tag_configure('linha_impar', background='#f2f2f2')
            for index, row in enumerate(resultados):
                tags = ['linha_par' if index % 2 == 0 else 'linha_impar']
                if row.get('status') == 'PENDENTE': tags.append('pendente')
                descricao_truncada = self._truncar_texto(row.get('descricao', ''), 60)
                self.tree.insert('', 'end', iid=str(row['id']),
                                 values=("◻", row['data_atendimento'].strftime('%d-%m-%Y'), row['status'],
                                         row['tipo_atendimento'], row['numero_atendimento'], descricao_truncada,
                                         row['colaborador_nome'], row['nome_setor']), tags=tuple(tags))
        except Error as e:
            logging.error(f"Erro ao carregar atividades: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Falha ao carregar atividades:\n{e}")

    def _selecionar_todos(self):
        self.todos_selecionados_state = not self.todos_selecionados_state
        novo_marcador = "☑" if self.todos_selecionados_state else "◻"
        for item_id in self.tree.get_children():
            self.tree.set(item_id, "id", novo_marcador)
            if self.todos_selecionados_state:
                self.selecionados.add(item_id)
            elif item_id in self.selecionados:
                self.selecionados.remove(item_id)
        self.tree.heading("id", text=novo_marcador)
        self._atualizar_contador_selecao()

    def _atualizar_contador_selecao(self):
        num = len(self.selecionados)
        self.var_contador_selecao.set(
            "Nenhum item selecionado" if num == 0 else f"1 item selecionado" if num == 1 else f"{num} itens selecionados")

    def _toggle_selecao(self, event):
        if self.tree.identify_region(event.x, event.y) != "cell" or self.tree.identify_column(event.x) != "#1": return
        if not (item := self.tree.identify_row(event.y)): return
        if item in self.selecionados:
            self.selecionados.remove(item); self.tree.set(item, "id", "◻")
        else:
            self.selecionados.add(item); self.tree.set(item, "id", "☑")
        self._atualizar_contador_selecao()

    def _exportar_csv(self):
        items_to_export = list(self.selecionados) or self.tree.get_children()
        if not items_to_export: return messagebox.showinfo("Informação", "Não há dados para exportar.")
        try:
            if not (
            filepath := filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")],
                                                     title="Salvar como")): return
            with open(filepath, mode='w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                cols = list(self.tree['columns'])[1:]
                writer.writerow([self.tree.heading(col)['text'] for col in cols])
                for item in items_to_export: writer.writerow(self.tree.item(item)['values'][1:])
            messagebox.showinfo("Sucesso", f"Dados exportados com sucesso para:\n{filepath}")
        except Exception as e:
            logging.error(f"Erro ao exportar CSV: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Falha ao exportar CSV:\n{e}")

    def _limpar_filtros(self):
        self.var_tipo.set("");
        self.var_data_ini.set("");
        self.var_data_fim.set("")
        self.var_ticket.set("");
        self.var_setor.set("");
        self.var_colaborador.set("")
        self.var_descricao_filtro.set("")
        self._carregar_atividades()

    def _excluir_selecionados(self):
        if not self.selecionados: return messagebox.showwarning("Aviso", "Nenhum item selecionado.")
        if not messagebox.askyesno("Confirmar Exclusão",
                                   f"Tem certeza que deseja excluir {len(self.selecionados)} registro(s)?",
                                   icon='warning'): return
        try:
            db = Database()
            placeholders = ",".join(["%s"] * len(self.selecionados))
            db.execute_query(f"DELETE FROM atividades WHERE id IN ({placeholders})", tuple(self.selecionados),
                             fetch=False)
            messagebox.showinfo("Sucesso", f"{len(self.selecionados)} registro(s) excluído(s).")
            self.selecionados.clear()
            self._carregar_atividades()
        except Error as e:
            logging.error(f"Erro ao excluir: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Falha ao excluir:\n{e}")

    def _ver_detalhes_on_double_click(self, event):
        if item_id := self.tree.identify_row(event.y):
            self.tree.selection_set(item_id)
            self._ver_detalhes()

    def _ver_detalhes(self):
        if not (selecionado := self.tree.selection()): return messagebox.showwarning("Aviso",
                                                                                     "Selecione uma atividade.")
        try:
            from screens.detalhes_atividade_view import DetalhesAtividadeView
            top = tk.Toplevel(self.master)
            DetalhesAtividadeView(top, int(selecionado[0]))
        except Exception as e:
            logging.error(f"Erro ao abrir detalhes: {e}", exc_info=True)
            messagebox.showerror("Erro", "Não foi possível abrir os detalhes.")

    def _editar_selecionado(self):
        if not (selecionado := self.tree.selection()): return messagebox.showwarning("Aviso",
                                                                                     "Selecione uma atividade.")
        try:
            from screens.editar_atividade_view import EditarAtividadeView
            top = tk.Toplevel(self.master)
            EditarAtividadeView(master=top, atividade_id=int(selecionado[0]), colaborador=self.colaborador,
                                on_save=self._carregar_atividades)
            top.wait_window()
        except Exception as e:
            logging.error(f"Erro ao abrir edição: {e}", exc_info=True)
            messagebox.showerror("Erro", "Não foi possível editar a atividade.")

    def _validar_data(self, data_str):
        for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y']:
            try:
                return datetime.strptime(data_str, fmt).date()
            except ValueError:
                continue
        return None


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Histórico de Atividades")
    root.state('zoomed')


    class MockColaborador:
        id = 1;
        setor_id = 1
        cargo = type('Cargo', (), {'value': 'admin'})()


    app = HistoricoAtividadesView(root, MockColaborador())
    root.mainloop()
