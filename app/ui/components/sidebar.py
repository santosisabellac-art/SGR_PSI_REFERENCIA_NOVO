import flet as ft

from app.ui.theme.theme import AppTheme


class Sidebar(ft.Container):

    def __init__(self):

        super().__init__()

        self.width = 250

        self.bgcolor = AppTheme.SURFACE

        self.padding = 20

        self.content = ft.Column(

            controls=[

                ft.Text(

                    "SGR",

                    size=28,

                    weight=ft.FontWeight.BOLD,

                    color=AppTheme.PRIMARY,

                ),

                ft.Divider(),

                ft.TextButton("📥 Caixa de Entrada"),

                ft.TextButton("👤 Aprendizes"),

                ft.TextButton("📅 Agenda"),

                ft.TextButton("📄 Documentos"),

                ft.TextButton("⚙ Configurações"),

            ],

            spacing=10,

        )