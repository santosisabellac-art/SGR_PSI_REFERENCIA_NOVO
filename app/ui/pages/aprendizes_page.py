import flet as ft


class AprendizesPage(ft.Column):

    def __init__(self):
        super().__init__(
            expand=True,
            spacing=20,
        )

        self.controls = [

            ft.Row(

                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                controls=[

                    ft.Text(
                        "Aprendizes",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                    ),

                    ft.ElevatedButton(

                        "➕ Novo Aprendiz",

                        icon=ft.Icons.ADD,

                        on_click=self.novo_aprendiz,

                    ),

                ],

            ),

            ft.TextField(

                label="Pesquisar aprendiz",

                prefix_icon=ft.Icons.SEARCH,

            ),

            ft.Divider(),

            ft.DataTable(

                expand=True,

                columns=[

                    ft.DataColumn(ft.Text("Nome")),

                    ft.DataColumn(ft.Text("Código")),

                    ft.DataColumn(ft.Text("Nível")),

                    ft.DataColumn(ft.Text("Sala")),

                    ft.DataColumn(ft.Text("Status")),

                ],

                rows=[],

            ),

        ]

    def novo_aprendiz(self, e):
        print("Novo Aprendiz")