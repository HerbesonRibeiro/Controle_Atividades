import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from utils.db import Database
import logging
import csv
from datetime import datetime

class HistoricoAtividadesView:
    def __init__(self, master, colaborador):
        self.master = master  # Janela raiz (tk.Tk) de HomeView
        self.colaborador = colaborador
        self.selecionados = set()
        self.limite_linhas = tk.IntVar(value=50)

        # Cria o frame de conteúdo dentro da janela raiz
        self.frame_conteudo = tk.Frame(self.master, bg='#f8f9fa', padx=10, pady=5)
        self.frame_conteudo.pack(fill='both', expand=True)

        self._configurar_estilos()
        self._setup_ui()
        self._carregar_filtros()
        self._carregar_atividades()

    def _configurar_estilos(self):
        """Configura os estilos visuais para melhor visibilidade"""
        self.style = ttk.Style()
        self.style.configure("Treeview", font=('Segoe UI', 10), rowheight=25,
                            background="#ffffff", fieldbackground="#ffffff",
                            bordercolor="#dddddd", borderwidth=1)
        self.style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'),
                            background='#e1e1e1', relief='flat', padding=3)
        self.style.map("Treeview", background=[('selected', '#e6f3ff')],
                      foreground=[('selected', 'black')])
        self.style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        # Estilos para botões menores
        self.style.configure("TButton", font=('Segoe UI', 9, 'bold'), padding=4)
        self.style.configure("Custom.TButton", background="#007bff", foreground="white",
                            padding=4)
        self.style.map("Custom.TButton",
                      background=[('active', '#0056b3'), ('!disabled', '#007bff')],
                      foreground=[('active', 'white'), ('!disabled', 'white')])

    def _setup_ui(self):
        ttk.Label(self.frame_conteudo, text="Histórico de Atividades",
                  font=('Segoe UI', 12, 'bold'), style="CustomLabel.TLabel").pack(pady=(0, 8))

        filtro_frame = tk.Frame(self.frame_conteudo, bg='#f8f9fa')
        filtro_frame.pack(fill='x', pady=(0, 8))

        self.var_tipo = tk.StringVar()
        self.var_data_ini = tk.StringVar()
        self.var_data_fim = tk.StringVar()
        self.var_ticket = tk.StringVar()
        self.var_setor = tk.StringVar()
        self.var_colaborador = tk.StringVar()

        # Tipo
        ttk.Label(filtro_frame, text="Tipo:", style="CustomLabel.TLabel").pack(side='left')
        self.filtro_tipo = ttk.Combobox(filtro_frame, textvariable=self.var_tipo,
                                        state='readonly')
        self.filtro_tipo.pack(side='left', padx=3)

        # De (Data Inicial)
        ttk.Label(filtro_frame, text="De:", style="CustomLabel.TLabel").pack(side='left')
        self.filtro_data_ini = DateEntry(filtro_frame, textvariable=self.var_data_ini,
                                         date_pattern='yyyy-MM-dd', background='darkblue',
                                         foreground='white', borderwidth=1, width=10)
        self.filtro_data_ini.pack(side='left', padx=3)
        self.filtro_data_ini.bind("<<DateEntrySelected>>",
                                  lambda e: self._carregar_atividades())

        # Até (Data Final)
        ttk.Label(filtro_frame, text="Até:", style="CustomLabel.TLabel").pack(side='left')
        self.filtro_data_fim = DateEntry(filtro_frame, textvariable=self.var_data_fim,
                                         date_pattern='yyyy-MM-dd', background='darkblue',
                                         foreground='white', borderwidth=1, width=10)
        self.filtro_data_fim.pack(side='left', padx=3)
        self.filtro_data_fim.bind("<<DateEntrySelected>>",
                                  lambda e: self._carregar_atividades())

        # Ticket
        ttk.Label(filtro_frame, text="Ticket:", style="CustomLabel.TLabel").pack(side='left')
        ttk.Entry(filtro_frame, textvariable=self.var_ticket).pack(side='left', padx=3)

        # Setor
        ttk.Label(filtro_frame, text="Setor:", style="CustomLabel.TLabel").pack(side='left')
        self.filtro_setor = ttk.Combobox(filtro_frame, textvariable=self.var_setor,
                                         state='readonly')
        self.filtro_setor.pack(side='left', padx=3)

        # Colaborador
        ttk.Label(filtro_frame, text="Colaborador:", style="CustomLabel.TLabel").pack(side='left')
        self.filtro_colaborador = ttk.Combobox(filtro_frame, textvariable=self.var_colaborador,
                                               state='readonly')
        self.filtro_colaborador.pack(side='left', padx=3)

        # Botões de filtro
        ttk.Button(filtro_frame, text="Filtrar", style="Custom.TButton",
                   command=self._carregar_atividades).pack(side='left', padx=5)
        ttk.Button(filtro_frame, text="Limpar Filtros", style="Custom.TButton",
                   command=self._limpar_filtros).pack(side='left', padx=3)

        # Botões de ação
        btn_frame = tk.Frame(self.frame_conteudo, bg='#f8f9fa')
        btn_frame.pack(fill='x', pady=(0, 5))
        tk.Button(btn_frame, text="Excluir", bg="#dc3545", fg="white",
                  command=self._excluir_selecionados).pack(side='left', padx=3)
        tk.Button(btn_frame, text="Editar", bg="#ffc107", fg="black",
                  command=self._editar_selecionado).pack(side='left', padx=3)
        tk.Button(btn_frame, text="Ver Detalhes", bg="#6c757d", fg="white",
                  command=self._ver_detalhes).pack(side='left', padx=3)

        # Frame para Treeview com barra de rolagem
        tree_frame = tk.Frame(self.frame_conteudo)
        tree_frame.pack(fill='both', expand=True, pady=(5, 0))

        self.scrollbar = tk.Scrollbar(tree_frame)
        self.scrollbar.pack(side='right', fill='y')

        columns = ("id", "data", "tipo", "ticket", "descricao",
                   "colaborador", "setor")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                 height=15, selectmode='extended', style="Treeview",
                                 yscrollcommand=self.scrollbar.set)
        self.tree.heading("id", text="☑")
        self.tree.column("id", width=50, anchor='center', stretch=False)
        col_configs = [("data", "Data", 90), ("tipo", "Tipo", 110),
                       ("ticket", "Ticket", 90), ("descricao", "Descrição", 150),
                       ("colaborador", "Colaborador", 110), ("setor", "Setor", 110)]
        for col, text, width in col_configs:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width)
        self.tree.pack(side='left', fill='both', expand=True)
        self.scrollbar.config(command=self.tree.yview)

        # Opção de limite de linhas
        limite_frame = tk.Frame(self.frame_conteudo, bg='#f8f9fa')
        limite_frame.pack(fill='x', pady=(5, 0))
        ttk.Label(limite_frame, text="Linhas por página:", style="CustomLabel.TLabel").pack(side='left', padx=5)
        self.combo_limite = ttk.Combobox(limite_frame, textvariable=self.limite_linhas,
                                         values=[50, 100, 200, 300, 400], state='readonly')
        self.combo_limite.pack(side='left', padx=5)
        self.combo_limite.bind("<<ComboboxSelected>>", lambda e: self._carregar_atividades())

        # Exportar CSV
        export_frame = tk.Frame(self.frame_conteudo, bg='#f8f9fa')
        export_frame.pack(fill='x', pady=(5, 5))
        tk.Button(export_frame, text="Exportar CSV", bg="#17a2b8", fg="white",
                  command=self._exportar_csv).pack(side='right', padx=5)

    def _carregar_filtros(self):
        """Carrega as opções disponíveis para os filtros de tipo, setor e colaborador"""
        try:
            cursor = Database().get_cursor()
            cursor.execute("SELECT nome FROM tipos_atendimento ORDER BY nome")
            tipos = [""] + [row['nome'] for row in cursor.fetchall()]
            self.filtro_tipo['values'] = tipos

            cursor.execute("SELECT nome_setor FROM setores ORDER BY nome_setor")
            setores = [""] + [row['nome_setor'] for row in cursor.fetchall()]
            self.filtro_setor['values'] = setores

            cursor.execute("SELECT nome FROM colaboradores ORDER BY nome")
            colaboradores = [""] + [row['nome'] for row in cursor.fetchall()]
            self.filtro_colaborador['values'] = colaboradores
        except Exception as e:
            logging.error(f"Erro ao carregar filtros: {e}", exc_info=True)

    def _carregar_atividades(self):
        try:
            cursor = Database().get_cursor()
            base_query = """
                SELECT
                    a.id,
                    a.data_atendimento,
                    t.nome AS tipo_atendimento,
                    a.numero_atendimento,
                    a.descricao,
                    c.nome AS colaborador_nome,
                    s.nome_setor
                FROM atividades a
                JOIN tipos_atendimento t ON a.tipo_atendimento_id = t.id
                JOIN colaboradores c ON a.colaborador_id = c.id
                JOIN setores s ON c.setor_id = s.id
            """
            where_clauses, params = [], []

            perfil = self.colaborador.cargo.value.lower()
            if perfil == 'colaborador':
                where_clauses.append("a.colaborador_id = %s")
                params.append(self.colaborador.id)
            elif perfil == 'gestor':
                where_clauses.append("s.id = %s")
                params.append(self.colaborador.setor_id)

            if self.var_tipo.get():
                where_clauses.append("t.nome = %s")
                params.append(self.var_tipo.get())

            if self.var_data_ini.get():
                data_ini = self._validar_data(self.var_data_ini.get())
                if data_ini:
                    where_clauses.append("DATE(a.data_atendimento) >= %s")
                    params.append(data_ini.isoformat())

            if self.var_data_fim.get():
                data_fim = self._validar_data(self.var_data_fim.get())
                if data_fim:
                    where_clauses.append("DATE(a.data_atendimento) <= %s")
                    params.append(data_fim.isoformat())

            if self.var_ticket.get():
                where_clauses.append("a.numero_atendimento LIKE %s")
                params.append(f"%{self.var_ticket.get()}%")

            if self.var_setor.get():
                where_clauses.append("s.nome_setor = %s")
                params.append(self.var_setor.get())

            if self.var_colaborador.get():
                where_clauses.append("c.nome = %s")
                params.append(self.var_colaborador.get())

            if where_clauses:
                base_query += " WHERE " + " AND ".join(where_clauses)

            base_query += " ORDER BY a.data_atendimento DESC LIMIT %s"
            params.append(self.limite_linhas.get())
            cursor.execute(base_query, tuple(params))
            resultados = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)
            self.selecionados.clear()

            self.tree.tag_configure('linha_par', background='#ffffff')
            self.tree.tag_configure('linha_impar', background='#f2f2f2')

            for index, row in enumerate(resultados):
                iid = str(row['id'])
                data_br = row['data_atendimento'].strftime('%d-%m-%Y')
                marcado = "☑" if iid in self.selecionados else "◻"
                tag_linha = 'linha_par' if index % 2 == 0 else 'linha_impar'

                self.tree.insert('', 'end', iid=iid, values=(
                    marcado,
                    data_br.upper(),
                    str(row['tipo_atendimento']).upper(),
                    str(row['numero_atendimento']).upper(),
                    str(row['descricao']).upper(),
                    str(row['colaborador_nome']).upper(),
                    str(row['nome_setor']).upper()
                ), tags=(tag_linha,))

        except Exception as e:
            logging.error(f"Erro ao carregar atividades: {e}", exc_info=True)
            messagebox.showerror("Erro", "Falha ao carregar atividades.")

    def _toggle_selecao(self, event):
        """Alterna a seleção de itens na tabela ao clicar na coluna de seleção."""
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = self.tree.identify_column(event.x)
        if column != "#1":
            return

        item = self.tree.identify_row(event.y)
        if not item:
            return

        if item in self.selecionados:
            self.selecionados.remove(item)
            self.tree.set(item, "id", "◻")
        else:
            self.selecionados.add(item)
            self.tree.set(item, "id", "☑")

        self.tree.selection_remove(self.tree.selection())
        if item in self.selecionados:
            self.tree.selection_add(item)

    def _exportar_csv(self):
        """Exporta os dados da tabela para um arquivo CSV"""
        try:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv")],
                title="Salvar como"
            )
            if not filepath:
                return

            with open(filepath, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')

                # Cabeçalho (pula coluna de seleção)
                cols = list(self.tree['columns'])[1:]
                headers = [self.tree.heading(col)['text'] for col in cols]
                writer.writerow(headers)

                # Exporta apenas itens selecionados
                items = self.tree.selection() if self.tree.selection() else self.tree.get_children()
                for item in items:
                    values = self.tree.item(item)['values'][1:]
                    row = [
                        v.strftime('%Y-%m-%d %H:%M:%S')
                        if isinstance(v, datetime) else v
                        for v in values
                    ]
                    writer.writerow(row)

            messagebox.showinfo("Sucesso",
                                f"Dados exportados com sucesso para:\n{filepath}")
        except Exception as e:
            logging.error(f"Erro ao exportar CSV: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Falha ao exportar CSV:\n{e}")

    def _limpar_filtros(self):
        """Limpa os filtros redefinindo para valores padrão"""
        self.var_tipo.set("")
        self.var_data_ini.set("")
        self.var_data_fim.set("")
        self.var_ticket.set("")
        self.var_setor.set("")
        self.var_colaborador.set("")
        self._carregar_atividades()

    def _excluir_selecionados(self):
        """Exclui os itens selecionados da tabela"""
        if not self.selecionados:
            messagebox.showwarning("Aviso", "Nenhum item selecionado para exclusão.")
            return

        confirm = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir {len(self.selecionados)} registro(s)?",
            icon='warning'
        )
        if not confirm:
            return

        db = Database()
        cursor = db.get_cursor()
        try:
            ids = list(self.selecionados)
            placeholders = ",".join(["%s"] * len(ids))
            cursor.execute(
                f"DELETE FROM atividades WHERE id IN ({placeholders})",
                tuple(ids)
            )
            db.conn.commit()

            count = len(ids)
            self.selecionados.clear()
            self._carregar_atividades()
            messagebox.showinfo("Sucesso",
                                f"{count} registro(s) excluído(s) com sucesso.")
        except Exception as e:
            db.conn.rollback()
            logging.error(f"Erro ao excluir registros: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Falha ao excluir registros:\n{e}")

    def _ver_detalhes(self):
        """Abre a janela de detalhes da atividade selecionada."""
        try:
            selecionado = self.tree.selection()
            if not selecionado:
                messagebox.showwarning("Aviso",
                                       "Selecione uma atividade para ver detalhes.")
                return

            atividade_id = int(selecionado[0])
            from screens.detalhes_atividade_view import DetalhesAtividadeView

            top = tk.Toplevel(self.master)
            top.title("Detalhes da Atividade")
            top.grab_set()
            DetalhesAtividadeView(top, atividade_id)
        except Exception as e:
            logging.error(f"Erro ao abrir detalhes: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Não foi possível abrir detalhes:\n{e}")

    def _editar_selecionado(self):
        """Abre a janela de edição para o item selecionado."""
        try:
            selecionado = self.tree.selection()
            if not selecionado:
                messagebox.showwarning("Aviso",
                                       "Selecione uma atividade para editar.")
                return

            atividade_id = int(selecionado[0])
            from screens.editar_atividade_view import EditarAtividadeView

            top = tk.Toplevel(self.master)
            top.title("Editar Atividade")
            top.transient(self.master)
            top.grab_set()

            EditarAtividadeView(
                master=top,
                atividade_id=atividade_id,
                colaborador=self.colaborador,
                on_save=self._carregar_atividades
            )
            top.wait_window()
        except Exception as e:
            logging.error(f"Erro ao abrir edição: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Não foi possível editar a atividade:\n{e}")

    def _validar_data(self, data_str):
        """
        Converte string para date nos formatos:
          - 'YYYY-MM-DD' (padrão DateEntry)
          - 'DD-MM-YYYY'
        Retorna date ou None se inválido.
        """
        formatos = ['%Y-%m-%d', '%d-%m-%Y']
        for fmt in formatos:
            try:
                return datetime.strptime(data_str, fmt).date()
            except ValueError:
                continue

        messagebox.showwarning(
            "Formato inválido",
            f"Data '{data_str}' precisa estar em aaaa-mm-dd ou dd-mm-aaaa"
        )
        return None


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Histórico de Atividades")
    class MockColaborador:
        def __init__(self):
            self.id = 1
            self.cargo = type('Cargo', (), {'value': 'colaborador'})()
            self.setor_id = 1
    app = HistoricoAtividadesView(root, MockColaborador())
    root.mainloop()