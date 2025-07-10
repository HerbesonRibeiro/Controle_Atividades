import tkinter as tk
from screens.atendimento_view import AtendimentoView
from tkinter import ttk, font


class HomeView:
    def __init__(self, master):
        self.master = master
        self.master.title("Controle de Atividades")
        self.master.geometry("1000x650")
        self.master.configure(bg='#f5f5f5')

        self._setup_ui()

    def _setup_ui(self):
        # Frame principal
        self.main_frame = tk.Frame(self.master, bg='#f5f5f5')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Cabeçalho
        self._build_header()

        # Corpo principal (sidebar + content)
        self.body_frame = tk.Frame(self.main_frame, bg='#f5f5f5')
        self.body_frame.pack(expand=True, fill='both', pady=(20, 0))

        # Sidebar
        self._build_sidebar()

        # Área de conteúdo
        self._build_content()

        # Rodapé
        self._build_footer()

    def _build_header(self):
        header_frame = tk.Frame(self.main_frame, bg='white', height=80)
        header_frame.pack(fill='x')

        tk.Label(
            header_frame,
            text="CONTROLE DE ATIVIDADES",
            font=('Helvetica', 16, 'bold'),
            bg='white',
            fg='#333'
        ).pack(side='left', padx=20)

        # Adicionei espaço para o usuário logado
        self.user_info = tk.Label(
            header_frame,
            text="Usuário: Admin",
            font=('Helvetica', 10),
            bg='white',
            fg='#666'
        )
        self.user_info.pack(side='right', padx=20)

    def _build_sidebar(self):
        sidebar = tk.Frame(self.body_frame, bg='#2c3e50', width=250)
        sidebar.pack(side='left', fill='y')

        # Estilo para os botões do menu
        menu_style = {
            'bg': '#2c3e50',
            'fg': 'white',
            'activebackground': '#34495e',
            'activeforeground': 'white',
            'anchor': 'w',
            'padx': 20,
            'pady': 12,
            'bd': 0,
            'font': ('Helvetica', 11)
        }

        # Seções do menu adaptadas para Controle de Atividades
        sections = [
            ("ATIVIDADES", [
                "Cadastrar Nova",
                "Listar Pendentes",
                "Relatórios"
            ]),
            ("PROJETOS", [
                "Gerenciar Projetos",
                "Atividades por Projeto"
            ]),
            ("EQUIPE", [
                "Membros",
                "Alocação"
            ]),
            ("CONFIGURAÇÕES", [
                "Perfil",
                "Preferências"
            ])
        ]

        for section, items in sections:
            # Título da seção
            tk.Label(
                sidebar,
                text=section,
                bg='#34495e',
                fg='white',
                padx=20,
                pady=8,
                anchor='w',
                font=('Helvetica', 10, 'bold')
            ).pack(fill='x')

            # Itens do menu
            for item in items:
                btn = tk.Button(
                    sidebar,
                    text=f"  {item}",
                    **menu_style,
                    command=lambda i=item: self._select_menu_item(i)
                )
                btn.pack(fill='x')

    def _build_content(self):
        content = tk.Frame(self.body_frame, bg='white')
        content.pack(expand=True, fill='both', padx=(20, 0))

        # Área de conteúdo dinâmico
        self.content_area = tk.Frame(content, bg='white')
        self.content_area.pack(expand=True, fill='both', padx=20, pady=20)

        # Conteúdo inicial (Dashboard)
        self._show_dashboard()

    def _build_footer(self):
        footer_frame = tk.Frame(self.main_frame, bg='white', height=50)
        footer_frame.pack(fill='x', pady=(20, 0))

        tk.Label(
            footer_frame,
            text="Sistema de Controle de Atividades v1.0",
            font=('Helvetica', 9),
            bg='white',
            fg='#666'
        ).pack(side='left', padx=20)

        tk.Label(
            footer_frame,
            text="© 2023 - Todos os direitos reservados",
            font=('Helvetica', 9),
            bg='white',
            fg='#666'
        ).pack(side='right', padx=20)

    def _show_dashboard(self):
        """Exibe o painel inicial"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Título
        tk.Label(
            self.content_area,
            text="Painel de Controle",
            font=('Helvetica', 14, 'bold'),
            bg='white',
            fg='#333'
        ).pack(anchor='w', pady=(0, 20))

        # Cards de resumo
        cards_frame = tk.Frame(self.content_area, bg='white')
        cards_frame.pack(fill='x', pady=10)

        cards_data = [
            {"title": "Atividades Pendentes", "value": "15", "color": "#e74a3b"},
            {"title": "Em Andamento", "value": "8", "color": "#f6c23e"},
            {"title": "Concluídas", "value": "23", "color": "#1cc88a"},
            {"title": "Atrasadas", "value": "3", "color": "#858796"}
        ]

        for card in cards_data:
            frame = tk.Frame(
                cards_frame,
                bg='#f8f9fa',
                padx=15,
                pady=15,
                relief='groove',
                bd=1
            )
            frame.pack(side='left', expand=True, fill='both', padx=5)

            tk.Label(
                frame,
                text=card["title"],
                font=('Helvetica', 10, 'bold'),
                bg='#f8f9fa'
            ).pack(anchor='w')

            tk.Label(
                frame,
                text=card["value"],
                font=('Helvetica', 24, 'bold'),
                bg='#f8f9fa',
                fg=card["color"]
            ).pack(pady=5)

        # Últimas atividades
        tk.Label(
            self.content_area,
            text="Últimas Atividades",
            font=('Helvetica', 12, 'bold'),
            bg='white',
            fg='#333'
        ).pack(anchor='w', pady=(30, 10))

        # Tabela simples (substitua por Treeview depois)
        table_frame = tk.Frame(self.content_area, bg='white')
        table_frame.pack(fill='x')

        # Cabeçalhos
        headers = ["ID", "Descrição", "Responsável", "Status", "Prazo"]
        for i, header in enumerate(headers):
            tk.Label(
                table_frame,
                text=header,
                font=('Helvetica', 10, 'bold'),
                bg='#e9ecef',
                padx=10,
                pady=5,
                width=15
            ).grid(row=0, column=i, sticky='ew')

        # Dados de exemplo
        sample_data = [
            ("001", "Revisar documento", "João", "Pendente", "15/05/2023"),
            ("002", "Testar sistema", "Maria", "Concluído", "10/05/2023"),
            ("003", "Atualizar relatório", "Carlos", "Andamento", "20/05/2023")
        ]

        for row, data in enumerate(sample_data, start=1):
            for col, value in enumerate(data):
                tk.Label(
                    table_frame,
                    text=value,
                    font=('Helvetica', 9),
                    bg='white',
                    padx=10,
                    pady=5,
                    width=15,
                    anchor='w'
                ).grid(row=row, column=col, sticky='ew')

    def _select_menu_item(self, item):
        """Atualiza o conteúdo com base no item selecionado"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

        title_frame = tk.Frame(self.content_area, bg='white')
        title_frame.pack(fill='x', pady=(0, 20))

        tk.Label(
            title_frame,
            text=item.upper(),
            font=('Helvetica', 14, 'bold'),
            bg='white',
            fg='#333'
        ).pack(side='left')

        # Conteúdo placeholder - substitua pelo conteúdo real de cada seção
        content_frame = tk.Frame(self.content_area, bg='white')
        content_frame.pack(expand=True, fill='both')

        tk.Label(
            content_frame,
            text=f"Conteúdo da seção: {item}",
            font=('Helvetica', 12),
            bg='white',
            fg='#666'
        ).pack(pady=50)


if __name__ == "__main__":
    root = tk.Tk()
    app = HomeView(root)
    root.mainloop()