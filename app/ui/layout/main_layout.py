import flet as ft


class MainLayout(ft.Row):
    """
    Layout principal da aplicação.

    Estrutura:

    ┌────────────┬──────────────────────────────┐
    │ Sidebar    │ Área de Conteúdo             │
    └────────────┴──────────────────────────────┘
    """

    def __init__(self, sidebar: ft.Control, content: ft.Control):
        super().__init__(
            expand=True,
            spacing=0,
            controls=[
                sidebar,
                ft.Container(
                    expand=True,
                    padding=30,
                    content=content,
                ),
            ],
        )

    def set_content(self, content: ft.Control):
        """
        Permite trocar o conteúdo central futuramente.
        """
        self.controls[1].content = content
        self.update()