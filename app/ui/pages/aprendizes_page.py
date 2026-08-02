import flet as ft

from app.ui.dialogs.aprendiz_dialog import AprendizDialog


class AprendizesPage(ft.Column):

    def __init__(self, page: ft.Page):
        super().__init__(
            expand=True,
            spacing=20,
        )

        self.page = page
        self.dialog = None

        self.tabela = ft.DataTable(
            expand=True,
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
            width=420,
        )

        self.controls = [

            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[

                    ft.Column(
                        spacing=0,
                        controls=[

                            ft.Text(
                                "Aprendizes",
                                size=32,
                                weight=ft.FontWeight.BOLD,
                            ),

                            ft.Text(
                                "Gerencie todos os aprendizes sob sua referência.",
                                size=14,
                                color=ft.Colors.GREY_600,
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
            page=self.page,
            on_save=self.carregar_dados,
        )

        self.page.open(self.dialog)

    def carregar_dados(self):
        """
        Na próxima entrega este método
        carregará automaticamente os aprendizes
        do banco SQLite.
        """
        pass