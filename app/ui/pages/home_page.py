import flet as ft

from app.ui.theme.theme import AppTheme


class HomePage(ft.Column):

    def __init__(self):
        super().__init__(
            expand=True,
            spacing=20,
        )

        self.controls = [

            ft.Text(
                "Bom dia, Isabella 👋",
                size=30,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Text(
                "Bem-vinda ao Sistema de Gestão da Psicóloga de Referência.",
                color=AppTheme.SUBTITLE,
            ),

            ft.Divider(),

            ft.Row(

                spacing=20,

                controls=[

                    self.card(
                        "🔴 Pendências",
                        "2 prioritárias"
                    ),

                    self.card(
                        "📅 Agenda",
                        "4 atendimentos hoje"
                    ),

                    self.card(
                        "📄 Produção",
                        "3 documentos"
                    ),

                ]

            ),

            ft.Divider(),

            ft.Text(

                "Próximas atividades",

                size=22,

                weight=ft.FontWeight.BOLD,

            ),

            ft.Card(

                content=ft.Container(

                    padding=20,

                    content=ft.Column(

                        controls=[

                            ft.Text("• Atualizar PEI de João Pedro"),

                            ft.Text("• Revisar PIC de Maria Eduarda"),

                            ft.Text("• Fazer supervisão de Lucas Henrique"),

                        ]

                    ),

                )

            )

        ]

    def card(self, titulo, valor):

        return ft.Container(

            expand=True,

            bgcolor=AppTheme.SURFACE,

            border_radius=12,

            padding=20,

            border=ft.border.Border(
    top=ft.BorderSide(1, AppTheme.BORDER),
    bottom=ft.BorderSide(1, AppTheme.BORDER),
    left=ft.BorderSide(1, AppTheme.BORDER),
    right=ft.BorderSide(1, AppTheme.BORDER),
),

            content=ft.Column(

                controls=[

                    ft.Text(
                        titulo,
                        weight=ft.FontWeight.BOLD,
                    ),

                    ft.Text(
                        valor,
                        size=22,
                    ),

                ]

            ),

        )