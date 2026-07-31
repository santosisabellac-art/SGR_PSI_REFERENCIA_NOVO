import flet as ft


def app(page: ft.Page):
    page.title = "SGR - Psicóloga de Referência"

    page.window.width = 1400
    page.window.height = 900
    page.window.min_width = 1200
    page.window.min_height = 800

    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "SGR - Psicóloga de Referência",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Versão 0.1 Alpha",
                    size=18,
                    color=ft.Colors.GREY_700,
                ),
            ]
        )
    )


def main():
    ft.app(target=app)