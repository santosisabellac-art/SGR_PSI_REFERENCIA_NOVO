from app.repositories.aprendiz_repository import AprendizRepository


class AprendizService:

    def __init__(self):
        self.repository = AprendizRepository()

    def listar(self):
        return self.repository.listar()

    def buscar(self, aprendiz_id):
        return self.repository.buscar_por_id(aprendiz_id)

    def criar(
        self,
        nome,
        codigo,
        nivel_suporte,
        dias_atendimento="",
        horario="",
        sala="",
        carga_horaria_aba="",
        observacoes="",
    ):

        return self.repository.criar(
            nome=nome,
            codigo=codigo,
            nivel_suporte=nivel_suporte,
            dias_atendimento=dias_atendimento,
            horario=horario,
            sala=sala,
            carga_horaria_aba=carga_horaria_aba,
            observacoes=observacoes,
        )

    def atualizar(
        self,
        aprendiz_id,
        nome,
        codigo,
        nivel_suporte,
        dias_atendimento="",
        horario="",
        sala="",
        carga_horaria_aba="",
        observacoes="",
    ):

        return self.repository.atualizar(
            aprendiz_id=aprendiz_id,
            nome=nome,
            codigo=codigo,
            nivel_suporte=nivel_suporte,
            dias_atendimento=dias_atendimento,
            horario=horario,
            sala=sala,
            carga_horaria_aba=carga_horaria_aba,
            observacoes=observacoes,
        )

    def excluir(self, aprendiz_id):
        return self.repository.excluir(aprendiz_id)