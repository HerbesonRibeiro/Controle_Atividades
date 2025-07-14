import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from utils.db import Database
import logging
import csv

class HistoricoAtividadesView:
    def __init__(self, master, colaborador):
        self.master = master
        self.colaborador = colaborador
        self.selecionados = set()

        self.frame = tk.Frame(self.master, bg='#f8f9fa', padx=20, pady=10)
        self.frame.pack(fill='both', expand=True)

        self._setup_ui()
        self._carregar_atividades()

    def _setup_ui(self):
        tk.Label(self.frame, text="Histórico de Atividades", font=('Segoe UI', 14, 'bold'), bg='#f8f9fa').pack(pady=(0, 10))

        # Filtros
        filtro_frame = tk.Frame(self.frame, bg='#f8f9fa')
        filtro_frame.pack(fill='x', pady=(0, 10))

        self.var_tipo = tk.StringVar()
        self.var_data_ini = tk.StringVar()
        self.var_data_fim = tk.StringVar()
        self.var_nivel = tk.StringVar()
        self.var_ticket = tk.StringVar()

        ttk.Label(filtro_frame, text="Tipo:", background='#f8f9fa').pack(side='left')
        self.filtro_tipo = ttk.Combobox(filtro_frame, textvariable=self.var_tipo, state='readonly')
        self.filtro_tipo.pack(side='left', padx=5)

        ttk.Label(filtro_frame, text="De:", background='#f8f9fa').pack(side='left')
        ttk.Entry(filtro_frame, textvariable=self.var_data_ini, width=10).pack(side='left', padx=5)

        ttk.Label(filtro_frame, text="Até:", background='#f8f9fa').pack(side='left')
        ttk.Entry(filtro_frame, textvariable=self.var_data_fim, width=10).pack(side='left', padx=5)

        ttk.Label(filtro_frame, text="Complexidade:", background='#f8f9fa').pack(side='left')
        self.filtro_nivel = ttk.Combobox(filtro_frame, textvariable=self.var_nivel, state='readonly',
                                         values=["", "baixo", "medio", "grave", "gravissimo"])
        self.filtro_nivel.pack(side='left', padx=5)

        ttk.Label(filtro_frame, text="Ticket:", background='#f8f9fa').pack(side='left')
        ttk.Entry(filtro_frame, textvariable=self.var_ticket).pack(side='left', padx=5)

        ttk.Button(filtro_frame, text="Filtrar", command=self._carregar_atividades).pack(side='left', padx=10)

        # Botões de ação
        btn_frame = tk.Frame(self.frame, bg='#f8f9fa')
        btn_frame.pack(fill='x', pady=(0, 10))

        tk.Button(btn_frame, text="Excluir Selecionados", bg="#dc3545", fg="white",
                  command=self._excluir_selecionados).pack(side='left', padx=5)

        tk.Button(btn_frame, text="Editar Selecionado", bg="#ffc107", fg="black",
                  command=self._editar_selecionado).pack(side='left', padx=5)

        tk.Button(btn_frame, text="Exportar CSV", bg="#17a2b8", fg="white",
                  command=self._exportar_csv).pack(side='left', padx=5)

        tk.Button(btn_frame, text="Ver Detalhes", bg="#6c757d", fg="white",
                  command=self._ver_detalhes).pack(side='left', padx=5)

        # Tabela
        columns = ("selecionar", "data", "tipo", "nivel", "ticket", "descricao")
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings', selectmode='browse')

        self.tree.heading("selecionar", text="✔")
        self.tree.column("selecionar", width=40, anchor='center')

        for col in columns[1:]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150)

        self.tree.pack(fill='both', expand=True)
        self.tree.bind("<Button-1>", self._toggle_selecao)

    def _carregar_atividades(self):
        try:
            cursor = Database().get_cursor()

            base_query = """
                SELECT a.id, a.data_atendimento, 
                       t.nome AS tipo_atendimento, 
                       a.nivel_complexidade, 
                       a.numero_atendimento, 
                       a.descricao
                FROM atividades a
                JOIN tipos_atendimento t ON a.tipo_atendimento_id = t.id
                JOIN colaboradores c ON a.colaborador_id = c.id
            """

            where_clauses = []
            params = []

            perfil = self.colaborador.perfil_nome.lower()

            if perfil == 'colaborador':
                where_clauses.append("a.colaborador_id = %s")
                params.append(self.colaborador.id)
            elif perfil == 'gestor':
                where_clauses.append("c.setor_id = %s")
                params.append(self.colaborador.setor_id)

            # Filtros da interface
            if self.var_tipo.get():
                where_clauses.append("t.nome = %s")
                params.append(self.var_tipo.get())

            if self.var_data_ini.get():
                where_clauses.append("DATE(a.data_atendimento) >= %s")
                params.append(self.var_data_ini.get())

            if self.var_data_fim.get():
                where_clauses.append("DATE(a.data_atendimento) <= %s")
                params.append(self.var_data_fim.get())

            if self.var_nivel.get():
                where_clauses.append("a.nivel_complexidade = %s")
                params.append(self.var_nivel.get())

            if self.var_ticket.get():
                where_clauses.append("a.numero_atendimento LIKE %s")
                params.append(f"%{self.var_ticket.get()}%")

            if where_clauses:
                base_query += " WHERE " + " AND ".join(where_clauses)

            base_query += " ORDER BY a.data_atendimento DESC"

            cursor.execute(base_query, tuple(params))
            resultados = cursor.fetchall()

            for i in self.tree.get_children():
                self.tree.delete(i)
            self.selecionados.clear()

            for row in resultados:
                iid = str(row['id'])
                self.tree.insert('', 'end', iid=iid, values=(
                    "", row['data_atendimento'], row['tipo_atendimento'],
                    row['nivel_complexidade'], row['numero_atendimento'], row['descricao']
                ))

        except Exception as e:
            logging.error(f"Erro ao carregar atividades: {e}", exc_info=True)
            messagebox.showerror("Erro", "Falha ao carregar atividades.")

    def _ver_detalhes(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma atividade para ver detalhes.")
            return

        atividade_id = int(selecionado[0])

        from screens.detalhes_atividade_view import DetalhesAtividadeView
        top = tk.Toplevel(self.master)
        DetalhesAtividadeView(top, atividade_id)

    def _editar_selecionado(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma atividade para editar.")
            return

        atividade_id = int(selecionado[0])

        from screens.editar_atividade_view import EditarAtividadeView
        top = tk.Toplevel(self.master)
        EditarAtividadeView(top, atividade_id, self.colaborador, self._carregar_atividades)

    def _toggle_selecao(self, event):
        # Função futura ou opcional
        pass

    def _excluir_selecionados(self):
        # Função futura ou opcional
        messagebox.showinfo("Futuro", "Função de exclusão ainda será implementada.")

    def _exportar_csv(self):
        # Função futura ou opcional
        messagebox.showinfo("Exportação", "Exportar CSV ainda não está implementado.")
