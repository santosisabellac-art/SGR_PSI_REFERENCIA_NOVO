import flet as ft

from app.ui.dialogs.aprendiz_dialog import AprendizDialog


class AprendizesPage(ft.Column):

    def __init__(self, page: ft.Page):
        super().__init__(expand=True, spacing=20)

        # IMPORTANTE:
        # Não usamos self.page porque essa propriedade já pertence ao Flet.
        self._page = page
        self.dialog = None

        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Código")),
                ft.DataColumn(ft.Text("Nível")),
                ft.DataColumn(ft.Text("Sala")),
                ft.DataColumn(ft.Text("Status")),
            ],
            rows=[],
        )

        self.pesquisa = ft.TextField(
            label="Pesquisar aprendiz",
            prefix_icon=ft.Icons.SEARCH,
            width=450,
        )

        self.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(
                                "Aprendizes",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Gerencie os aprendizes sob sua referência.",
                                size=14,
                            ),
                        ],
                    ),
                    ft.ElevatedButton(
                        text="Novo Aprendiz",
                        icon=ft.Icons.ADD,
                        on_click=self.novo_aprendiz,
                    ),
                ],
            ),

            self.pesquisa,

            ft.Divider(),

            self.tabela,
        ]

    def novo_aprendiz(self, e):

        self.dialog = AprendizDialog(
            page=self._page,
            on_save=self.carregar_dados,
        )

        self._page.open(self.dialog)

    def carregar_dados(self):
        """
        Na próxima entrega vamos carregar
        automaticamente os aprendizes do banco.
        """
        pass