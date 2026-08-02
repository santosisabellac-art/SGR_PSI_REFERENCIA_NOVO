import flet as ft

from app.ui.components.sidebar import Sidebar
from app.ui.layout.main_layout import MainLayout
from app.ui.pages.home_page import HomePage
from app.ui.theme.theme import AppTheme


def app(page: ft.Page):

    page.title = "SGR - Psicóloga de Referência"

    page.window.width = 1450
    page.window.height = 900

    page.bgcolor = AppTheme.BACKGROUND

    page.padding = 0

    home = HomePage()

    layout = MainLayout(
        sidebar=Sidebar(),
        content=home,
    )

    page.add(layout)


def main():
    ft.app(target=app)


if __name__ == "__main__":
    main()