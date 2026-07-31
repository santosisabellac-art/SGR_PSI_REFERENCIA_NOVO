import flet as ft

from app.ui.components.sidebar import Sidebar
from app.ui.theme.theme import AppTheme


def app(page: ft.Page):

    page.title = "SGR - Psicóloga de Referência"

    page.window.width = 1450
    page.window.height = 900

    page.bgcolor = AppTheme.BACKGROUND

    page.padding = 0

    page.add(

        ft.Row(

            controls=[

                Sidebar(),

                ft.Container(

                    expand=True,

                    padding=30,

                    content=ft.Column(

                        [

                            ft.Text(

                                "Bem-vinda, Isabella",

                                size=28,

                                weight=ft.FontWeight.BOLD,

                            ),

                            ft.Text(

                                "Sistema de Gestão da Psicóloga de Referência",

                                color=AppTheme.SUBTITLE,

                            ),

                        ]

                    ),

                ),

            ],

            expand=True,

        )

    )


def main():
    ft.app(target=app)