import flet as ft

from app.services.aprendiz_service import AprendizService


class AprendizDialog(ft.AlertDialog):

    def __init__(self, page: ft.Page, on_save=None):
        super().__init__()

        self.page = page
        self.on_save = on_save
        self.service = AprendizService()

        self.nome = ft.TextField(label="Nome", expand=True)

        self.codigo = ft.TextField(label="Código Interno")

        self.nivel = ft.Dropdown(
            label="Nível de Suporte",
            options=[
                ft.dropdown.Option("Nível 1"),
                ft.dropdown.Option("Nível 2"),
                ft.dropdown.Option("Nível 3"),
            ],
        )

        self.dias = ft.TextField(
            label="Dias de Atendimento"
        )

        self.horario = ft.TextField(
            label="Horário"
        )

        self.sala = ft.TextField(
            label="Sala"
        )

        self.carga = ft.TextField(
            label="Carga Horária ABA"
        )

        self.obs = ft.TextField(
            label="Observações",
            multiline=True,
            min_lines=3,
            max_lines=5,
        )

        self.title = ft.Text("Novo Aprendiz")

        self.content = ft.Column(

            width=600,

            scroll=ft.ScrollMode.AUTO,

            controls=[

                self.nome,

                self.codigo,

                self.nivel,

                self.dias,

                self.horario,

                self.sala,

                self.carga,

                self.obs,

            ],

        )

        self.actions = [

            ft.TextButton(
                "Cancelar",
                on_click=self.cancelar,
            ),

            ft.ElevatedButton(
                "Salvar",
                icon=ft.Icons.SAVE,
                on_click=self.salvar,
            ),

        ]

    def cancelar(self, e):
        self.open = False
        self.page.update()

    def salvar(self, e):

        self.service.criar(

            nome=self.nome.value,

            codigo=self.codigo.value,

            nivel_suporte=self.nivel.value,

            dias_atendimento=self.dias.value,

            horario=self.horario.value,

            sala=self.sala.value,

            carga_horaria_aba=self.carga.value,

            observacoes=self.obs.value,

        )

        self.open = False

        if self.on_save:
            self.on_save()

        self.page.update()